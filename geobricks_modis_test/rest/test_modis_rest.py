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