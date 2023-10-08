# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import pickle
import os.path
import e2g
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from icalendar import Calendar, Event
from timezonefinder import TimezoneFinder
from datetime import datetime
import datedelta

class Source:
    def __init__(self, url, tags, lat=59.33, lng=18.07):
        self.url = url
        self.tags=tags
        self.lat=lat
        self.lng=lng
   
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

today=datetime.today()
nextyear=today+datedelta.YEAR

startdate= today.strftime('%Y-%m-%d')
year=startdate[:4]
enddate=nextyear.strftime('%Y-%m-%d')
endyear=enddate[:4]

swe_url="https://eventor.orientering.se/Events/ExportICalendarEvents?startDate={}&endDate={}&organisations=1&classifications=International%2CChampionship%2CNational%2CRegional&disciplines=MountainBike&cancelled=False".format(startdate,enddate)
aus_url="https://eventor.orienteering.asn.au/Events/ExportICalendarEvents?startDate={}&endDate={}&organisations=1&classifications=International%2CChampionship%2CNational%2CRegional%2CLocal&disciplines=MountainBike&cancelled=False".format(startdate,enddate)
#esp_url= 'https://calendar.google.com/calendar/ical/hsa5ki3pjtpodh0efs48m3sifc%40group.calendar.google.com/public/basic.ics'
nor_url='https://eventor.orientering.no/Events/ExportICalendarEvents?startDate={}&endDate={}&organisations=2%2C1&disciplines=MountainBike&classifications=International%2CChampionship%2CNational%2CRegional%2CLocal&cancelled=False'.format(startdate,enddate)
iof_url_wre='https://eventor.orienteering.org/Events/ExportICalendarEvents?startDate={}&endDate={}&organisations=1&disciplines=MountainBike&mode=List&attributes=5&cancelled=False'.format(startdate,enddate)
iof_url_major='https://eventor.orienteering.org/Events/ExportICalendarEvents?startDate={}&endDate={}&organisations=1&disciplines=MountainBike&attributes=1%2C2%2C3%2C4%2C6&mode=List&cancelled=False'.format(startdate,enddate)
cze_url='https://calendar.google.com/calendar/ical/6vppph2la1prss8uor5irvl6t0%40group.calendar.google.com/public/basic.ics'
sui_url='https://www.o-l.ch/cgi-bin/fixtures?&year={}&kind=2&ics=1'.format(year)
sui_url_nextyear='https://www.o-l.ch/cgi-bin/fixtures?&year={}&kind=2&ics=1'.format(endyear)
por_url='http://www.orioasis.pt/oasis/shortcut.php?action=shortcut_events_all_info&view_type=list&calendarid%5B%5D=&disciplinid=2&view_type_radio=list&country_code=-1&region_code=&quantity=20&interval=calend&year={}&date_start={}&col_name=on&col_place=on&col_type=on&col_org=on&col_date=on&col_options=on&task=export'.format(year,startdate)
bul_url="https://calendar.google.com/calendar/ical/2e964f5pvknim1fbcvoqr4avco%40group.calendar.google.com/public/basic.ics"
hun_url="https://calendar.google.com/calendar/ical/fl0lsipnovbclj1ob5hgkva0ik%40group.calendar.google.com/public/basic.ics"

sources = []

sources.append(Source(aus_url,'#AUS',-33.0, 151.0))
sources.append(Source(swe_url,'#SWE'))
#sources.append(Source(esp_url,'#ESP',40.43, -3.70))
sources.append(Source(iof_url_wre,'#IOF #WRE'))
sources.append(Source(iof_url_major,'#IOF #MAJOR'))
sources.append(Source(nor_url,'#NOR',59.92,10.75))
sources.append(Source(cze_url,'#CZE',50.07,14.42))
sources.append(Source( sui_url,"#SUI",46.95, 7.43))
sources.append(Source( sui_url_nextyear,"#SUI",46.95, 7.43))
sources.append(Source( por_url,"#POR",38.73, -9.14))
sources.append(Source( bul_url,"#BUL",42.70,23.32))
sources.append(Source( hun_url,"#HUN",47.52,19.06))

def insertupdate(globcalid, service, event, icaluid):
    event_from_globcal=service.events().list(calendarId=globcalid, iCalUID=icaluid).execute().get('items', [])
    if len(event_from_globcal) == 1:
        print('   update')
        service.events().update(eventId=event_from_globcal[0]['id'], calendarId=globcalid, body=event).execute()
    else:
        print('   import')
        service.events().import_(calendarId=globcalid, body=event).execute()     
        
def date2googledate(date):
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

def tags2str(input_tag, country_tag):
    tags = set()
    for tag in tags:
        tags.add(input_tag)
    tags.add(country_tag)
    return ' '.join(tags)

def googleify(calendarFeed, tags, api_key, n2i, latitude, longitude):
    tf = TimezoneFinder()
    events=[]
    for component in calendarFeed.walk():
        try:
            if component.name == 'VEVENT':
                event = {}
                geo = component.get('geo')
                url = component.get('url')
                if not url:
                    url = ''
                description = component.get('description')
               
                location = component.get('location')
                if not description:
                    description = ""
                if geo:
                    latitude = float(component.get('geo').to_ical().split(";")[0])
                    longitude = float(component.get('geo').to_ical().split(";")[1])
                    event['description'] = description + " " + url + " " + tags2str(tags, e2g.country_tag(latitude, longitude, api_key, n2i))
                    event['location'] = " ".join(geo.to_ical().split(";"))
                elif location:
                    event['location'] = location
                    try:
                        location_geo = e2g.loc2geo(location, api_key)
                        if location_geo:
                            latitude = location_geo.latitude
                            longitude = location_geo.longitude
                            event['description'] = description + " " + url + " " + tags2str(tags, e2g.country_tag(latitude, longitude, api_key, n2i))
                    except BaseException:
                        event['description'] = description + " " + url + " " + tags 
                else:
                    event['description'] = description + " " + url + " " + tags
                event['start'] = {'date':date2googledate(e2g.time_convert(latitude, longitude, component['dtstart'].to_ical().decode('utf8') , tf))}
                if component.get('dtend'):
                    event['end'] = {'date':date2googledate(e2g.end_time_convert(latitude, longitude, component['dtend'].to_ical().decode('utf8') , tf))}
                else:
                    event['end']=event['start']
                event['iCalUID'] = str(component["uid"])
                event['summary'] = str(component['summary'])
                if event['start']['date'] >= startdate:
                    events.append(event)
        except AttributeError as err:
            print("Unexpected error:", err)

    return events

def check_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    creds = check_credentials()
    service = build('calendar', 'v3', credentials=creds)

    globalid = 'cktpr9p08or12g0820g83kce0o@group.calendar.google.com'
    testglobalid = 'a2t51pthvh6p2hjjjavaqdv39k@group.calendar.google.com'
    calendarid=globalid
    
    with open("api_key", "r") as f:
        api_key= f.read()

    ioc_names = e2g.name2ioc()
    for src in sources:
        print("importing from {}".format(src.url))
        r=requests.get(src.url, headers={'Accept': 'text/calendar'})
        events = googleify(Calendar.from_ical(r.content), src.tags, api_key, ioc_names, src.lat, src.lng)
        print("importing {} from {}".format(len(events), src.url))
        for event in events:
            print('   ' + event['summary'])
            insertupdate(calendarid, service, event, event['iCalUID'])

if __name__ == '__main__':
    main()