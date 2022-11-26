# HyperGui

## MacOS
#### Installation Instructions
Download HyperGUI by clicking the green 'Clone or Download' button and downloading and unpacking the .zip file.

To install Python, go to python.org/downloads/ and download version 3.7.4.

To install the required packages, navigate to terminal and type in `pip3 install --user -r /path/requirements.txt`, where 'path' refers to the path of directories required to reach the file `requirements.txt` (for example, 'Users/joe/downloads/HyperGUI_1.0-master'). Alternatively, type the following into the terminal as separate commands:
- `pip3 install --user cycler`
- `pip3 install --imageio`
- `pip3 install --kiwisolver`
- `pip3 install --matplotlib`
- `pip3 install --networkx`
- `pip3 install --numpy`
- `pip3 install --opencv-python'
- `pip3 install --pandas'
- `pip3 install --Pillow`
- `pip3 install --pyparsing`
- `pip3 install --python-dateutil`
- `pip3 install --pytz'
- `pip3 install --PyWavelets`
- `pip3 install --scikit-image`
- `pip3 install --scipy`
- `pip3 install --six`
- `pip3 install --tifffile'
- `pip3 install --XlsxWriter'

Correct versions are: cycler==0.10.0, imageio==2.9.0, kiwisolver==1.3.1, matplotlib==3.4.2, networkx==2.6.2, numpy==1.21.1, opencv-python==4.5.3.56, pandas==1.3.1, Pillow==8.3.1, pyparsing==2.4.7, python-dateutil==2.8.2, pytz==2021.1, PyWavelets==1.1.1, scikit-image==0.18.2, scipy==1.7.1, six==1.16.0, tifffile==2021.8.8, XlsxWriter==3.0.1

#### Running Instructions
Navigate to terminal and type in `cd ` (with space at the end). Then click the HyperGui folder in your Finder and drag and drop it into the terminal. Press enter and type in `python3 HyperGui.py` and press enter again. The software should launch now.


## Windows
#### Installation Instructions
Download HyperGUI by clicking the green 'Clone or Download' button and downloading and unpacking the .zip file.

To install Python, go to python.org/downloads/ and download version 3.7.4.

To instal pip, go to https://pip.pypa.io/en/stable/installing/ and download get-pip.py. Then, navigate to Command Prompt and type in `cd path` where 'path' refers to the path of directories required to get to where get-pip.py is. Then, type `python get-pip.py`.

To install the required packages, navigate to Command Prompt and type in `cd path` where 'path' refers to the path of directories that finished with `HyperGUI_1.0-master`. Once in the HyperGUI directory, type `pip3 install --user -r requirements.txt`. Alternatively, type the following into Command Prompt as separate commands:
- `pip3 install --user cycler`
- `pip3 install --imageio`
- `pip3 install --kiwisolver`
- `pip3 install --matplotlib`
- `pip3 install --networkx`
- `pip3 install --numpy`
- `pip3 install --opencv-python'
- `pip3 install --pandas'
- `pip3 install --Pillow`
- `pip3 install --pyparsing`
- `pip3 install --python-dateutil`
- `pip3 install --pytz'
- `pip3 install --PyWavelets`
- `pip3 install --scikit-image`
- `pip3 install --scipy`
- `pip3 install --six`
- `pip3 install --tifffile'
- `pip3 install --XlsxWriter'

Correct versions are: cycler==0.10.0, imageio==2.9.0, kiwisolver==1.3.1, matplotlib==3.4.2, networkx==2.6.2, numpy==1.21.1, opencv-python==4.5.3.56, pandas==1.3.1, Pillow==8.3.1, pyparsing==2.4.7, python-dateutil==2.8.2, pytz==2021.1, PyWavelets==1.1.1, scikit-image==0.18.2, scipy==1.7.1, six==1.16.0, tifffile==2021.8.8, XlsxWriter==3.0.1

#### Running Instructions
Navigate to Command Prompt and type in `cd ` (with space at the end). Then click the HyperGui folder in your downloads folder and drag and drop it into the Command Prompt window. Press enter and type in `python HyperGui.py` and press enter again. The software should launch now.


## Development Notes
#### Regarding Performance
For every folder uploaded, it's scanned for a data cube,
and that data cube is processed fully for all of the analysis patterns.
Similarly, for every change in mode (Normal vs Original, Masked vs. Whole, etc.),
every data cube will be updated accordingly.
Also, when switching between data cubes,
all the images will be re-rendered, which also takes time.

You can see the progress of the calculations in the logs.

**Currently, it's not advisable to run more than ~10 data cube directories at a time.**

If the program hangs or bugs out, press `Ctrl-C` in the console to shut it down.
