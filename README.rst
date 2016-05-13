=====================
Geolinkedata REST API
=====================

Geolinkedata REST API is a Django app to provide restful api for the project Geolinkedata.

Requirements
============

It requires geogig. Install it with:

.. code-block:: bash

  git clone https://github.com/locationtech/geogig.git

  cd geogig/src/parent

  mvn clean install

It is recommended to isolate the development in a virtual environment. For example you can use `pyenv`_ and install the plugin `pyenv-virtualenv`_ 

.. _pyenv-virtualenv: https://github.com/yyuu/pyenv-virtualenv

.. _pyenv: https://github.com/yyuu/pyenv

Development
===========

Create a virtual enviroment with the specified version of *python*:

.. code-block:: console

    pyenv install 2.7.11
    pyenv virtualenv 2.7.11 geolinkedata

Enter the virtual enviroment:

.. code-block:: console

    eval "$(pyenv init -)"
    pyenv shell geolinkedata
    pyenv activate geolinkedata

Firsty install the required *Django* version supported by `GeoNode`_ for compatibility.

.. _GeoNode:  http://geonode.org

.. code-block:: console

    pip install django==1.8.7
    pip freeze > requirements.txt

and install these python packages:
 
.. code-block:: bash

  pip install djangorestframework
  pip install djangorestframework-xml
  pip install django-oauth-toolkit
  pip install django-rest-swagger
  pip install geogig-py

Usage
-----

- Start a new Django project in the same virtual enviroment:

.. code-block:: console

    mkdir usage
    django-admin startproject tutorial .

- Install the api application from the repository:

.. code-block:: console

    pip install -e <LOCAL_PATH>/geolod-api

- Append required apps to ``INSTALLED_APPS`` var in your **settings.py**:
      
.. code-block:: python

      INSTALLED_APPS = (
        ...
        ...
        ...
        'rest_framework',
        'rest_framework_swagger',
        'provider',
        'oauth2_provider',       
        'api',
      )
 
- add these configurations in the same file:

.. code-block:: python
  
  STATIC_ROOT = os.path.join(BASE_DIR, "static")

  # dirs for upload and storing files
  UPLOAD_SHAPE = '/tmp/shapes'
  UPLOAD_TRIPLE_STORE = '/tmp/triple-stores'

  # rest_framework config
  REST_FRAMEWORK = {

      'DEFAULT_AUTHENTICATION_CLASSES':
          (
              'rest_framework.authentication.BasicAuthentication',
              'rest_framework.authentication.SessionAuthentication',
              'oauth2_provider.ext.rest_framework.OAuth2Authentication',
          ),
      'DEFAULT_RENDERER_CLASSES':
          (
              'rest_framework.renderers.BrowsableAPIRenderer',
              'rest_framework.renderers.JSONRenderer',
              'rest_framework_xml.renderers.XMLRenderer',
          ),
      'DEFAULT_PARSER_CLASSES':
          (
              'rest_framework_xml.parsers.XMLParser',
          ),
      'DEFAULT_THROTTLE_CLASSES':
          (
              'rest_framework.throttling.ScopedRateThrottle',
          ),
      'DEFAULT_THROTTLE_RATES':
          {
              'default': '10/minute',
              'download': '50/minute',
              'utility': '5/minute',
          }
  }

  # rest swagger config
  SWAGGER_SETTINGS = {
      "exclude_namespaces": [],
      "api_version": '1.0',
      "api_path": "/",
      "enabled_methods": [
          'get',
          'post',
          'put',
          'patch',
          'delete'
      ],
      "api_key": '',
      "is_authenticated": False,
      "is_superuser": False,
  }
  
- Create the api db tables:

.. code-block:: bash
    
    python manage.py syncdb

- Add api urls to urls.py of the tutorial application:

.. code-block:: python

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
      url(r'^admin/', include(admin.site.urls)),
      # api
      url(r'^', include('api.urls')),
      # api swaggerized
      url(r'^docs/', include('rest_framework_swagger.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  
- Start geogig with:

.. code-block:: bash
    
    geogig-gateway

- Run the command for serving static files:

.. code-block:: console
  
    cd usage
    python manage.py collectstatic  

- Start the local server at the default port 8000 with gunicorn:

.. code-block:: console

    gunicorn tutorial.wsgi

Usage of the tutorial application with docker
---------------------------------------------

Set up the shell with your docker machine:

.. code-block:: console

    eval $(docker-machine env default)

Rebuild the services with this command:

.. code-block:: console

    docker-compose build

Run the application on the container by executing:

.. code-block:: console

    docker-compose up

Add the first superuser for the application:

.. code-block:: console
    
    docker-compose run web python manage.py createsuperuser

Update database settings to Postgresql
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You are going to modify *settings.py* to let you change the database configuration:

.. code-block:: python

    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

where the **HOST** is the link to the *docker-compose.yml* database service:

.. code-block:: yml

    db:
      image: postgres

Secondly we should also add the package *psycopg2* as dependency:

.. code-block:: console

    pip install psycopg2
    pip freeze > requirements.txt

.. warning:: A trouble with previous versions of Django for migrations can be arised. If you encounter that in the error of such message 'django.db.utils.ProgrammingError: relation "auth_user" does not exist' then accomplish the actions below

In order to build new migrations for the api reusable app you can execute this commands below. Delete the old compiled files *.pyc*:

.. code-block:: console

    rm -rf api/*.pyc
    rm -rf api/migrations/*.pyc

Build new migrations for the api app:

.. code-block:: python

    python manage.py makemigrations api

After this migrations would be generated again.

Update the container
""""""""""""""""""""

Once you are ready with the projects then run the container from scratch:

.. code-block:: console

    docker-compose build
    docker-compose up

Then execute the **migrate** command in the api_tutorial django project inside the container:

.. code-block:: console

    docker-compose run web python manage.py migrate

Finally create a new superuser with the command:

.. code-block:: console

    docker-compose run web python manage.py createsuperuser

Test the api_tutorial application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can test the API urls with the user just created in the sqlite database. First of all it would be useful to make it to the docker environment. So let's get started with some basic variable's settings for the docker host ip address:

.. code-block:: bash

    DOCKER_HOST_IP=$(docker-machine ip)

In order to get the required cookies for making calls to the django site we can do the following request with `curl`_ or similar tools:

.. _curl: https://curl.haxx.se/

.. code-block:: bash

    curl -Ic - -XGET http://$DOCKER_HOST_IP:8000/admin/login/\?next\=/admin/

Each request has a response cookie named **csrftoken** that we want to catch and use it as a variable for the following requests: 

.. code-block:: bash

    CSRFTOKEN=$(curl -c - -XGET "http://${DOCKER_HOST_IP}:8000/admin/login/?next=/admin/" | grep csrftoken | cut -f 7)
    echo $CSRFTOKEN

.. note:: Alternatively you can use the commands below to extract the cookie:

  .. code-block:: bash
  
      curl -I -XGET http://$DOCKER_HOST_IP:8000/admin/login/?next=/admin/ -o /dev/null -c cookies.txt -s
      grep csrftoken cookies.txt | cut -f 7

Once we have all the elements to accomplish the login request then run the HTTP POST with the following command:

.. code-block:: bash

    curl -H "Cookie: csrftoken=$CSRFTOKEN" -d "username=admin&password=admin1234&csrfmiddlewaretoken=$CSRFTOKEN&next=/admin/" -XPOST http://$DOCKER_HOST_IP:8000/admin/login/ -v -c -

The response figures out two new cookies (*csrftoken*,*sessionid*) required for all authenticated calls to the web application urls. Embed the command above in a bash variable for automatically storing the cookies' value and then reuse them:

.. code-block:: bash
    
    # csrftoken cookie
    CSRFTOKEN_RESP=$(curl -H "Cookie: csrftoken=$CSRFTOKEN" -d "username=admin&password=admin1234&csrfmiddlewaretoken=$CSRFTOKEN&next=/admin/" -XPOST "http://${DOCKER_HOST_IP}:8000/admin/login/" -c - | grep csrftoken | cut -f 7)
    echo $CSRFTOKEN_RESP

.. code-block:: bash

    # sessionid cookie
    SESSIONID=$(curl -H "Cookie: csrftoken=$CSRFTOKEN" -d "username=admin&password=admin1234&csrfmiddlewaretoken=$CSRFTOKEN&next=/admin/" -XPOST "http://${DOCKER_HOST_IP}:8000/admin/login/" -c - | grep sessionid | cut -f 7)
    echo $SESSIONID

At this point we are able to making all authenticated calls to the APIs. For example you can query as an administrator all the users actually available in the django system:

.. code-block:: bash

    curl -H "Cookie: csrftoken=$CSRFTOKEN_RESP; sessionid=$SESSIONID" -XGET 'http://192.168.99.100:8000/v1/geo/users/?format=json' -v

e2e tests
^^^^^^^^^
Todo

Fetch the API model
-------------------

Install the utility `fetch-swagger-schema`_ 

.. _fetch-swagger-schema: https://github.com/signalfx/fetch-swagger-schema

.. code-block:: console

    npm install -g fetch-swagger-schema

Fetch and save schema as a json file:

.. code-block:: console

    fetch-swagger-schema http://127.0.0.1:8000/docs/api-docs/ api.json

How to document your API
------------------------

Actually the current fetched schema is based on specs 1.2 since **django-rest-swagger** doesn't support the new version 2.0. You can also edit your API specification with the latter version by using the Swagger Editor GUI. Follow this commands below

.. code-block:: console

    npm install -g http-server
    wget https://github.com/swagger-api/swagger-editor/releases/download/v2.9.8/swagger-editor.zip
    unzip swagger-editor.zip
    http-server swagger-editor 

Then you can open the `API console`_ at the local url.

.. _API console: http://localhost:8080/


  
  
  
  
  
  