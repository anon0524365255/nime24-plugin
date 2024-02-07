#include "SinusoidalOscillator.h"
#include <juce_audio_basics/juce_audio_basics.h>

SinusoidalOscillator::SinusoidalOscillator()
{
    // Constructor - set default values
    sampleRate = 44100.0;
    modAmount = 0.0;
    phase = 0.0;
    setFrequencyHz(440.0);
}

void SinusoidalOscillator::prepare(double sr)
{
    sampleRate = sr;

    // Reset internal state
    phase = 0.0;
}

float SinusoidalOscillator::process(float modulation)
{
    float out = sin(static_cast<float>(phase));
    double mod = phaseIncr * modulation * modAmount;
    phase += phaseIncr + mod;
    if (phase > 2.0 * M_PI)
        phase -= 2.0 * M_PI;
    return out;
}

void SinusoidalOscillator::setFrequencyHz(float newValue)
{
    frequency = newValue;
    phaseIncr = static_cast<float>(2.0 * M_PI * frequency / sampleRate);
}

void SinusoidalOscillator::setModAmount(float newValue)
{
    modAmount = newValue;
}
