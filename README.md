# bkmrk

[![Build Status](https://travis-ci.org/vicyap/bkmrk.svg?branch=master)](https://travis-ci.org/vicyap/bkmrk)
[![Coverage Status](https://coveralls.io/repos/github/vicyap/bkmrk/badge.svg?branch=master)](https://coveralls.io/github/vicyap/bkmrk?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/f8cc867b3d1ec2ddd655/maintainability)](https://codeclimate.com/github/vicyap/bkmrk/maintainability)

---

Do you ever want save a quote while reading?

## Developers

### Workflow

The workflow is centered around `pipenv`.

#### Setup

Set up [pipenv](https://docs.pipenv.org/).

`pip install pipenv`

#### Run

I mainly run commands through `pipenv run <cmd>`.

```
pipenv run flask run
```

#### pip and virtualenv

If you come from a `pip` and `virtualenv` workflow, here are a couple of
analogous operations.

* `pipenv shell` - `source venv/activate`. 
* `pipenv install` - `pip install -r requirements.txt`

#### Database

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

#### Resources

* [Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Post/Redirect/Get](https://en.wikipedia.org/wiki/Post/Redirect/Get)
* [Setting Up HTTPS](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04)
