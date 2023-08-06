# Bitmask decoder

Python wrapper to decode days-of-week bitmasks.

This mask is created by assigning an integer to each day of the week and summing up the integers of the relevant days.

It is assumed that the days are assigned as follows:

- Monday: 1
- Tuesday: 2
- Wednesday: 4
- Thursday: 8
- Friday: 16
- Saturday: 32
- Sunday: 64

Any combinations of these days can be summed up to create a mask for that specific combination. For example:

`42 = tuesday, thursday and saturday`

## Installation
bitmask-decoder is available via pip.

` pip install -i https://test.pypi.org/simple/ bitmask-decoder==0.0.2`


## 2 Functions
- `bitmask_decoder.decode_weekday()`

# Example

```python
import bitmask_decoder
bitmask_decoder.decode_weekday(17) # ['Mon', 'Fri']
```
