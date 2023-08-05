# zylogger

A logger that can be used directly without any config.

## build
```
python setup.py sdist bdist_wheel
```

## upload to test_pypi
```
python -m twine upload --verbose --repository testpypi dist/*
```

## upload to pypi
```
python -m twine upload
```

## usage
### install
```
pip install zylogger
```

### usage
```
import logging

import zylogger

zylogger.init()

logging.info('hello zylogger')
```
