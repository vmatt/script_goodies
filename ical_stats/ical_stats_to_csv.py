from icalendar import Calendar, Event
from datetime import datetime
import pytz
import requests
import calendar
import dotenv


def contains(txt,word_list):
    for word in word_list:
        if word in txt:
            return True
    return False
url = dotenv.dotenv_values('.env')['CAL_URL']
ignored_events = dotenv.dotenv_values('.env')['IGNORED_EVENTS'].split(',')
ignored_events = [x.strip().strip("'") for x in ignored_events]
year = int(input("Enter year (press enter to current year): ") or datetime.now().year)
month = int(input("Enter month (01-12) (press enter to current month): ") or datetime.now().month)
end_day = calendar.monthrange(year, month)[1]
print()

gcal = Calendar.from_ical(requests.get(url).text)
events_dict = {}

for component in gcal.walk():
    title = component.get('SUMMARY')
    if not title:
        continue
    title = str(title)
    start_ts = component.get('DTSTART')
    end_ts   = component.get('DTEND')
    if isinstance(start_ts.dt,datetime) and isinstance(end_ts.dt,datetime) :
        start_ts = start_ts.dt.astimezone(pytz.timezone('Europe/Budapest'))
        end_ts   = end_ts.dt.astimezone(pytz.timezone('Europe/Budapest'))
        start_ts = start_ts.replace(tzinfo=None)
        end_ts = end_ts.replace(tzinfo=None)

        if datetime(year,month,1,0,0,0) < start_ts  and start_ts <  datetime(year,month,end_day,23,59,59):
            duration = end_ts - start_ts
            duration_hours = round(duration.total_seconds()/60/60,2)
            duration_hours = float(duration_hours)
            if not contains(title, ignored_events):
                try:
                    events_dict[title]+= duration_hours
                except KeyError:
                    events_dict[title] = duration_hours


total_hours = sum(events_dict.values())

# events_dict = sorted(events_dict.items(), key=lambda x:x[1])
for event_name,hours in events_dict.items():
    print(f"{event_name} - {hours} hours")
print(f" Summed hours: {total_hours}")



