# Star Atlas Price Monitor
This project has been structured following the [python-blueprint](https://github.com/johnthagen/python-blueprint)
from [johnthagen](https://github.com/johnthagen).

This is small project, I'm using to learn python. It strives to be good idiomatic python, but being 
myself a newbie to python programming is probably full of mistakes and there's for sure potential
for great improvement. I'll add those improvements and make things more idiomatic as I learn.

## What's this project about?

SAMO (Star Atlas Monitor) is a very simple application that downloads the list of ship
prices from aephia.com and stores them for later use.

## Future enhancements
- Alerting: Send alerts based on certain prices thresholds being reached, on new items being sold...
- Price charting: Show a visual representation of Star Atlas NFT prices over time.

## Command Cheatsheet
### Poetry

#### One-time initialization
```
poetry install
```

#### Add a project dependency
```
poetry add requests
```

#### Add a dependency to a specific group
```
poetry add types-requests --group test type_check
```

#### Activate poetry's virtual env
```
poetry shell
```

#### Run main file
```
poetry run python3 src/samo/monitor.py
```

#### Build package
```
poetry build
```

### Nox
#### Run all checks
```
nox
```
#### Execute tests
```
nox -s test -- -k prune_non_relevant_fields
```
#### Code Style check
```
nox -s lint
```
#### Code Formatting
```
nox -s fmt
```
```
nox -s fmt_check
```


#### List dependecies' licenses
```
nox -N -s licenses
```

### Other
#### Print dependency tree
```
pipdeptree
```

## References
- https://github.com/typeddjango/awesome-python-typing