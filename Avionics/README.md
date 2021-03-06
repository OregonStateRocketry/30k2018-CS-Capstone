## Overview
This is the payload avionics software for OSU's 2017-18 ESRA 30k rocket.

The payload will be ejected from the rocket body at apogee (near 30,000 feet) and will begin to fall.  The payload will then attempt to accelerate downward to sustain 0 G from it's perspective, for 10-12 seconds in order to support an on-board biological experiment.

The payload carries a brushless motor and esc on the nose, and an internal reaction wheel that it will use to counter the torque created by the propeller.

After the experiment, the payload will eject a drogue parachute at 20,000 feet, and a primary parachute at 2,000 feet.

## Install

This software is intended to run on a raspberry pi zero computer.

```
$ chmod +x installPayload.sh
$ sudo ./installPayload.sh
```

The software is designed to run automatically on startup, however, you can also run it manually with:

`Avionics/Payload/$ python3 mainPayloadState.py`

To run unit tests, make sure you have the `coverage` library installed:

`pip install coverage`

Then run the tests:

`coverage run unitTests.py`

And view the report for whichever modules you're interested in:

`coverage report -m ESCMotor.py MPL3115A2.py MPU9250.py PCF8523.py mainPayload.py payloadState.py`

You can also see a general report using `coverage report` but it will include some libraries that we are not responsible for writing.
