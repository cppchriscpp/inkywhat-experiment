# inkywhat experiment

Doing some experimenting with the inkywhat. This code can and will be clumsy; please look anywhere else for examples!

This shows output from an rss feed, as well as (eventually) weather info, and maybe more. (What about a twitter search?)

It puts it on a little layout that... honestly looks kinda silly but it's better than nothing.

## Cron entry

Want this to update every 30 minutes automatically? Dump this in `crontab -e`... and update your folder as needed.
```cron
*/30 * * * * cd /home/pi/inkywhat-experiment && /usr/bin/python main.py
```
