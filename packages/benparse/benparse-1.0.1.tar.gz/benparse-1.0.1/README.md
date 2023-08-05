# benparse
benparse is a bencode parser for Python 3. It is capable of reading and creating [bencoded files](https://en.wikipedia.org/wiki/Bencode) such as torrents

## Features
* Syntax is similar to built-in modules such as `json` and `pickle`
* Has an optional strict mode that will raise an error when it encounters non-fatal errors such as out-of-order dict keys or integers with leading zeros. This ensures that "round-tripping" bencoded data (loading bencoded data and then dumping it back to bencode) will never caused unexpected changes
* Able to change the character encoding used to encode/decode strings
* Fully typed

## Usage
Complete usage documentation and examples are available [here](https://adralioh.gitlab.io/benparse)

```python
# Load a bencoded file
with open('linux_distro.torrent', 'rb') as file:
    torrent_dict = benparse.load(file)

# Make changes
torrent_dict[b'announce'] = b'http://mirror.example.org:6969/announce'

# Save a Python object as a bencoded file
with open('linux_distro.torrent', 'wb') as file:
    benparse.dump(torrent_dict, file)
```

## Requirements
- [Python 3.6+](https://www.python.org/)
- [Typing Extensions](https://pypi.org/project/typing-extensions/) (only for Python versions less than 3.8)

## Installation
Install from PyPI:
```shell
pip3 install benparse
```

Install from source:
```shell
git clone https://gitlab.com/adralioh/benparse.git
pip3 install ./benparse
```

## Tests
Tests are run using the built-in `unittest` module, and [Coverage.py](https://coverage.readthedocs.io/) is used to measure code coverage

Run tests without measuring coverage:
```shell
python3 -m unittest discover tests
```

Run tests and measure coverage:
```shell
coverage run -m unittest discover tests
```

View the results:
```shell
coverage report
```

Generate a detailed report, outputted to `./htmlcov`:
```shell
coverage html
```

## Building documentation
Sphinx is used to build documentation

Build requirements:
- [Sphinx](https://www.sphinx-doc.org/)

How to build:
```shell
cd docs
make html
```
