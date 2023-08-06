![PyPI](https://img.shields.io/pypi/v/meapy?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/meapy?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meapy?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/meapy?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/meapy?style=flat-square)

# MeaPy
Python API Wrapper for Measurement Data

## Vision
MeaPy wants to be a easy-to-use and conformable API for working with measurement data in den Big Test Data environment.

## Getting Started
```
pip install meapy
```

## Usage
```python
from meapy import MeaPy, MeasurementList, LoadingConfig

# "Basic " is the content if the HTTP Authorization-Header. In this example it is the Basic Authentication Header for user:password
mp = MeaPy("http://madam-docker.int.kistler.com:8081/", "Basic dXNlcjpwYXNzd29yZA==")

# direct search (by default limited to 100 results)
result = mp.search("test")
# result is a list of meapy.Measurement

# search and iteration over the whole result set
ml = MeasurementList(mp)
count = 0
for mea in ml.items('Station.Id="d4f1ad55-72d5-403c-81b8-73b2942b58f4"'):
    count+=1
print(count)

# load a measurement
config = LoadingConfig()
config.withSignals(['time'])
signals = mp.load(result[0], config)
# signals is a list of meapy.SignalData that contains the information for the requested channels
```
