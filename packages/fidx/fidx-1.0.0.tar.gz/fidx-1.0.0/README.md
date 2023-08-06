# fidx
> A module for float and custom indexes in Python

Allows to use float indexes to access lists, tuples, … in percentage (e.g. 0.5 is the middle item).  
Allows also to add custom index types to existing types or to custom ones.

## Installation

```sh
pip install fidx
```

## Usage example

```python
>>> import fidx

>>> fidx([1,2,3])[.5]
2

>>> l = fidx([1,2,3,4])
>>> l[:.5], l[.5:]
([1, 2], [3, 4])

>>> t = fidx.tuple(i//2 for i in range(0,10))
>>> t[.2:-.2:.2]
(1, 2, 3)
```

_For more examples and usage, please refer to the [Wiki][wiki]._

## About

Davide Peressoni – dpdmancul+fidx@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

<https://gitlab.com/DPDmancul/>


<!-- Markdown link & img dfn's -->
[wiki]: https://gitlab.com/DPDmancul/fidx/-/wikis/home
 
