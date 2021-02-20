import unittest, sys, e2g
from timezonefinder import TimezoneFinder

class TestMethods(unittest.TestCase):
    API_KEY = 'secret'

    def testLoc2Geo(self):
        location = e2g.loc2geo('Sydney, Australia', self.API_KEY)
        self.assertEqual(location.latitude, -33.8688197)
        self.assertEqual(location.longitude, 151.2092955)
    
    def testGeo2Loc(self):
        location = e2g.geo2loc('-33.8688197, 151.2092955')
        self.assertEqual(location.raw['address']['country'], 'Australia')

    def testGeo2Country(self):
        self.assertEqual(e2g.geo2country(-33.8688197, 151.2092955, self.API_KEY), 'Australia')
    

    def testGeoToCountry(self):
        self.assertEqual(e2g.geo2country(-37.81,144.96, self.API_KEY), 'Australia')

    def testGeoToTag(self):
        self.assertEqual(e2g.country_tag(-37.81,144.96, self.API_KEY,e2g.name2ioc()), '#AUS')

    def testNameToIOC(self):
        self.assertEqual(e2g.name2ioc().get("Switzerland"), 'SUI')

    def testTimeConvertLocation(self):
        t = "20210916T140000Z"
        tf = TimezoneFinder()
        latitude = -32.9255093538619
        longitude = 151.561411089668
        self.assertEqual(e2g.time_convert(latitude, longitude, t, tf), '20210917')

    def testTimeConvertLocationNewcastle(self):
        t = "20210918T140000Z"
        tf = TimezoneFinder()
        latitude = -32.9255093538619
        longitude = 151.561411089668
        self.assertEqual(e2g.time_convert(latitude, longitude, t, tf), '20210919')

    def testTimeConvertDst(self):
        t = "20190822T220000Z"
        tf = TimezoneFinder()
        latitude = 59.36142
        longitude = 18.061
        self.assertEqual(e2g.time_convert(latitude, longitude, t, tf), '20190823')

    def testTimeConvert(self):
        t = "20190122T220000Z"
        tf = TimezoneFinder()
        latitude = 59.36142
        longitude = 18.061
        self.assertEqual(e2g.time_convert(latitude, longitude, t, tf), '20190122')

    def testEndTimeConvert(self):
        t = "20190822T220000Z"
        tf = TimezoneFinder()
        latitude = 59.36142
        longitude = 18.061
        self.assertEqual(e2g.end_time_convert(latitude, longitude, t, tf), '20190823')
		
TestMethods.API_KEY = sys.argv.pop()
unittest.main()
