# Star Atlas Price Monitor
This project has been structured following the [python-blueprint](https://github.com/johnthagen/python-blueprint)
from [johnthagen](https://github.com/johnthagen).

This is small project, I'm using to learn python. It strives to be good idiomatic python, but being 
myself a newbie to python programming is probably full of mistakes and there's for sure potential
for great improvement. I'll add those improvements and make things more idiomatic as I learn.

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

### Nox
#### Run all checks
```
nox
```