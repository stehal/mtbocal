# iCalendar

[iCalendar](https://icalendar.org/) is an internet standard for exchange of calendar information. iCalendar is used and supported by many products
including Google Calendar, Apple Calendar and Microsoft Outlook. It's also supported by a few federation fixture lists.

## Support for iCalendar in federation fixture lists


Product | Used by | [iCalendar export](#icalendar-export) | [Geocoding](#geocoding) | [Custom MTBO URL](#custom-url) | Notes
------- | ------- | ----------- | --------- | ---------------------- | -----
eventor | IOF, SWE, NOR, AUS |  :heavy_check_mark: |  :heavy_check_mark: |:x: |
Unknown | SUI |  :heavy_check_mark: | :heavy_check_mark: | :x: |
OriOasis | POR | :heavy_check_mark: | :x: | :x: | Bug: missing UID, races must to be deleted manually before updating.
O-Manager | GER | :heavy_check_mark: | :x: | :x: | Bug: error text in export file which must be deleted manually. Every race must be selected individually to export.
Unknown | LAT |  :heavy_check_mark: | :x: | :x: |
O-Service | DEN | :x: | :x: | :x: |
IRMA | FIN | :x: | :x: | :x: |
ORIS | CZE | :x: | :x: | :x: |
Unknown | FRA | :x: | :x: | :x: |

##### Table Footnotes
###### iCalendar export
A tick in this column indicates that it is possible to export to iCalendar format - though not necessarily easy or pretty (see Notes column).

###### Geocoding 
A GEO tag makes it possible to show race location on a map.

###### Custom URL
Without a custom url, exporting MTBO fixtures is a manual activity. A custom url makes it possible to automatically schedule synchronisation of fixtures to another calendar, reducing both work and risk that the information is out of date.

