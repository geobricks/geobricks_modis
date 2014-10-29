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
Please check the [examples](https://github.com/geobricks/geobricks_modis/tree/master/examples) section for further details.
Installation
------------
The plug-in is distributed through PyPi and can be installed by typing the following command in the console:
```
pip install geobricksmodis
```
