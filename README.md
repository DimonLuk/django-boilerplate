# Django 3.0 boilerplate


Fully integrated react template lives here - link will be provided once the template is ready.


# Motivation, rules, contributions and etc.


Each new project requires some general set up before actual work can be started. This template tries to give you ability to skip this boring process and jump right away to coding important things. It contains everything that author thinks is essential for developing django applications and even a little bit more)) If you have any suggestions on how to improve this template feel free to open issues with your thoughts. If you want to contribute I'm more than welcome. There are no rules for issues and PRs, since the project is small and I do not expect a lot of activity here, but if there are a lot of active issues and PRs, then I guess I'll develop some rules, so if you're interested in the project's life, check this README from time to time.


# Very short guide


```bash
$ git clone https://github.com/DimonLuk/django-boilerplate my_project
$ cd my_project
$ rm -rf .git
$ git init
$ git commit -m "Initial commit"
$ pip install poetry
$ poetry install
$ poetry shell
$ export HELPERS_ALLOW_SUDO=1 # read Custom django management command section
$ python manage.py run_in_docker --noninteractive # Now your application is accessible at localhost:8000
# ATTENTION!!! Check dockerfile section, which explains how to add your code!!!!
```


# High level overview of repository content


Boilerplate will be described in the following order (from "higher" level to "lower" level)
- Environments
- Gitlab ci
- Custom django management commands
- docker-compose files
- Dockerfile
- Python packages
- Custom views
- Custom serializers
- Custom schemes
- Custom models
- Custom middlewares
- Custom settings
- Tests
- Other


# Environments


- local - you should use this environment when you do development on your machine. **docker-compose.yaml** runs it by default with `runserver_plus`
- testing - you should use this environment when you run tests on your machine or on pipeline. **docker-compose.test.yaml**
- dev - you can use for your alpha env, where all developers can play around with changes
- qa - you can use it for your pre-production environment or staging
- prod


# Gitlab ci


Contains test stage, which triggers on merge (pull) requests and when updates are pushed to master. Runs tests, collects coverage and test reports. No configuration is required, just upload project to gitlab.

Useful references:
- [Gitlab ci documentation](https://docs.gitlab.com/ee/ci/)
- [Gitlab integration with github](https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html)


# Custom django management commands


ATENTION!!! Some commands requires superuser permissions to work properly (
this is because of cache files generated by postgres and python inside docker are
assigned to root, so in order to remove them you have to be root). Check code if you
don't trust. To allow commands to be executed with root rights please set environmental
variable HELPERS_ALLOW_SUDO to true and enter your password (if you have it). If the
variable is not set to true commands will use current user's rights.

The whole `management` module is ignored by tests since there're not much things that
can have reasonable tests (and I'm lazy). If you decide to improve this, feel free
to add tests.

Available commands:
- `$ python manage.py run_in_docker` - starts postgresql, container in local mode with installed dependencies and set up environmental variables and drops you here. If you specify `--noninteractive` parameter it will start application in the background. Once the application is launched will be accessible at `locahost:8000`
- `$ python manage.py run_tests_in_docker` - starts postgresql, container in testing mode with installed dependencies and set up environmental variables and drops you here. If you specify `--noninteractive` parameter it will start running tests and attach you to generated logs.
- `$ python manage.py stop_docker` - simply stops everything that was launched by docker-compose
- `$ python manage.py clear_database` - clears cache for database that was created by docker-compose
- `$ python manage.py clear_pycache` - clears all **\_\_pycache\_\_** folders inside project's repository
- `$ python manage.py get_logs` - prints logs from containers created by docker-compose
- `$ python manage.py list_containers` - lists active containers created by docker-compose


# docker-compose files


Repository contains 2 docker-compose files. One for running tests and one for running development server. Both files contain PostgreSQL image, username: `postgres`, password: `user`, database data is stored in **\_\_postgres\_data\_\_** folder inside the template root (it's gitignored), so your data will be preserved during different sessions of development, just remove this folder in order to get a fresh database. Hot reloading is configured by using the whole template directory as docker-compose volume. **docker-compose.yaml** is responsible for running development server, the application uses port **80** inside docker container which mapped to port **8000** on host machine, so you can access your application at **localhost:8000**. **docker-compose.test.yaml** is responsible for running tests, port mappings are the same, but since there is no development server running during test sessions, so you won't be able to connect to anything.

# Dockerfile


ATTENTION!!! Don't forget to add your newly created directories to Dockerfile, otherwise they won't appear inside image which means your code will never be executed!! To add directory with your code, find the following string inside **Dockerfile**:
```Dockerfile
COPY LICENSE manage.py poetry.lock pyproject.toml startup-script.sh /code/
COPY database_scripts /code/database_scripts
COPY helpers /code/helpers
COPY project /code/project
```
After the last `COPY` statement add the following code:
```Dockerfile
COPY path/to/your/dir /code/path/to/your/dir
```
For example if you create new django application called my_app, then you'll have to add the following code:
```Dockerfile
COPY my_app /code/my_app
```

Dockerfile is based on python3.8-slim image. Accepts the following build arguments:
- MODE - required, can be one of **local**, **testing**, **dev**, **qa** and **prod** which corresponds to environment where container will be run this also corresponds to set of settings that will be chosen.
- POSTGRES\_NAME - required for **dev**, **qa** and **prod**, name of database
- POSTGRES\_USER - required for **dev**, **qa** and **prod**, username for postgres database
- POSTGRES\_PASSWORD - required for **dev**, **qa** and **prod**, password for postgres database
- POSTGRES\_HOST - required for **dev**, **qa** and **prod**, address of host machine where database is located
- POSTGRES\_PORT - required for **dev**, **qa** and **prod**,  I know that you know what this is
- SENTRY\_DSN - required for **dev**, **qa** and **prod**


# Python packages


All settings are separated into according blocks inside settings file. It's a good idea to follow this convention when you start developing of your project. To see actual settings, please check files inside **project/settings** folder. Project is already configured to register and authenticate users via django and django rest, also you can find autogenerated documentation for drf endpoints. Below you can find links to docs of installed packages.


### Production packages:


- [Django 3.0](https://docs.djangoproject.com/en/3.0/) 
- [Django REST framework](https://www.django-rest-framework.org/)
- [psycopg2-binary](https://www.psycopg.org/docs/). Binary version is used since it allows faster builds of docker containers
- [requests](https://pypi.org/project/requests/)
- [uvicorn](https://www.uvicorn.org/) - ASGI server for django 3
- [sentry-sdk](https://docs.sentry.io/platforms/python/django/) - you have to provide `SENTRY_DSN` argument when building docker images for dev, qa and prod
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) - currently all connections are allowed
- [drf_yasg](https://drf-yasg.readthedocs.io/en/stable/) - very, very cool package for building OpenAPI3.0 schemes for your RESTful APIs.
- [django-grappelli](https://grappelliproject.com/) - improved admin page for django
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) - cool package for controlling authentication and authorization.
- [django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/introduction.html) - documentation is not very good, to my mind, but this is the best package for RESTful authentication that I've found
- [djangorestframework-jwt](https://jpadilla.github.io/django-rest-framework-jwt/) - used by django-rest-auth
- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) - yes it's installed for production, because it can be used there to debug something. I haven't done this yet, but it seems reasonable for me. People who can access debug toolbar are specified inside `HELPERS` group of settings.


### Development packages:


- [pudb](https://github.com/inducer/pudb) - very cool debuger, to my opinion it's better then pdb or ipdb
- [django-extensions](https://django-extensions.readthedocs.io/en/latest/) - no comments, must have for any project. It's enabled only for test and local environments.
- [werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) - used by django-extensions' command `runserver_plus`. Useful thing, allows you to jump to debugger on stack trace
- [pytest](https://docs.pytest.org/en/latest/)
- [pytest-django](https://pytest-django.readthedocs.io/en/latest/)
- [pytest-pudb](https://pypi.org/project/pytest-pudb/)
- [pytest-cov](https://pypi.org/project/pytest-cov/)
- [snapshottest](https://github.com/syrusakbary/snapshottest) - very cool thing when you have to test your APIs or when you have to generate payload for another API
- [factory-boy](https://factoryboy.readthedocs.io/en/latest/) - very cool library when you have to create complicated objects to test them


# Custom views


In this section you can find views that are not from installed packages but were written especially for this template
- healthcheck - always opened for any user. Tries to access database if try is successful returns 200, otherwise returns 500


# Custom serializers


In this section you can find serializers that are not from installed packages but were written especially for this template
- MetaInfoInnerSerializerMixin - describes fields `version`, `timestamp` and `hash`, which fields are added to serializer depends on settings specified in `HELPERS` dict. This serializer is used to build another more complex serializer
- MetaInfoSerializerMixin - you should subclass this serializer in order to include fields described in MetaInfoInnerSerializerMixin to your serializer, but PAY ATTENTION, subclassing will only add descriptions of the fields to your serializer, actual values will be populated by according middleware if required settings are set in `HELPERS` dict. This serializer is used to create nice drf\_yasg scheme
- DetailSerializer - it's used to build drf\_yasg schemes


# Custom schemes


In this section you can find schemes that are not from installed packages but were written especially for this template
- scheme - class that builds decorator that you can use in order to create nice drf\_yasg schemes for your drf views
- healthcheck\_scheme - scheme for healthcheck view. You can use it as example


# Custom middleware


In this section you can find middleware that are not from installed packages but were written especially for this template
- ErrorFormatterMiddleware - middleware that catches errors (by error codes that you specify in `HELPERS` dict in the settings) and formats them to the following shape `{"detail": "Internal server error"}`.
- ResponseMetaInformationInHeadersMiddleware - middleware that adds meta information to responses headers. Currently supported meta information: application version, timestamp, response hash. By default it's included
- ResponseMetaInformationInJsonMiddleware - middleware that adds meta information to response json payload (if response contains such json payload). Currently supported meta information: application version, timestamp, response hash. By default it's included


Headers with meta info:
- H-Application-Version - controlled by `HELPERS` settings
- H-Timestamp - timestamp when the response has been created
- H-Response-Hash - unique md5 hash of the response


Json response with meta info:
```json
{
	...your data goes here
	"_meta_info": {
		"application_version": "controlled by HELPERS settings",
		"timestamp": "timestamp of the response",
		"hash": "unqiue md5 hash of the response"
	}
}
```


# Custom settings


Here you find documentation for `HELPERS` dict
- SELF\_STATIC\_SERVE - boolean, defaults to True. Defines if django should serve static files on **dev**, **qa** and **prod** environments
- PROJECT\_URL - string, defaults to `http://localhost:8000`. Defines project url which is then used to generate appropriate calls for schemes
- SWAGGER\_SCHEMES\_NO\_AUTH - boolean, defaults to True. Defines if swagger scheme (and ui) should be protected with authentication
- INCLUDE\_META\_INFO - boolean, default to True. Defines if meta info should be included
- META\_INFO\_IN\_JSON\_RESPONSE - boolean, defaults to True. Defines if meta info should be included into json response. Mutually exclusive with META\_INFO\_IN\_HEADERS
- META\_INFO\_IN\_HEADERS - boolean, defaults to False. Defines if meta info should be included into headers. Mutually exclusive with META\_INFO\_IN\_HEADERS
- META\_INFO - list of strings, available values: version, hash, timestamp, defaults to all available values. Defines what meta info should be included
- APPLICATION\_VERSION - string, defaults to 0.0.1
- ERROR\_CODES\_TO\_CATCH - list of integers, defaults to `[500]`. Defines which error codes should be formatted by ErrorFormatterMiddleware
- SUPERUSER\_EMAILS - list of strings. Defines which users can access debug toolbar in prod
- SUPERUSER\_USERNAMES - list of strings, defaults to `["admin"]`. The same as SUPERUSER\_EMAILS, but defines users via usernames. 
- ENABLE\_DEBUG\_TOOLBAR - boolean, defaults to True. Defines if debug toolbar is enabled


# Tests


Coverage is 100%, so your own code coverage won't be affected by the template helpers. Tests infrastructure (everything inside **tests** folders):
- classes - contains classes that are used to create different mocks
- fixtures - contains general fixtures, like application client
- helpers - contains tests for everything that lives inside **helpers** folder of the template


To add your tests create folder **tests/your\_project\_name**. Place here **\_\_init\_\_.py** files and create file **test\_whatever\_you\_want.py** and write your tests here. Try to keep all fixtures inside **fixtures** folders and use `factory-boy` library to create instances of django models for your tests


# Other


- Repo contains pre-commit hook that generates swagger.json to docs folder. It can be useful in some cases. To activate this hook run the following command in the root directory of template: `$ git config core.hooksPath .githooks`
- Also there's one django migration that create admin user with username: admin and password: admin.
