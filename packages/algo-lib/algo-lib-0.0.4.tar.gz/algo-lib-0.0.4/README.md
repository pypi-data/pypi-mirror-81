# Algo-lib (the Algorithm Library)

This is a simple example package. It contains two searching algorithms. The purpose of this repo is to practice packaging a library for distribution. 

### Quick Start

1. Install algo-lib from the command line using pip.
```
python3 -m pip install --upgrade algo-lib
```

#### Example Usage

1. Binary Search
```python
from algo_lib.search.Search import Search

lst = [1, 50, 99, 150, 40000]
targetValue = 99

#binary search returns the index of a target value if present in a sorted list
targetIndex = Search.binary(lst, 0, len(lst) - 1, targetValue) #targetIndex is 2
```

2. Linear Search
```python
from algo_lib.search.Search import Search

lst = [5, 1, 2, 100, 41, -1]
targetValue = -1

#linear search returns the index of a target value if present in list
targetIndex = Search.binary(lst, targetValue) #targetIndex is 5
```