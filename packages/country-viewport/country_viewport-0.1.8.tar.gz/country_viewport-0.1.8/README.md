# Country-viewport

If you are in need of fetching viewports from countries, but do not want to use Google APIs, this package is for you.

### Installation

```sh
$ pip3 install country-viewport
```

### Usage

```python
>>> import country_viewport
>>> country_viewport.get('CU')
{
    'min_latitude': 19.90553,
    'min_longitude': -84.28599,
    'max_latitude': 23.15917,
    'max_longitude': -74.15181,
}
```

## License

MIT
