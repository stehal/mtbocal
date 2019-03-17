# Technical Documentation

Google forms is used for submission of single events.

Google calendar is used for event calendar.

A free version of [Event-O-Matic](https://amplifiedlabs.zendesk.com/hc/en-us/categories/202878748-Event-O-Matic) 
plugin is used to automatically create calendar events on 
form submission.

`e2g.py` script is used to convert eventor exported ical:

* Google ignores `GEO` so we add latitude and longitude to `LOCATION` instead
* Create country tags based on location, both country name and [ISO 3166 alpha-3 codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) are added eg #AUT #AUSTRIA
* Convert all events to all-day events and adjust date to event's local time
* Google ignores `URL` field so we add it to `DESCRIPTION` instead.

