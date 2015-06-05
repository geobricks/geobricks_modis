import json
import unittest
from flask import Flask
from geobricks_modis.rest.modis_rest import modis


class GeobricksModisRestTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(modis, url_prefix='/modis')
        self.tester = self.app.test_client(self)

    def test_discovery(self):
        response = self.tester.get('/modis/discovery/', content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(out['name'], 'MODIS')
        self.assertEquals(out['type'], 'DATASOURCE')

    def test_list_products_service(self):
        response = self.tester.get('/modis/', content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(len(out), 68)

    def test_list_years_service(self):
        response = self.tester.get('/modis/MOD13A2/', content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(len(out), 16)