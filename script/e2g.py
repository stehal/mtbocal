# -*- coding: utf-8 -*-

import sys,re,json,chardet
from datetime import datetime, timedelta
from pytz import timezone, utc
import argparse
from timezonefinder import TimezoneFinder
from icalendar import Calendar, Event
from pygeocoder import Geocoder, GeocoderError
import pycountry
from geopy import geocoders


def name2ioc():
	with open("./data/country-codes_json.json",encoding="utf-8") as f:
		json_string = f.read().encode("utf-8")
		parsed_json = json.loads(json_string)
		convert = {}
		for j in parsed_json:
			convert[j["CLDR display name"]] =j["IOC"]
		return convert

def parseargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file", help="path of input file (ics)")
	parser.add_argument("out_file", help="path of output file (ics)")
	parser.add_argument("api_key", help="google api key for geocoding")
	parser.add_argument("--tags", help="eg #YGWS #WMS #CZE #IOF")
	args = parser.parse_args()
	return args

def time_convert(latitude, longitude, t, tf):
	""" 
	Latitude and longitude are used to determine timezone. The correct day local time can then be determined.
	"""
	if len(t) == 8:
		return t
	f = utc.localize(datetime.strptime(t, '%Y%m%dT%H%M%SZ')).astimezone(timezone(tf.timezone_at( lat=latitude, lng=longitude)))
	
	return f.strftime('%Y%m%d')

def end_time_convert(latitude, longitude, t, tf):
	if len(t) == 8:
		return t
	f = utc.localize(datetime.strptime(t, '%Y%m%dT%H%M%SZ')).astimezone(timezone(tf.timezone_at( lat=latitude, lng=longitude)))
	if f.hour != 0 or f.minute != 0 or f.second != 0:
		f += timedelta(days= 1)
	return f.strftime('%Y%m%d')

def run(args):
	out = open(args.out_file, "w", encoding='utf8')
	rawdata = open(args.in_file, 'rb').read()
	result = chardet.detect(rawdata)
	charenc = result['encoding']
	calendar = Calendar.from_ical(open(args.in_file, encoding=charenc).read())

	tags = args.tags
	if not tags:
		tags = ""
	googleify(calendar, tags, args.api_key, name2ioc())
	out.write(c.to_ical().decode('UTF-8').replace('\r\n', '\n').strip())

def googleify(c, tags, api_key, n2i):
	"""
	Converts eventor geo to location which is used by google. Eventor supplied url and tags (supplied as args) are used to create description.
	Events are converted to all day events to avoid confusion caused by different time zones. 
	"""
	tf = TimezoneFinder()

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
				component['description'] = description + " " + url + " " + tags + " " + country_tag(latitude, longitude, api_key, n2i)
				component['location'] = " ".join(geo.to_ical().split(";"))
			else:
				component['description'] = description + " " + url + " " + tags
			component['dtstart'] = time_convert(latitude, longitude, component['dtstart'].to_ical().decode('utf8') , tf)
			
			if component.get('dtend'):
				component['dtend'] = end_time_convert(latitude, longitude, component['dtend'].to_ical().decode('utf8') , tf)

def geo2country(latitude, longitude, api_key):
	geocoder = Geocoder(api_key)
	try:
		results =  geocoder.reverse_geocode(latitude, longitude)
		return results.country
	except GeocoderError as err:
		print("Error reverse geocoding: ", err, latitude, longitude)
		return None

def loc2geo(address, api_key):
	geolocator = geocoders.GoogleV3(api_key=api_key)
	return geolocator.geocode(address)

def geo2loc(point):
	geolocator = geocoders.Nominatim(user_agent='elah.nevets@gmail.com')
	return geolocator.reverse(point)


def country_tag(latitude, longitude, api_key, n2i):
	country=n2i.get((geo2country(latitude, longitude, api_key)))
	if not country:
		return ""
	return '#' + country 
		
if __name__ == '__main__':
	args = parseargs()
	run(args)	