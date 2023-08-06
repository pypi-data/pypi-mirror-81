# dvpipe

> A small Python utility for piping data from function to function in sequential order.

dvpipe allows you to pass data from function to function sequentially as you would in
tradional method chaining. You can use dvpipe to transform any type of data not
just DataFrames as with [DataFrame.pipe()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html)

Example Usage:
```python
from dvpipe import pipe


df = (pipe(df,
           clean,
           transform,
           dump_to_csv))
```


Use Python tuples for functions with parameters.
```python
df = pipe(df, (dump_to_csv, 'output.csv'))
```
