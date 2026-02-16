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
### Docker
For installation steps refer to [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## How to build and run the docker image
To build the container image:
```
docker build --tag sanmo .
```
To run the image in a container:
```
docker run --rm -v sanmo-store:/home/user/sanmo_store sanmo
```

## How to build, run tests, ...
Run inside the poetry virtual environment
```
poetry run python3 src/sanmo/price_fetcher.py
```

Start a shell on the poetry virtual environment
```
poetry shell
```

Add dependencies
```
poetry add black
```

Install dependencies
```
poetry install
```

Build archive
```
poetry build
```

Show dependency tree
```
poetry show --tree
```

## References
- https://github.com/typeddjango/awesome-python-typing
- https://www.yippeecode.com/topics/python-poetry-cheat-sheet/
- https://referenceguide.dev/cheatsheet/dockerfile