import urllib
import datetime
import json
import os
import time
from ftplib import FTP
from bs4 import BeautifulSoup
from geobricks_modis.config.gaul2modis import countries_map
from geobricks_modis.config.modis_config import config as conf
from geobricks_modis.config.modis_temporal_resolutions import resolutions


def get_modis_product_table():
    """
    Parse the MODIS product list.
    @return: Dictionary with the MODIS product list.
    """
    data = None
    try:
        with open('../resources/json/modis_product_table.json') as product_table:
            data = json.load(product_table)
    except ValueError:
        data = create_modis_product_table_file()
    except IOError:
        data = create_modis_product_table_file()
    return data


def create_modis_product_table_file():
    # sock = urllib.urlopen('https://lpdaac.usgs.gov/products/modis_products_table')
    sock = urllib.urlopen('http://fenixapps.fao.org/repository/MODIS_PRODUCT_TABLE/index.html')
    html = sock.read()
    sock.close()
    soup = BeautifulSoup(html)
    tables = soup.findAll('table')
    if len(tables) == 0:
        return list_products()
    else:
        table = tables[len(tables) - 1]
        tbody = table.find('tbody')
        trs = tbody.findAll('tr')
        products = []
        keys = ['code', 'platform', 'modis_data_product', 'raster_type', 'spatial_resolution']
        for tr in trs:
            p = {}
            counter = 0
            tds = tr.findAll('td')
            for td in tds:
                text = ''.join(td.find(text=True)).strip().replace('\n', '')
                if counter == 0:
                    text = td.find('a').find(text=True)
                try:
                    p[keys[counter]] = text
                    counter += 1
                except IndexError:
                    pass
            try:
                p['temporal_resolution'] = resolutions[p['code']]
            except KeyError:
                pass
            p['label'] = p['code'] + ': ' + p['modis_data_product'] + ' (' + p['spatial_resolution'] + ')'
            products.append(p)
        try:
            with open('../resources/json/modis_product_table.json', 'w+') as product_table:
                json.dump(products, product_table)
        except IOError:
            if not os.path.exists('../resources/json'):
                os.makedirs('../resources/json')
            with open('../resources/json/modis_product_table.json', 'w+') as product_table:
                json.dump(products, product_table)
        return products


def list_products():
    """
    List all the available MODIS products.
    @return: An array of code/label objects.
    """
    if conf['source']['type'] == 'FTP':
        ftp = FTP(conf['source']['ftp']['base_url'])
        ftp.login()
        ftp.cwd(conf['source']['ftp']['data_dir'])
        l = ftp.nlst()
        l.sort()
        out = []
        for s in l:
            out.append({'code': s, 'label': s})
        ftp.quit()
        return out


def list_years(product_name):
    """
    List all the available years for a given MODIS product.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @return: An array of code/label objects.
    """
    if conf['source']['type'] == 'FTP':
        ftp = FTP(conf['source']['ftp']['base_url'])
        ftp.login()
        ftp.cwd(conf['source']['ftp']['data_dir'])
        ftp.cwd(product_name.upper())
        l = ftp.nlst()
        l.sort(reverse=True)
        out = []
        for s in l:
            try:
                float(s)
                out.append({'code': s, 'label': s})
            except ValueError:
                pass
        ftp.quit()
        return out


def list_days(product_name, year):
    """
    List all the available days for a given MODIS product and year.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @return: An array of code/label objects.
    """
    year = year if type(year) is str else str(year)
    if conf['source']['type'] == 'FTP':
        ftp = FTP(conf['source']['ftp']['base_url'])
        ftp.login()
        ftp.cwd(conf['source']['ftp']['data_dir'])
        ftp.cwd(product_name.upper())
        ftp.cwd(year)
        l = ftp.nlst()
        l.sort()
        out = []
        for s in l:
            date = day_of_the_year_to_date(s, year).strftime('%d %B')
            out.append({'code': s, 'label': date})
        ftp.quit()
        return out


def get_raster_type(product_name):
    for p in get_modis_product_table():
        if p['code'] == product_name:
            return p['raster_type']


def list_layers(product_name, year, day):
    """
    List all the available layers for a given MODIS product, year and day.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, three digits, e.g. '017'
    @type day: str | int
    @return: An array of code/label/size objects.
    """
    raster_type = get_raster_type(product_name)
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    ftp = FTP(conf['source']['ftp']['base_url'])
    ftp.login()
    ftp.cwd(conf['source']['ftp']['data_dir'])
    ftp.cwd(product_name.upper())
    ftp.cwd(year)
    ftp.cwd(day)
    ls = []
    #ftp.retrlines('MLSD', ls.append)
    ftp.retrlines('LIST', ls.append)
    ftp.quit()
    out = []
    tmp_buffer = []

    #ADDED BY Z4K
    def iff( test_, then_, else_ ): # then_, else_ always get evaled so pls be atoms
        if test_:
            return then_
        else:
            return else_

    curr_year_fmt, prev_year_fmt, unified_fmt = '%b %d %H:%M', '%b %d  %Y', '%Y-%m-%d-%H:%M'

    def updatetuple( t, i, x ): # insert x into the ith field of tuple, t
        l = list( t )
        return tuple( l[:i] + [x] + l[i+1:] )

    def parsePrevYear( date ): return time.strptime( date, prev_year_fmt )
    def parseCurrYear( date ):
        datewith1900 = time.strptime( date, curr_year_fmt )
        currentYear  = time.gmtime()[0]
        return updatetuple( datewith1900, 0, currentYear )

    def dateParser( date ): return iff( ':' in date, parseCurrYear, parsePrevYear )
    def parseDate( date ):  return time.mktime( dateParser( date )( date ) )

    def displayDate( date ):
        date_struct, curr_struct = time.gmtime( date ), time.gmtime()
        date_year, curr_year = date_struct[0], curr_struct[0]
        year_fmt = iff( date_year == curr_year, curr_year_fmt, prev_year_fmt )
        return time.strftime( year_fmt, date_struct )

    R_MSK, W_MSK, X_MSK, Z_MSK =   4,   2,   1,   0
    R_STR, W_STR, X_STR, Z_STR = 'r', 'w', 'x', '-'

    def str2mode( str ):
        r, w, x = str[0] == R_STR,  str[1] == W_STR,  str[2] == X_STR
        return iff( r, R_MSK, Z_MSK ) | iff( w, W_MSK, Z_MSK ) | iff( x, X_MSK, Z_MSK )

    def mode2str( mode ):
        r, w, x = mode & R_MSK, mode & W_MSK, mode & X_MSK
        return iff( r, R_STR, Z_STR ) + iff( w, W_STR, Z_STR ) + iff( x, X_STR, Z_STR )

    def str2fullmode( str ):
        u, g, o = str[0:3], str[3:6], str[6:9]
        return str2mode( u ) << 6 | str2mode( g ) << 3 | str2mode( o )

    def fullmode2str( mode ):
        u, g, o = mode >> 6 & 0x7, mode >> 3 & 0x7, mode & 0x7
        return mode2str( u ) + mode2str( g ) + mode2str( o )

    def str2perm( str ):
        return str[0] == 'd', str[0] == 'l', str2fullmode( str[1:] )

    def perm2str( isdir, islink, mode ):
        return iff( isdir, 'd', iff( islink, 'l', '-' ) ) + fullmode2str( mode )

    def extract_info( line ):
        fullmode, links, owner, group, size, rest = line.split( None, 5 )
        isdir, islink, mode = str2perm( fullmode )
        dateStr, name = rest[:12], rest[13:]
        date = parseDate( dateStr )
        return {
            'name': name,
            'perms': fullmode,
            'isdir': isdir, 'islink': islink,
            'mode': mode, 'links': int( links ),
            'owner': owner, 'group': group,
            'size': int( size ),
            'datestr': dateStr, 'date': date
        }

    for line in ls:
        try:
            # start = line.index('Size=')
            # end = line.index(';', start)
            # size = line[start + len('Size='):end]
            # start = line.index(product_name.upper())
            # file_name = line[start:]
            info = extract_info(line)
            #print info
            size = info["size"]
            file_name = info["name"]
            if file_name not in tmp_buffer:
                tmp_buffer.append(file_name)
                file_path = 'ftp://' + conf['source']['ftp']['base_url'] + conf['source']['ftp']['data_dir']
                file_path += product_name.upper() + '/' + year + '/' + day + '/'
                #file_path += line[start:]
                file_path += file_name
                if raster_type == 'Tile':
                    h = file_name[2 + file_name.index('.h'):4 + file_name.index('.h')]
                    v = file_name[1 + file_name.index('v'):3 + file_name.index('v')]
                    label = 'H ' + h + ', V ' + v + ' (' + str(round((float(size) / 1000000), 2)) + ' MB)'
                else:
                    label = '(' + str(round((float(size) / 1000000), 2)) + ' MB)'
                row = {
                    'file_name': file_name,
                    'file_path': file_path,
                    'label': label,
                    'size': None
                }
                print row
                out.append(row)
        except ValueError:
            pass
    return out


def list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v):
    """
    List all the available layers for a given MODIS product, year and day.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, three digits, e.g. '017'
    @type day: str | int
    @param from_h: e.g. '05'
    @type from_h: str | int
    @param to_h: e.g. '05'
    @type to_h: str | int
    @param from_v: e.g. '05'
    @type from_v: str | int
    @param to_v: e.g. '05'
    @type to_v: str | int
    @return: An array of code/label/size objects.
    """
    raster_type = get_raster_type(product_name)
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    from_h = from_h if type(from_h) is str else str(from_h)
    to_h = to_h if type(to_h) is str else str(to_h)
    from_v = from_v if type(from_v) is str else str(from_v)
    to_v = to_v if type(to_v) is str else str(to_v)
    from_h = from_h if len(from_h) == 2 else '0' + from_h
    to_h = to_h if len(to_h) == 2 else '0' + to_h
    from_v = from_v if len(from_v) == 2 else '0' + from_v
    to_v = to_v if len(to_v) == 2 else '0' + to_v
    if conf['source']['type'] == 'FTP':
        ftp = FTP(conf['source']['ftp']['base_url'])
        ftp.login()
        ftp.cwd(conf['source']['ftp']['data_dir'])
        ftp.cwd(product_name.upper())
        ftp.cwd(year)
        ftp.cwd(day)
        ls = []
        #ftp.retrlines('MLSD', ls.append)
        ftp.retrlines('LIST', ls.append)
        ftp.quit()
        out = []
        tmp_buffer = []
        for line in ls:
            try:
                start = line.index('Size=')
                end = line.index(';', start)
                size = line[start + len('Size='):end]
                start = line.index(product_name.upper())
                file_name = line[start:]
                if file_name not in tmp_buffer:
                    tmp_buffer.append(file_name)
                    if raster_type == 'Tile':
                        if is_layer_in_the_range(file_name, from_h, to_h, from_v, to_v):
                            file_path = 'ftp://' + conf['source']['ftp']['base_url'] + conf['source']['ftp']['data_dir']
                            file_path += product_name.upper() + '/' + year + '/' + day + '/'
                            file_path += line[start:]
                            h = file_name[2 + file_name.index('.h'):4 + file_name.index('.h')]
                            v = file_name[1 + file_name.index('v'):3 + file_name.index('v')]
                            label = 'H ' + h + ', V ' + v + ' (' + str(round((float(size) / 1000000), 2)) + ' MB)'
                            out.append({
                                'file_name': file_name,
                                'file_path': file_path,
                                'label': label,
                                'size': None
                            })
                    else:
                        file_path = 'ftp://' + conf['source']['ftp']['base_url'] + conf['source']['ftp']['data_dir']
                        file_path += product_name.upper() + '/' + year + '/' + day + '/'
                        file_path += line[start:]
                        label = '(' + str(round((float(size) / 1000000), 2)) + ' MB)'
                        out.append({
                            'file_name': file_name,
                            'file_path': file_path,
                            'label': label,
                            'size': None
                        })
            except ValueError:
                pass
        return out


def is_layer_in_the_range(file_name, from_h, to_h, from_v, to_v):
    """
    Check whether a given file is in the specified range, according to its name.
    @param file_name: Name of the file.
    @type file_name: str
    @param from_h: Starting horizontal index of the range.
    @type from_h: str | int
    @param to_h: Ending horizontal index of the range.
    @type to_h: str | int
    @param from_v: Starting vertical index of the range.
    @type from_v: str | int
    @param to_v: Ending vertical index of the range.
    @type to_v: str | int
    @return: True if the file is in the range, false otherwise.
    """
    from_h = from_h if type(from_h) is str else str(from_h)
    to_h = to_h if type(to_h) is str else str(to_h)
    from_v = from_v if type(from_v) is str else str(from_v)
    to_v = to_v if type(to_v) is str else str(to_v)
    from_h = from_h if len(from_h) == 2 else '0' + from_h
    to_h = to_h if len(to_h) == 2 else '0' + to_h
    from_v = from_v if len(from_v) == 2 else '0' + from_v
    to_v = to_v if len(to_v) == 2 else '0' + to_v
    h_idx = len('.h') + file_name.index('.h')
    h = int(file_name[h_idx:(2 + h_idx)])
    v_idx = len(str(h) + 'v') + file_name.index(str(h) + 'v')
    v = int(file_name[v_idx:(2 + v_idx)])
    if int(from_h) <= h <= int(to_h) and int(from_v) <= v <= int(to_v):
        return True
    return False


def list_countries():
    return countries_map


def list_layers_countries_subset(product_name, year, day, countries):
    """
    Filter MODIS tiles based on the product, the year, the day and the country. Country codes can be in GAUL,
    ISO2, ISO3 or a combination of the previous.
    @param product_name: e.g. 'mod13q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, e.g. '047'
    @type day: str | int
    @param countries: Comma separated string containing country codes in GAUL, ISO2 or ISO3. e.g. '8,IT,FRA'
    @type countries: str | int
    @return: Array of objects.
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    out = []
    countries_list = countries.split(',')
    for country_code in countries_list:
        if country_code.isdigit():
            out += list_layers_countries_subset_gaul(product_name, year, day, country_code)
        elif len(country_code) == 2:
            out += list_layers_countries_subset_iso2(product_name, year, day, country_code.upper())
        else:
            out += list_layers_countries_subset_iso3(product_name, year, day, country_code.upper())
    return out


def list_layers_countries_subset_gaul(product_name, year, day, countries):
    """
    List all the available layers for a given MODIS product, year and day.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, e.g. '047'
    @type day: str | int
    @param countries: GAUL codes, comma separated e.g. '18,25,34'
    @type countries: str
    @return: An array of code/label/size objects.
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    countries_list = countries.split(',')
    out = []
    clean_out = []
    file_names_buffer = []
    for g2m in countries_map:
        if g2m['gaul_code'] in countries_list:
            from_h = g2m['from_h']
            to_h = g2m['to_h']
            from_v = g2m['from_v']
            to_v = g2m['to_v']
            tmp = list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
            out += tmp
    for tmp in out:
        if tmp['file_name'] not in file_names_buffer:
            file_names_buffer.append(tmp['file_name'])
            clean_out.append(tmp)
    return clean_out


def list_layers_countries_subset_iso2(product_name, year, day, countries):
    """
    List all the available layers for a given MODIS product, year and day.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @type product_name: str
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, three digits, e.g. '017'
    @type day: str | int
    @param countries: ISO2 codes, comma separated e.g. 'IT,FR'
    @type countries: str
    @return: An array of code/label/size objects.
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    countries_list = countries.split(',')
    out = []
    clean_out = []
    file_names_buffer = []
    for g2m in countries_map:
        if g2m['iso2_code'] in countries_list:
            from_h = g2m['from_h']
            to_h = g2m['to_h']
            from_v = g2m['from_v']
            to_v = g2m['to_v']
            tmp = list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
            out += tmp
    for tmp in out:
        if tmp['file_name'] not in file_names_buffer:
            file_names_buffer.append(tmp['file_name'])
            clean_out.append(tmp)
    return clean_out


def list_layers_countries_subset_iso3(product_name, year, day, countries):
    """
    List all the available layers for a given MODIS product, year and day.
    @param product_name: Code of MODIS product, e.g. 'MOD13Q1'
    @param year: e.g. '2010'
    @type year: str | int
    @param day: Day of the year, three digits, e.g. '017'
    @type day: str | int
    @param countries: ISO3 codes, comma separated e.g. 'ITA,FRA'
    @type countries: str
    @return: An array of code/label/size objects.
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    countries_list = countries.split(',')
    out = []
    clean_out = []
    file_names_buffer = []
    for g2m in countries_map:
        if g2m['iso3_code'] in countries_list:
            from_h = g2m['from_h']
            to_h = g2m['to_h']
            from_v = g2m['from_v']
            to_v = g2m['to_v']
            tmp = list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
            out += tmp
    for tmp in out:
        if tmp['file_name'] not in file_names_buffer:
            file_names_buffer.append(tmp['file_name'])
            clean_out.append(tmp)
    return clean_out


def day_of_the_year_to_date(day, year):
    """
    Convert a day of an year to a date
    @param day: day of the year
    @type day: str | int
    @param year: year of reference
    @type year: str | int
    @return: the date of the day/year i.e. "2012-01-20"
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    first_of_year = datetime.datetime(int(year), 1, 1).replace(month=1, day=1)
    ordinal = first_of_year.toordinal() - 1 + int(day)
    return datetime.date.fromordinal(ordinal)
__author__ = 'z4k'
