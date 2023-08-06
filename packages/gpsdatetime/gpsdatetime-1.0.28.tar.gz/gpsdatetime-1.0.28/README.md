# gpsdatetime - Python GPS date/time management package

This is a python library for GNSS date/time transformations

## Usage

```python
import gpsdatetime as gpst

# init from current computer date/time
t = gpst.gpsdatetime()

# init from modified julian date 
t=gpst.gpsdatetime(mjd=54605.678)

# init from GPS week and second of week
t=gpst.gpsdatetime(wk=1400, wsec=600700)

# init from usual time elements
t=gpsdatetime(yyyy=2016, mon=1, dd=7, hh=3, min=5, sec=5)

# init from SINEX time string
t=gpsdatetime('16:004:46888')

# init from sinex date elements
t=gpst.gpsdatetime(yyyy=2016, doy=004, dsec=45677)

# init from iso time string
t=gpsdatetime('16:01:04T03:05:05Z')

# init from RINEX time string
t=gpsdatetime('18 10  9 12 20 45.00000')

y = t.yyyy
# y = 2020
iso_t = t.st_iso_epoch()
# 2020-10-01T12:00:26

print(t)
#Gpstime (version 2016-06-27)
#
#s1970 : 1480272707.601859
#YYYY_MM_DD : 2016/11/27  
#HH:MM:SS : 18:51:47.601858854
#GPS week : 1925
#Day of week : 0 (SUN)
#Second of week : 67907.601858854 
#Second of day : 67907.601858854  
#session : s
#Modified Julian Date : 57719.785968  
#Julian Date : 2457720.285968
#YYYY : 2016  DOY : 332
#GMST (dec. hour) : 23.337554
#GAST (dec. hour) : 23.337429
#Eq. of Equinoxes (dec. hour) : -0.000125

# output ISO time string 
s = t.st_iso_epoch()

# output pyephem (https://rhodesmill.org/pyephem/) time string 
s = t.st_pyephem_epoch()

# output SINEX time string
s = t.st_snx_epoch()

# add 5 seconds (or substract 2s) to gpsdatetime object t
t += 5
t -= 2

# test wether t is before t1 or not 
if t < t1:
    print('t before t1')
    
# duration between two time objects
t1 = gpst.gpsdatetime()
t2 = gpst.gpsdatetime()
Delta_t  = t2 - t1 # result in seconds

# set t object to current date at 0h00
t.day00()

# set t object to current week on sunday morning 0h00
t.wk00()

```

## Installation

Installation is accomplished from the command line.

user@desktop:~/gpsdatetime$ python3 setup.py install

The above command needs to be performed as root.

## licence

Copyright (C) 2014-2020, Jacques Beilin / ENSG-Geomatique

Distributed under terms of the CECILL-C licence.

