# curlyboi

Actually a snek!

## Build

```
$ g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --include` example.cpp -o _curlyboi.`python3-config --extension-suffix`
```

## Install

You can clone the repo and then install `curlyboi` using `pip`:

```
$ pip install .
```

## Usage

```
$ curlyboi
```

## Versioning

`curlyboi` uses [Semantic Versioning](https://semver.org/). For the available versions, see the tags on the GitHub repository.

## License

This project is licensed under the Apache License, see the [LICENSE](https://github.com/vinayak-mehta/curlyboi/blob/master/LICENSE) file for details.
