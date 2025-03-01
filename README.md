# code coverage sample application

This is a sample application with unit tests and code coverage using coverage.py.

## python setup 
```bash
pip install -r requirements.txt
coverage run -m unittest discover
coverage report -m
coverage xml