"""
Quick add an event to your calendar." 
!caladd [name] [start date (default is the current date for the user)] [start time (required)] [end date (default is the start date)] [end time]"

 start date (required) - formatted as YYYY-MM-DD, use '!' to use the current local date" 
 start time (required) - formatted as HH:MM[AM/PM (if HH is < 12)], use '!' to use the current local time" 
 end date (required) - use '!' to use the same value as start date" 
 end time (required) - can be formatted as +[number][h(ours)/m(inutes)], which is appended to the start time, use '!' to use the default offset value from start time")

"""


import re
import datetime as dt
import time
import os
from dotenv import load_dotenv
import caldav
from caldav.davclient import get_davclient

load_dotenv()
caluser = os.getenv('CALDAV_USERNAME')

def getUserSettings(author_id):
    return {
        "offset": "+1h",
        "TZ": "-04:00"
    }

def parseOffset(offsetstr):
    offsetdirection = offsetstr[0]
    offsetval = offsetstr[1:len(offsetstr)-1]
    offsetunit = offsetstr[len(offsetstr)-1]
    
    if(offsetdirection not in ["+", "-"]):
        raise Exception("Invalid offset direction ({}) specified.".format(offsetdirection))

    if(offsetunit not in [ "h", "m" ]):
        raise Exception("Invalid offset unit ({}) specified.".format(offsetunit))

    try:
        offset = int(offsetval)
    except:
        raise Exception("Invalid offset ({}) specified.".format(offsetval))

    if offsetunit == "h":
        return dt.timedelta(hours=offset)
    else:
        return dt.timedelta(minutes=offset)


def addEvent(author_id, args):

    if len(args) != 5:
        return "Invalid number of arguments specified."
    else:
        eventName = args[0]
        startDate = args[1]
        startTime = args[2]
        endDate = args[3]
        endTime = args[4]

        userconfig = getUserSettings(author_id)

        if startDate == "!":
            d = dt.datetime.now()
        else:
            d = dt.datetime.fromisoformat(startDate)

        if startTime == "!":
            t = dt.datetime.now()
        else:
            t = dt.time.fromisoformcaldav_url, caldav_username and caldav_passwordat(startTime)

        start = dt.datetime.combine(d.date(), t.time())

        

        if endDate == "!":
            d = start
        else:
            d =  dt.datetime.fromisoformat(startDate)

        if re.fullmatch(r'[+-]\d+?[hm]', endTime) != None:
            t = dt.time.fromisoformat(endTime)
        elif endTime == "!":
            t = t + parseOffset("+15m")
        else:
            t = t + parseOffset(endTime)

        end = dt.datetime.combine(d.date(), t.time())

        with get_davclient() as client:
            cal = client.calendar(url="/dav.php/calendars/{}/personal".format(caluser))
            cal.save_event(
                dtstart=start,
                dtend=end,
                summary=eventName
            )

        stime = str(start.timestamp()).split('.')[0]
        etime = str(end.timestamp()).split('.')[0]
        return 'Added event {} starting at <t:{}:F> and ending at <t:{}:F>'.format(eventName, stime, etime)
