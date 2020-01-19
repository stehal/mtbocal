# iCalendar

[iCalendar](https://icalendar.org/) is an internet standard for exchange of calendar information. iCalendar is used and supported by many products
including Google Calendar, Apple Calendar and Outlook. It's also supported by a few federation fixture lists.

## Support for iCalendar in federation fixture lists


Product | Used by | [iCalendar export](#icalendar_export) | Geo coded [2] | Custom URL for MTBO [3] | Notes
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

####iCalendar export
It's possible to export export fixtures in iCalendar format (not always easy or pretty)

####[2] With a GEO tag, race location can be shown on a map.

####[3] With a custom endpoint it's possible to automatically schedule synchronisation of fixtures to another calendar.

