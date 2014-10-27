import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_modis.core import modis_core as m


modis = Blueprint('modis', __name__)


@modis.route('/')
@cross_origin(origins='*')
def list_products_service():
    out = m.get_modis_product_table()
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/')
@cross_origin(origins='*')
def list_years_service(product_name):
    out = m.list_years(product_name)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/')
@cross_origin(origins='*')
def list_days_service(product_name, year):
    out = m.list_days(product_name, year)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/')
@cross_origin(origins='*')
def list_layers_service(product_name, year, day):
    out = m.list_layers(product_name, year, day)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/<from_h>/<to_h>/<from_v>/<to_v>/')
@cross_origin(origins='*')
def list_layers_subset_service(product_name, year, day, from_h, to_h, from_v, to_v):
    out = m.list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/<countries>/')
@cross_origin(origins='*')
def list_layers_countries_subset_service(product_name, year, day, countries):
    out = m.list_layers_countries_subset(product_name, year, day, countries)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/countries/')
@cross_origin(origins='*')
def list_countries():
    out = m.list_countries()
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')
