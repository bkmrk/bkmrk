# bkmrk

[![Build Status](https://travis-ci.org/vicyap/bkmrk.svg?branch=master)](https://travis-ci.org/vicyap/bkmrk)

---

Do you ever want save a quote while reading?

## Developers

### Workflow

The workflow is centered around `pipenv`.

#### Setup

Set up [pipenv](https://docs.pipenv.org/).

`pip install pipenv`

Set up environment.

`source ./ENV`

#### Run

I mainly run things through `pipenv run <cmd>`.


```
source ./ENV
pipenv run flask run
```

#### pip and virtualenv

If you come from a `pip` and `virtualenv` workflow, here are a couple of
analogous operations.

* `pipenv shell` - `source venv/activate`. 
* `pipenv install` - `pip install -r requirements.txt`

#### Database

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

## Resources

* [Post/Redirect/Get](https://en.wikipedia.org/wiki/Post/Redirect/Get)
