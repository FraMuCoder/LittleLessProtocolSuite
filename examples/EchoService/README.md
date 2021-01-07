# Echo Service Example using Little Less Protocol for Python

To run this example you will need [Little Less Protocol for Python](https://github.com/FraMuCoder/PyLittleLessProtocol).
Follow the instruction to build Little Less Protocol for Python distribution package and call:
```bash
python3 -m venv env
source env/bin/activate
pip install <PATH_TO_LITTLE_LESS_PROTOCOL_FOR_PYTHON>/dist/littlelessprotocol-0.0.1-py3-none-any.whl
python EchoService.py -d /dev/ttyUSB0
```

To see a result you will also need a running Echo Service.
Use the example in [Little Less Protocol for Arduino (develop)](https://github.com/FraMuCoder/LittleLessProtocol/tree/develop).
