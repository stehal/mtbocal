# -*- coding: utf-8 -*-

import unittest,sys,re,json,chardet
from datetime import datetime, timedelta
import pytz
from pytz import timezone
import argparse
from timezonefinder import TimezoneFinder
from icalendar import Calendar, Event
from pygeocoder import Geocoder
import pycountry

def name2ioc():
	with open("./data/country-codes_json.json",encoding="utf-8") as f:
		json_string = f.read()
		parsed_json = json.loads(json_string,encoding="utf-8")
		convert = {}
		for j in parsed_json:
			convert[j["CLDR display name"]] =j["IOC"]
		return convert

def parseargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file", help="path of input file (ics)")
	parser.add_argument("out_file", help="path of output file (ics)")
	parser.add_argument("api_key", help="google api key for geocoding")
	parser.add_argument("--tags", help="eg #YGWS #WMS")
	args = parser.parse_args()
	return args

def time_convert(latitude, longitude, t, tf):
	""" 
	Latitude and longitude are used to determine timezone. The correct day local time can then be determined.
	"""
	if len(t) == 8:
		return t
	f = pytz.utc.localize(datetime.strptime(t, '%Y%m%dT%H%M%SZ')).astimezone(timezone(tf.timezone_at( lat=latitude, lng=longitude)))
	
	return f.strftime('%Y%m%d')

def end_time_convert(latitude, longitude, t, tf):
	if len(t) == 8:
		return t
	f = pytz.utc.localize(datetime.strptime(t, '%Y%m%dT%H%M%SZ')).astimezone(timezone(tf.timezone_at( lat=latitude, lng=longitude)))
	if f.hour != 0 or f.minute != 0 or f.second != 0:
		f += timedelta(days= 1)
	return f.strftime('%Y%m%d')

def run(args):
	out = open(args.out_file, "w", encoding='utf8')
	rawdata = open(args.in_file, 'rb').read()
	result = chardet.detect(rawdata)
	charenc = result['encoding']
	c = Calendar.from_ical(open(args.in_file, encoding=charenc).read())
	tf = TimezoneFinder()
	googleify(c, args, tf, name2ioc())
	out.write(c.to_ical().decode('UTF-8').replace('\r\n', '\n').strip())

def googleify(c, args, tf, n2i):
	"""
	Converts eventor geo to location which is used by google. eventor supplied url and tags (supplied as args) are used to create description.
	Events are converted to all day events to avoid confusion caused by different time zones. 
	"""
	if not args.tags:
		args.tags = ""
	for component in c.walk():
		if component.name == "VEVENT":
			geo = component.get('geo')
			latitude = 59.33
			longitude = 18.07
			url = component.get('url')
			
			if not url:
				url = ""
			description = component.get("description")
			if not description:
				description = ""
			if geo:
				latitude = float(component.get('geo').to_ical().split(";")[0])
				longitude = float(component.get('geo').to_ical().split(";")[1])
				component['description'] = description + " " + url + " " + args.tags + " " + country_tag(latitude, longitude, args.api_key, n2i)
				component['location'] = " ".join(geo.to_ical().split(";"))
			else:
				component['description'] = description + " " + url + " " + args.tags
			component['dtstart'] = time_convert(latitude, longitude,component['dtstart'].to_ical().decode('utf8') , tf)
			component['dtend'] = end_time_convert(latitude, longitude, component['dtend'].to_ical().decode('utf8') , tf)
			

def geo2country(latitude, longitude, api_key):
	geocoder = Geocoder(api_key)
	results =  geocoder.reverse_geocode(latitude, longitude)
	return results.country


def country_tag(latitude, longitude, api_key, n2i):
	return '#' + n2i.get((geo2country(latitude, longitude, api_key))) 
	

class TestMethods(unittest.TestCase):
	API_KEY = 'secret'
	
	def testGeoToCountry(self):
		self.assertEqual( geo2country(-37.81,144.96, self.API_KEY), 'Australia')

	def testGeoToTag(self):
		self.assertEqual( country_tag(-37.81,144.96, self.API_KEY,name2ioc()), '#AUS')
	
	def testNameToIOC(self):
		self.assertEqual( name2ioc().get("Switzerland"), 'SUI')


	def testTimeConvertDst(self):
		t = "20190822T220000Z"
		tf = TimezoneFinder()
		latitude = 59.36142
		longitude = 18.061
		self.assertEqual( time_convert(latitude, longitude, t, tf), '20190823')

	def testTimeConvert(self):
		t = "20190122T220000Z"
		tf = TimezoneFinder()
		latitude = 59.36142
		longitude = 18.061
		self.assertEqual( time_convert(latitude, longitude, t, tf), '20190122')

	def testEndTimeConvert(self):
		t = "20190822T220000Z"
		tf = TimezoneFinder()
		latitude = 59.36142
		longitude = 18.061
		
		self.assertEqual( end_time_convert(latitude, longitude, t, tf), '20190823')

	
		
if __name__ == '__main__':
	#TestMethods.API_KEY = sys.argv.pop()
	#unittest.main()
	args = parseargs()
	run(args)	