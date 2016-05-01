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

.. code-block:: django

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

You can edit your API specification using the Swagger Editor GUI. Follow this commands below

.. code-block:: console

    npm install -g http-server
    wget https://github.com/swagger-api/swagger-editor/releases/download/v2.9.8/swagger-editor.zip
    unzip swagger-editor.zip
    http-server swagger-editor 

Then you can open the `API console`_ at the local url.

.. _API console: http://localhost:8080/


  
  
  
  
  
  