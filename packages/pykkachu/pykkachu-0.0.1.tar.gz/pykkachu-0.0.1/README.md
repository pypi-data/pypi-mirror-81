# Pykkachu

A convenience library on top of Pykka and PySM to help with common Actor Model patterns.
[Github](https://github.com/amcknight/pykkachu)

## Roadmap
### v0.1
- Expand to work with all Actor types instead of just ThreadingActors
- Better encapsulate Pykka and PySM so they are not imported by users
- Make Fleet abstract and take a subactor selection algorithm as param
- Unit tests
### Beyond
- Create a config loader for wiring up simple Actors
- Add simple patterns like "Retry" and "When"

## Changelog
### v0.0.1
- Made it exist by pulling it from [gab](https://github.com/amcknight/gab)
- Factored it into classes
- Pulled a Message class in from [gab](https://github.com/amcknight/gab)

## Deployment

```commandline
rm -rf dist
pipenv shell
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
exit
```
