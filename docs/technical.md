# Technical Documentation

## Platform
Google forms is used for submission of single events.

Google calendar is used for event calendar.

## Plugin
A free version of [Event-O-Matic](https://amplifiedlabs.zendesk.com/hc/en-us/categories/202878748-Event-O-Matic) 
plugin is used to automatically create calendar events on 
form submission.

## Customization
`e2g.py` script is used to convert eventor exported ical:

* Google ignores `GEO` so we add latitude and longitude to `LOCATION` instead
* Create country tags based on location. [IOC country codes](https://en.wikipedia.org/wiki/List_of_IOC_country_codes) are added eg #AUT
* Convert all events to all-day events and adjust date to event's local time
* Google ignores `URL` field so we add it to `DESCRIPTION` instead.

## Embed in a web page
Use this code to embed this calendar in a web page:
```
<iframe src="https://calendar.google.com/calendar/embed?showTz=0&amp;mode=AGENDA&amp;height=600&amp;wkst=2&amp;bgcolor=%2333cc00&amp;src=cktpr9p08or12g0820g83kce0o%40group.calendar.google.com&amp;color=%23691426&amp;ctz=Europe%2FStockholm" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
```

## Import log
* 2020-01-18 GER 2020 races imported (with some effort)
* 2020-01-?? NOR 2020 race imported (despite wrong geo ref)
* 2019-11-30 Races for 2020 SWE, IOF, AUS and POR imported
* 2019-08-11 Races import from Sweden fixture list
* 2019-07-06 Races import from Latvia, Sweden, Australia, IOF, Switzerland and Portugal fixture lists
* 2019-03-19 Races from Latvian fixture list, though only one race imported - why aren't Riga races in the Latvian fixture list for example?
* 2019-03-18 Races from [Portuguese calendar](http://www.orioasis.pt/oasis/shortcut.php?&action=shortcut_events_all_info&calendarid=59%2C6%2C17%2C16%2C18%2C30%2C19%2C32%2C36%2C37%2C52%2C79%2C69%2C85%2C&disciplinid=2&country_code=PT&quantity=20&interval=calend&view_type=list&show_past_events=on&date_start=2019-03-11&col_name=on&col_place=on&col_type=on&col_org=on&col_date=on&col_options=on&task=export&)
* 2019-03-17 Races from Swedish event calendar (eventor)
* 2019-03-17 Races from Australian event calendar (eventor)
* 2019-03-17 Races from IOF event calendar (eventor)
* 2019-03-17 Races from [Swiss event calendar](https://www.o-l.ch/cgi-bin/fixtures?&year=2019&kind=2) 
