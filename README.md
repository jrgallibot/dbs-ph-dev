<<<<<<< HEAD
# dbs-ph-dev
=======
# Indexer App

Let's get your pages crawled and indexed.

## Installation - Docker

The easiest way to get up and running is with [Docker](https://www.docker.com/).

Just [install Docker](https://www.docker.com/get-started) and
[Docker Compose](https://docs.docker.com/compose/install/)
and then run:

```
make init
```

This will spin up a database, web worker, celery worker, and Redis broker and run your migrations.

You can then go to [localhost:8000](http://localhost:8000/) to view the app.

*Note: if you get an error, make sure you have a `.env.dev` file, or create one based on `.env.dev.example`.*

### Using the Makefile

You can run `make` to see other helper functions, and you can view the source
of the file in case you need to run any specific commands.

For example, you can run management commands in containers using the same method 
used in the `Makefile`. E.g.

```
docker-compose exec web python manage.py createsuperuser
```

## Installation - Native

You can also install/run the app directly on your OS using the instructions below.

Setup a virtualenv and install requirements
(this example uses [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):

```bash
mkvirtualenv Home -p python3.9
pip install -r requirements.txt
```

## Set up database

*If you are using Docker you can skip these steps.*

Create a database named `Home`.

```
createdb Home
```

Create database tables:

```
./manage.py migrate
```

## Running server

**Docker:**

```bash
make start
```

**Native:**

```bash
./manage.py runserver
```

## Building front-end

To build JavaScript and CSS files, first install npm packages:

**Docker:**

```bash
make npm-install
```

**Native:**

```bash
npm install
```

Then build (and watch for changes locally):

**Docker:**

```bash
make npm-watch
```

**Native:**

```bash
npm run dev-watch
```

## Running Celery

Celery can be used to run background tasks. If you use Docker it will start automatically.

You can run it using:

```bash
celery -A Home worker -l INFO
```

Or with celery beat (for scheduled tasks):

```bash
celery -A Home worker -l INFO -B
```

## Google Authentication Setup

To setup Google Authentication, follow the [instructions here](https://django-allauth.readthedocs.io/en/latest/providers.html#google).

## Running Tests

To run tests:

**Docker:**

```bash
make test
```

**Native:**

```bash
./manage.py test
```

Or to test a specific app/module:

**Docker:**

```bash
docker-compose exec web python manage.py test apps.utils.tests.test_slugs
```

**Native:**

```bash
./manage.py test apps.utils.tests.test_slugs
```

On Linux-based systems you can watch for changes using the following:


**Docker:**

```bash
find . -name '*.py' | entr docker-compose exec web python manage.py test apps.utils.tests.test_slugs
```

**Native:**

```bash
find . -name '*.py' | entr python ./manage.py test apps.utils.tests.test_slugs
```
>>>>>>> f12da3d3b6d76f7b5379812d3f9f2043121c6606
