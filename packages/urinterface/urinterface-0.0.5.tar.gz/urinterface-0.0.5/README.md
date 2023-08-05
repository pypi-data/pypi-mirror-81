# URInterface

## Overview 

This library facilitates data acquisition and commands of the UR Robot e-series.
It establishes a TCP/IP connection to the UR robot and allows to execute UR script commands, log data, etc.
Please note, that the robot should be configured in `Remote Control` mode.
The UR robot can be controlled remotely in various ways:
1. Dashboard server (port 29999): https://www.universal-robots.com/articles/ur/dashboard-server-e-series-port-29999/
   Allows for commands like `power on`, `load <program.urp>`, `play`, `stop`, `pause`, etc.
2. Send script commands (port 30001 or 30002): https://www.universal-robots.com/articles/ur/remote-control-via-tcpip/
   Allows for commands like `movej([0.1,0.2,0.3,0.4,0.5,0.6],v=1.0,a=2.0)` and many more, see
   https://www.universal-robots.com/download/?option=77326#section77085
   Frequency: 10 Hz
3. Real-Time Data Exchange (RTDE): https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/
   Allows to send and receive data with up to 500 Hz

## Installing URInterface from pip

```
pip install urinterface
```

## Installing URInterface locally (for development and local use)

Change to the root directory of this project and:
```
pip install -e .
```


## Setting up dev environment in PyCharm.

1. Open the root of this repo as a new project from sources in PyCharm.
1. Make sure that most root folders are set as project source folders (Settings > Project Structure > Mark the folders as source folders )
1. Run the tests and install missing dependencies

## Installing UR Robot Simulator

If using virtual box, then follow the instructions in https://www.universal-robots.com/download/

If using Hyper-V, then install ubuntu VM and then install the UR Robot simulator. Make use to use the quick create menu, so that you get clipboard and all that stuff for free (see https://superuser.com/questions/734880/hyper-v-clipboard-and-integration-services-in-ubuntu)

This package has been tested with **UR Sim for Linux 5.9.1**.

## Publishing this package on pypi

Instructions adapted from: https://packaging.python.org/tutorials/packaging-projects/

Delete generated directories.

Make sure to install dependencies:

```
pip install setuptools wheel twine
```

Create source distribution
```
python setup.py sdist
```
Create binary distribtion
```
python setup.py bdist_wheel
```

Upload package:
```
python -m twine upload dist/*
set user and password according to pypi's api token
```






## Common Errors

### Failure to boot from ISO file

with the following error:
```
No operating system was loaded. Your virtual machine may be configured incorrectly. Exit and re-configure...
```

The solution is to follow this guide: https://www.thomasmaurer.ch/2018/06/how-to-install-ubuntu-in-a-hyper-v-generation-2-virtual-machine/



## Error when running the unit tests from PyCharm

Error:
```
Testing started at 08:54 ...
H:\srcctrl\gitlab\urinterface\venv\Scripts\python.exe "C:\Program Files\JetBrains\PyCharm Community Edition 2020.1.1\plugins\python-ce\helpers\pycharm\_jb_pytest_runner.py" --target robot_connection_tests.py::MyTestCase.test_dummy_start_stop_record
Traceback (most recent call last):
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2020.1.1\plugins\python-ce\helpers\pycharm\_jb_pytest_runner.py", line 4, in <module>
    import pytest
ModuleNotFoundError: No module named 'pytest'

Process finished with exit code 1
```

Solution: 

1. Clear all run configurations, and create a new one using unittest.

