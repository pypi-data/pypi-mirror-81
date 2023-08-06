Python Data Reader
===============
This is a Python module currently built for python >= 2.7


## Basic Usage

After getting the ISReader module, usage is really simple:

```python
from ISReader.Reader import Reader

# create Reader instance
reader = Reader(access_key="YOUR_ACCESS_KEY", bucket_key="YOUR_BUCKET_KEY")

# get latest events for all stream keys
all_latest_events = reader.get_latest()

# get latest events for specific stream keys
signal_keys = ['signal_a', 'signal_b']
events = reader.get_latest(keys=signal_keys)
```
