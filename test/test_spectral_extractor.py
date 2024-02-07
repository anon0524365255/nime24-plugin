import math

import cppyy
import pytest
import torch

# import matplotlib.pyplot as plt

SR = 48000


def test_spectral_extractor_init(torchdrum):
    extractor = torchdrum.SpectralExtractor()
    assert isinstance(extractor, torchdrum.SpectralExtractor)


def test_spectral_extractor_prepare(torchdrum):
    extractor = torchdrum.SpectralExtractor()

    fft_size = 256
    extractor.prepare(SR, fft_size)

    assert extractor.getSampleRate() == SR

    fft = extractor.getFFT()
    assert fft.getSize() == fft_size
    assert extractor.getFFTBuffer().size() == fft_size * 2

    # Confirm the window function is set
    window = extractor.getFFTWindow()
    assert window.size() == fft_size

    # Compare to the window from torch
    torch_window = torch.hann_window(fft_size, periodic=False)
    window = torch.tensor(window)
    assert torch.allclose(window, torch_window, atol=1e-4)


def test_spectral_extractor_process_fft(torchdrum, controller):
    extractor = torchdrum.SpectralExtractor()

    fft_size = 256
    extractor.prepare(SR, fft_size)

    buffer = controller.getFeatureBuffer()
    buffer.setSize(1, fft_size)

    # Create a test sinusoid
    w0 = 2 * torch.pi * 440 / SR
    phase = torch.ones(fft_size) * w0
    x = torch.sin(torch.cumsum(phase, dim=0))

    for i in range(buffer.getNumSamples()):
        buffer.setSample(0, i, x[i])

    results = cppyy.gbl.std.vector[float]()
    results.resize(1)
    extractor.process(buffer, results)

    fftBuffer = extractor.getFFTBuffer()
    assert fftBuffer.size() == fft_size * 2
    results = torch.tensor(fftBuffer)

    # Compare to the expected FFT from torch
    x_window = x * torch.hann_window(fft_size, periodic=False)
    expected = torch.abs(torch.fft.rfft(x_window))

    nyquist = fft_size // 2 + 1
    assert torch.allclose(results[:nyquist], expected[:nyquist], atol=1e-4)


def test_spectral_extractor_process_centroid(torchdrum, controller):
    extractor = torchdrum.SpectralExtractor()

    fft_size = 256
    extractor.prepare(SR, fft_size)

    buffer = controller.getFeatureBuffer()
    buffer.setSize(1, fft_size)

    # Create a test sinusoid
    bin_freq = SR / fft_size
    f0 = bin_freq * 10.0
    w0 = 2 * torch.pi * f0 / SR

    phase = torch.ones(fft_size) * w0
    x = torch.sin(torch.cumsum(phase, dim=0))

    for i in range(buffer.getNumSamples()):
        buffer.setSample(0, i, x[i])

    results = cppyy.gbl.std.vector[float]()
    results.resize(1)
    extractor.process(buffer, results)

    expected = 12 * math.log2(f0 / 440.0) + 69.0
    assert results[0] == pytest.approx(expected, rel=1e-3)
