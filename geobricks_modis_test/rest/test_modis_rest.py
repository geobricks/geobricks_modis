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
        response = self.tester.post('/modis/unittest/',
                                    content_type='application/json',
                                    data=json.dumps({
                                        'username': 'sheldon@cooper.com',
                                        'password': 'howimetyourmother'
                                    }))
        out = json.loads(response.data)
        print out