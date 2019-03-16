from datetime import datetime, timedelta
from pytz import timezone
import argparse
from timezonefinder import TimezoneFinder
from icalendar import Calendar, Event

def parseargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file", help="path of input file (ics)")
	parser.add_argument("out_file", help="path of output file (ics)")
	parser.add_argument("--tags", help="eg #GBR #YOUNGGUNS")
	args = parser.parse_args()
	return args

def time_convert(latitude, longitude, t, tf):
	""" 
	Latitude and longitude are used to determine timezone. The correct day local time can then be determined.
	"""
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
	for component in c.walk():
		if component.name == "VEVENT":
			latitude = float(component.get('geo').to_ical().split(";")[0])
			longitude = float(component.get('geo').to_ical().split(";")[1])
			component['location'] = " ".join(component.get('geo').to_ical().split(";"))
			component['description'] = component.get('url') + " " + args.tags
			component['dtstart'] = time_convert(latitude, longitude,component['dtstart'].to_ical().decode('utf8') , tf)
			component['dtend'] = component['dtstart']
  

if __name__ == '__main__':
	args = parseargs()
	run(args)
	