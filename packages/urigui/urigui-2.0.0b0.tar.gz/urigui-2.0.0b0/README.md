[![Build Status](https://travis-ci.org/vasi/pixz.svg?branch=master)](https://vininjr.github.io)
# URI Online Judge Command Line Interface
Utility CLI for submitting solutions to URI Online Judge

### Install:
```
  pip install -U urigui
  or
  pip3 install -U urigui
```

### Usage:
  - uri login
  - uri set_language
  - uri submit <solution_path> <problem_id>
  - uri live

### Arguments:
```
    <solution_path>     Path to the file containing to solution.
    <problem_id>        URI Online Judge's problem ID
```

### Example:
```
uri submit /home/USER/codes/problem2010.cpp 2010
```

### Language Id's:

| Id     | Name |
| ---      | ---       |
|1 | C|
|2 | C++|
|3 | Java|
|4 | Python|
|5 | Python 3|
|6 | Ruby|
|7 | C#|
|8 | Scala|
|9 | Lua|
|10 | Javascript|
|11 | Java 8|
|12 | Go|
|14 | C99|
|15 | Kotlin|
|16 | C++17|
|17 | Haskell|
|18 | Ocaml|
|19 | Pascal|
|20 | Python 3.8|
|21 | Java 14|

### Attribution

This Code is adapted from the [Rafael Telles][homepage], version 0.2.0,
available at [PyPI][version]

[homepage]: https://github.com/rafael-telles/uricli
[version]: https://pypi.org/project/uricli/