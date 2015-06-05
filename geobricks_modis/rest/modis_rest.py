import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_modis.core import modis_core as m
from geobricks_modis.resources.modis_schema import schema


modis = Blueprint('modis', __name__)


@modis.route('/discovery/')
@cross_origin(origins='*', headers=['Content-Type'])
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    return Response(json.dumps(schema), content_type='application/json; charset=utf-8')


@modis.route('/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_products_service():
    """
    List available products.
    @return: List of code/label objects.
    """
    out = m.get_modis_product_table()
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_years_service(product_name):
    """
    List available years for the given product.
    @param product_name: MODIS product code.
    @type product_name: str
    @return: List of code/label objects.
    """
    out = m.list_years(product_name)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_days_service(product_name, year):
    """
    List available days for the given product and year.
    @param product_name: MODIS product code.
    @type product_name: str
    @param year: Year.
    @type year: str|int
    @return: List of code/label objects.
    """
    out = m.list_days(product_name, year)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_layers_service(product_name, year, day):
    """
    List available layers for the given product, year and day.
    @param product_name: MODIS product code.
    @type product_name: str
    @param year: Year.
    @type year: str|int
    @param day: Day.
    @type day: str|int
    @return: List of code/label objects.
    """
    out = m.list_layers(product_name, year, day)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/<from_h>/<to_h>/<from_v>/<to_v>/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_layers_subset_service(product_name, year, day, from_h, to_h, from_v, to_v):
    """
    List available layers for the given filters.
    @type product_name: str
    @param year: Year.
    @type year: str|int
    @param day: Day.
    @type day: str|int
    @param from_h: Starting horizontal index of the range.
    @type from_h: str | int
    @param to_h: Ending horizontal index of the range.
    @type to_h: str | int
    @param from_v: Starting vertical index of the range.
    @type from_v: str | int
    @param to_v: Ending vertical index of the range.
    @type to_v: str | int
    @return: List of code/label objects.
    """
    out = m.list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/<product_name>/<year>/<day>/<countries>/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_layers_countries_subset_service(product_name, year, day, countries):
    """
    List available layers for the given filters.
    @param year: Year.
    @type year: str|int
    @param day: Day.
    @type day: str|int
    @param countries: Comma separated list of country code: GAUL, ISO2 or ISO3.
    @type countries: str
    @return: List of code/label objects.
    """
    out = m.list_layers_countries_subset(product_name, year, day, countries)
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@modis.route('/countries/')
@cross_origin(origins='*', headers=['Content-Type'])
def list_countries():
    """
    List available countries.
    @return: List of code/label objects.
    """
    out = m.list_countries()
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')
