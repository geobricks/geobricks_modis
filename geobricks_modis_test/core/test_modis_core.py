import unittest
from geobricks_modis.core import modis_core as c


class GeobricksModisTest(unittest.TestCase):

    def test_get_modis_product_table(self):
        products = c.get_modis_product_table()
        self.assertEqual(len(products), 68)

    def test_list_products(self):
        products = c.list_products()
        self.assertEqual(len(products), 427)

    def test_list_years(self):
        years = c.list_years('MOD13A2')
        self.assertEqual(len(years), 16)

    def test_list_days(self):
        days = c.list_days('MOD13A2', '2010')
        self.assertEqual(len(days), 23)

    def test_list_layers(self):
        layers = c.list_layers('MOD13A2', 2014, '001')
        self.assertEqual(len(layers), 286)
        layers = c.list_layers('MYD11C1', 2014, '001')
        self.assertEqual(len(layers), 1)

    def test_list_layers_subset(self):
        layers = c.list_layers_subset('MOD13A2', '2010', '001', 5, 7, 3, 9)
        self.assertEqual(len(layers), 5)
        layers = c.list_layers_subset('MYD11C1', '2010', '001', 5, 7, 3, 9)
        self.assertEqual(len(layers), 1)

    def test_list_layers_countries_subset(self):
        layers = c.list_layers_countries_subset('MOD13A2', '2010', '001', '8,IT,fra')
        self.assertEqual(len(layers), 12)

    def test_list_layers_countries_subset_gaul(self):
        layers = c.list_layers_countries_subset('MOD13A2', '2010', '001', '8,1')
        self.assertEqual(len(layers), 8)

    def test_list_layers_countries_subset_iso2(self):
        layers = c.list_layers_countries_subset_iso2('MOD13A2', '2010', '001', 'IT,FR')
        self.assertEqual(len(layers), 7)

    def test_list_layers_countries_subset_iso3(self):
        layers = c.list_layers_countries_subset_iso3('MOD13A2', '2010', '001', 'ITA,FRA')
        self.assertEqual(len(layers), 7)

    def test_day_of_the_year_to_date(self):
        date = c.day_of_the_year_to_date('017', 2014)
        date_string = date.strftime("%Y-%m-%d %H:%M:%S").split(' ')[0]
        self.assertEqual(date_string, '2014-01-17')

    def test_list_countries(self):
        out = c.list_countries()
        self.assertEquals(len(out), 277)

if __name__ == '__main__':
    unittest.main()
