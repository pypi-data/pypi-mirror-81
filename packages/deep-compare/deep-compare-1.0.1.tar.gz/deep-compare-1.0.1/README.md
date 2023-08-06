# Deep Compare
![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg) ![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)

Deep Compare is a simple module that lets the user compare two variables irrespective of their current datatype.

## Installation
$ pip install -i https://test.pypi.org/simple/ deep-compare

## Requirements
 - Python3.7+

## Usage

install the Deep Compare package using the command

```bash
$ pip install -i https://test.pypi.org/simple/ deep-compare
```

you will be able to use package after installation by importing it in your python file like
```python
from deep-compare import compare_variables.CompareVariables
```
CompareVariables includes 11 methods

##### 1. is_float(value)
    returns True if the value is an integer or float, else returns False.

```python
a = '17.5'
is_float = CompareVariables.is_float(a)
print(is_float)
```
output
```bash
>>> True
```
```python
a = 'hi'
is_float = CompareVariables.is_float(a)
print(is_float)
```
output

```bash
>>> False
```

##### 2. is_date_time(value)
    returns True if value is a date or date-time(if the input datatype is a string the date or datetime must be in iso time format and the python version used must be 3.7 or above) else returns False.

```python
a = '2020-12-12 10:45'
is_date_time = CompareVariables.is_date_time(a)
print(is_date_time)
```
output

```bash
>>> True
```
```python
a = '15th january 2020 '
is_date_time = CompareVariables.is_date_time(a)
print(is_date_time)
```
output

```bash
>>> False
```

##### 3. can_literal_eval(value)
    returns True if value is a list, dict, tuple, set etc.

```python
a = '[2,5,6]'
can_literal_eval = CompareVariables.can_literal_eval(a)
print(can_literal_eval)
```
output

```bash
>>> True
```

##### 4. is_complex(value):
    returns True if value is a complex number else returns False.

```python
a = '3 + 5j'
is_complex = CompareVariables.is_complex(a)
print(is_complex)
```
output

```bash
>>> True
```
```python
a = '15th january 2020 '
is_complex = CompareVariables.is_complex(a)
print(is_complex)
```
output

```bash
>>> False
```

##### 5. compare(value1, value2)
    returns True if the values are equal else returns False.

```python
a = 5
b = 5
output = CompareVariables.compare(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = 5
b = '5'
output = CompareVariables.compare(a,b)
print(output)
```
output

```bash
>>> False
```
##### 6. compare_date(value1, value2):
    returns True if the two input date values(value can be iso time format string also) are equal else returns False.

```python
a = '2020-12-12 10:58'
b = '2020-12-12'
output = CompareVariables.compare_date(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = '2020-12-12 10:58'
b = '2020-10-12 10:58'
output = CompareVariables.compare_date(a,b)
print(output)
```
output

```bash
>>> False
```

##### 7. compare_datetime(value1, value2):
    returns True if the input two input datetime values(value can be iso time format string also) are equal else returns False.

```python
from datetime import datetime

a = '2020-12-12 10:58'
b = datetime(2020,12,12,10,58)
output = CompareVariables.compare_datetime(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = '2020-12-12 10:58'
b = '2020-12-12 11:58'
output = CompareVariables.compare_datetime(a,b)
print(output)
```
output

```bash
>>> False
```

##### 8. datatype_check(value):
    returns the input value in its correct datatype else returns False.

```python
a = '3 + 4j'
output = CompareVariables.datatype_check(a)
print(output)
```
output

```bash
>>> 3+4j
```

##### 9. compare_list_or_tuples_or_set(value1, value2):
    returns True if the input values(list/tuple/set) are equal else returns False.

```python
a = '[1,2,3,44]'
b = '["1","2","3","44"]'
output = CompareVariables.compare_list_or_tuples_or_set(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = '[1,2,3,44]'
b = '["1","2","3"]'
output = CompareVariables.compare_list_or_tuples_or_set(a,b)
print(output)
```
output

```bash
>>> False
```

##### 10. compare_dicts(value1, value2):
    returns True if the input values(dicts) are equal else returns False.

```python
a = '{"1":"2",3:5}'
b = {1:2,3:5}
output = CompareVariables.compare_dicts(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = '{"1":"2",3:5}'
b = {1:2,3:5,4:6}
output = CompareVariables.compare_dicts(a,b)
print(output)
```
output

```bash
>>> False
```

##### 11. type_matching_and_compare(value1, value2):
    returns True if the values are equal irrespective of the input datatype else returns False.

```python
a = '{"1":"2",3:5}'
b = {1:2,3:5}
output = CompareVariables.type_matching_and_compare(a,b)
print(output)
```
output

```bash
>>> True
```
```python
a = '[1,2,3,44]'
b = '["1","2","3"]'
output = CompareVariables.type_matching_and_compare(a,b)
print(output)
```
output

```bash
>>> False
```

## Communication
If you find a bug, open an issue.
If you have a feature request, open an issue.
If you want to contribute, submit a pull request.