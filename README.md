# Star Atlas Price Monitor
This project has been structured following the [python-blueprint](https://github.com/johnthagen/python-blueprint)
from [johnthagen](https://github.com/johnthagen).

This is small project, that I'm personally using to learn python. Although it strives to be idiomatic
python, it's probably full of mistakes since I'm myself pretty new to the language. This gives huge
potential upside for improvements. I'll add those improvements and make things more idiomatic as I learn.

## What's this project about?

SAMO (Star Atlas Monitor) is a very simple application that downloads the list of ship
prices from aephia.com and stores them for later use.

## Future enhancements
- Alerting: Send alerts based on certain prices thresholds being reached, on new items being sold...
- Price charting: Show a visual representation of Star Atlas NFT prices over time.

## Project Pre-requisities
### Poetry
In ubuntu in can be installed like this:
```
curl -sSL https://install.python-poetry.org | python3 -\n
```
### Terraform
In ubuntu in can be installed as a snap
```
sudo snap install terraform --classic
```

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
poetry add types-requests --group type_check
```
```
poetry add boto3 --group dev
```

#### Activate poetry's virtual env
```
poetry shell
```

#### Run main file
```
poetry run python3 src/sanmo/monitor.py
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
### Terraform
#### Initialize terraform
```
terraform init
```
#### Formatting and validation
```
terraform fmt
```
```
terraform validate
```
### Materializing resources
```
terraform plan
```
```
terraform apply
```
### Cleaning up resources
```
terraform destroy
```
## References
- https://github.com/typeddjango/awesome-python-typing