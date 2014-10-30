Geobricks MODIS
===============
The MODIS plug-in for the Geobricks downloader provides methods to filter the MODIS FTP based on the product code, the datetime and the geographic area. As istance, the following represents the list of MODIS tiles covering Angola for the MOD13Q1 product on January 1st 2002:
```json
[
    {
        "file_name": "MOD13Q1.A2012001.h19v09.005.2012019104600.hdf",
        "size": "196646026",
        "file_path": "ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2012/001/MOD13Q1.A2012001.h19v09.005.2012019104600.hdf",
        "label": "H 19, V 09 (196.65 MB)"
    },
    {
        "file_name": "MOD13Q1.A2012001.h19v10.005.2012019104816.hdf",
        "size": "192004771",
        "file_path": "ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2012/001/MOD13Q1.A2012001.h19v10.005.2012019104816.hdf",
        "label": "H 19, V 10 (192.0 MB)"
    },
    {
        "file_name": "MOD13Q1.A2012001.h20v09.005.2012019103646.hdf",
        "size": "217254791",
        "file_path": "ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2012/001/MOD13Q1.A2012001.h20v09.005.2012019103646.hdf",
        "label": "H 20, V 09 (217.25 MB)"
    },
    {
        "file_name": "MOD13Q1.A2012001.h20v10.005.2012019104512.hdf",
        "size": "240262517",
        "file_path": "ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2012/001/MOD13Q1.A2012001.h20v10.005.2012019104512.hdf",
        "label": "H 20, V 10 (240.26 MB)"
    }
]
```
Installation
============
The plug-in is distributed through PyPi and can be installed by typing the following command in the console:
```
pip install geobricksmodis
```
Examples
========
Get products list
-----------------------
```python
from geobricks_modis.core import modis_core as c


products = c.list_products()
```
Get available years
-------------------
```python
from geobricks_modis.core import modis_core as c


years = c.list_years('MOD13A2')
```
Get available days
------------------
```python
from geobricks_modis.core import modis_core as c


days = c.list_days('MOD13A2', '2010')
```
Get available layers
--------------------
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers('MOD13A2', '2010', '001')
```
Get a subset of layers
----------------------
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_subset('MOD13A2', '2010', '001', 5, 7, 3, 9)
```
Get layers by country GAUL code
-------------------------------
This method retrieves the list of MODIS tiles for the given product, year and day, filtered by the country GAUL code. The example below gets the layers of Afghanistan (`1`) and Angola (`8`).
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_countries_subset_gaul('MOD13A2', '2010', '001', '8,1')
```
Get layers by country ISO2 code
-------------------------------
This method retrieves the list of MODIS tiles for the given product, year and day, filtered by the country ISO2 code. The example below gets the layers of Italy (`it`) and France (`FR`). Codes can be either lower or upper case.
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_countries_subset_iso2('MOD13A2', '2010', '001', 'it,FR')
```
Get layers by country ISO3 code
-------------------------------
This method retrieves the list of MODIS tiles for the given product, year and day, filtered by the country ISO3 code. The example below gets the layers of Italy (`ita`) and France (`FRA`). Codes can be either lower or upper case.
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_countries_subset_iso3('MOD13A2', '2010', '001', 'ITA,fra')
```
Get layers by country code
-------------------------------
The previous methods can be used in combined way: layers can be filtered by means of GAUL (`8`), ISO3 (`ITA`) and ISO2 (`fr`) codes. 
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_countries_subset('MOD13A2', '2010', '001', '8,ITA,fr')
```
