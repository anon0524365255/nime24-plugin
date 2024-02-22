# torchdrum-plugin
Differentiable drum synthesizer plugin

**Note to reviewers**: Repo is in an in-progress state and will be fully updated with
compiled plugins for download ahead of the camera-ready submission.

## Building from Source

Clone project and pull submodules. Includes JUCE.
```
git clone --recurse-submodules git@github.com:jorshi/torchdrum-plugin.git
cd torchdrum-plugin
```

Install TorchLib dependency. One easy way to do this is via Python. Recommended to
create a new virtual environment or anaconda environment to do this.
```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.1.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install numpy
```

Save the TORCHLIB_PATH from Python
```
export TORCHLIB_PATH=`python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'`
```

Build with cmake
```
cmake -Bbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=$TORCHLIB_PATH
cmake --build build --config Release --parallel 4
```
