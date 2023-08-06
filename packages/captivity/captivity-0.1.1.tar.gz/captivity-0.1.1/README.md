# Getting started with Captivity

The only purpose of `captivity` is to support you in writing better `pandas` code by caging in
some of its worst excentricities. `pandas` is great, but `import captivity; import pandas as pd` is better.

The philosophy behind `captivity` is that there's nothing worse than silent failure. If you didn't ask pandas to automagically correct your arguments, it shouldn't.

## Example

To find a comprehensive set of examples, check out the `captivity/tests/` directory. To pique your interest, consider the following:

```python
import pandas as pd

a = pd.DataFrame({
    "x": [1, 2], 
    "y": [3, 4]}
)

b = pd.DataFrame({
    "z": [5, 6],
    "x": [9, 0]
})

a_b = pd.concat([a, b], axis=1)

print(a_b)
>>    x  y  z  x
>> 0  1  3  5  9
>> 1  2  4  6  0 

``` 

Woa! That should definitely not be allowed by default. With `captivity`, it's not.

```python
...
a_b = pd.concat([a, b], axis=1)

>> Traceback (most recent call last):
>> ...
>> captivity.CaptivityException: Column-wise concatenation would result in duplicate column labels for column: {'x'}

```

In addition, captivity currently supports:
* **sensible checks on vertical concatenation (column sets must match)**
* **sensible checks on merges (no more `_x` and `_y` columns - except when `suffixes=("_x", "_y")` is passed explicitly)**
* turning `CaptivityExceptions` into `CaptivityWarnings` - useful when first using `captivity` in an existing codebase

## Does it also catch \<Issue X\> ?
`captivity` is a labor not of love, but of annoying bugs I find in my own code that are caused by careless default arguments in pandas. 
If you find one in yours that you'd like captivity to patch, please raise an issue on GitHub or contact me directly (or better yet, implement
it and put out a PR!)

 ## Running the tests
 
 To test `captivity`, run `pytest --cov` in the root directory of this project.
 
 ## Installation
 To install `captivity`, simply run `pip install git+https://github.com/maxsnijders/captivity.git`. 

