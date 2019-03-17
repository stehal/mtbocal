# -*- coding: utf-8 -*-

import unittest,sys,re
from datetime import datetime, timedelta
from pytz import timezone
import argparse
from timezonefinder import TimezoneFinder
from icalendar import Calendar, Event
from pygeocoder import Geocoder
import pycountry

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
	e = datetime.strptime(t, '%Y%m%dT%H%M%SZ')
	e.astimezone(timezone(tf.timezone_at( lat=latitude, lng=longitude)))
	return e.strftime('%Y%m%d')

def run(args):
	out = open(args.out_file, "w")
	c = Calendar.from_ical(open(args.in_file).read())
	tf = TimezoneFinder()
	googleify(c, args, tf)
	out.write(c.to_ical().decode('UTF-8').replace('\r\n', '\n').strip())

def googleify(c, args, tf):
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
			if geo:
				latitude = float(component.get('geo').to_ical().split(";")[0])
				longitude = float(component.get('geo').to_ical().split(";")[1])
				component['description'] = component.get('url') + " " + args.tags + " " + country_tag(latitude, longitude, args.api_key)
				component['location'] = " ".join(geo.to_ical().split(";"))
			else:
				component['description'] = component.get('url') + " " + args.tags
			component['dtstart'] = time_convert(latitude, longitude,component['dtstart'].to_ical().decode('utf8') , tf)
			component['dtend'] = time_convert(latitude, longitude,component['dtend'].to_ical().decode('utf8') , tf)
			

def geo2country(latitude, longitude, api_key):
	geocoder = Geocoder(api_key)
	results =  geocoder.reverse_geocode(latitude, longitude)
	return results.country

def name2alpha3(cn_name):
	mapping = {country.name: country.alpha_3 for country in pycountry.countries}
	return mapping.get(cn_name)

def country_tag(latitude, longitude, api_key):
	return '#' + name2alpha3(geo2country(latitude, longitude, api_key)) 
	

class TestMethods(unittest.TestCase):
	API_KEY = 'secret'
	
	def testGeoToCountry(self):
		self.assertEqual( geo2country(-37.81,144.96, self.API_KEY), 'Australia')

	def testGeoToTag(self):
		self.assertEqual( country_tag(-37.81,144.96, self.API_KEY), '#AUS')
	
	def testNameToAlpha3(self):
		self.assertEqual( name2alpha3("Australia"), 'AUS')
		
if __name__ == '__main__':
	#TestMethods.API_KEY = sys.argv.pop()
	#unittest.main()
	args = parseargs()
	run(args)
	