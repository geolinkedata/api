# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CkanResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(max_length=200, null=True, blank=True)),
                ('id_resource', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeonodeResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('layer', models.CharField(max_length=200, null=True)),
                ('workspace', models.CharField(max_length=50, null=True, blank=True)),
                ('map', models.CharField(max_length=300, null=True, blank=True)),
                ('output_wfs', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodeToken',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='node_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShapeFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shp', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/geolinkedata-data'), max_length=200, upload_to=b'shapes')),
                ('dbf', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/geolinkedata-data'), max_length=200, upload_to=b'shapes')),
                ('shx', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/geolinkedata-data'), max_length=200, upload_to=b'shapes')),
                ('prj', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/www/geolinkedata-data'), max_length=200, upload_to=b'shapes')),
                ('owner', models.ForeignKey(related_name='shapefiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TripleStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('format_file', models.CharField(max_length=9, null=True, choices=[(b'rdf', b'RDF/XML'), (b'n3', b'N3'), (b'nt', b'N-TRIPLES'), (b'ttl', b'TURTLE')])),
                ('target_store', models.CharField(default=b'GeoSparql', max_length=200, null=True)),
                ('feature_string', models.CharField(max_length=200, null=True, blank=True)),
                ('attribute', models.CharField(max_length=200, null=True, blank=True)),
                ('type_wkt', models.CharField(blank=True, max_length=12, null=True, choices=[(b'point', b'Point'), (b'polygon', b'Polygon'), (b'multipolygon', b'MultiPolygon')])),
                ('name', models.CharField(default=b'name', max_length=200, null=True, blank=True)),
                ('class_store', models.CharField(default=b'type', max_length=200, null=True, blank=True)),
                ('ns_prefix', models.CharField(max_length=200, null=True, blank=True)),
                ('ns_URI', models.CharField(default=b'http://geoknow.eu/geodata#', max_length=200, null=True, blank=True)),
                ('ontology_NS_prefix', models.CharField(default=b'geo', max_length=200, null=True, blank=True)),
                ('ontology_NS', models.CharField(default=b'http://www.opengis.net/ont/geosparql#', max_length=200, null=True, blank=True)),
                ('default_lang', models.CharField(blank=True, max_length=2, null=True, choices=[(b'en', b'English'), (b'it', b'Italian')])),
                ('ignore', models.CharField(max_length=200, null=True, blank=True)),
                ('source_RS', models.CharField(max_length=200, null=True, blank=True)),
                ('target_RS', models.CharField(max_length=200, null=True, blank=True)),
                ('input_file', models.CharField(max_length=400, null=True, blank=True)),
                ('output_file', models.FileField(max_length=200, null=True, upload_to=b'/tmp/triple-stores', blank=True)),
                ('owner', models.ForeignKey(related_name='triplestores', to=settings.AUTH_USER_MODEL)),
                ('shp', models.ManyToManyField(to='api.ShapeFile')),
            ],
        ),
        migrations.CreateModel(
            name='UserDataLoadedEvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('loaded', models.BooleanField()),
                ('created', models.DateTimeField()),
                ('user', models.ForeignKey(related_name='user_data_loaded', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='geonoderesource',
            name='shp',
            field=models.ForeignKey(to='api.ShapeFile'),
        ),
        migrations.AddField(
            model_name='ckanresource',
            name='shp',
            field=models.ForeignKey(to='api.ShapeFile'),
        ),
    ]
