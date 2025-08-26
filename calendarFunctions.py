import re
import datetime as dt
import time
import os
from dotenv import load_dotenv
import caldav
from caldav.davclient import get_davclient

# Load environment variables from ./.env
load_dotenv()

# get the user's env variable
caluser = os.getenv('CALDAV_USERNAME')


# Placeholder function for the default settings, in the end I want this to be something that is cross referenced per user perhaps.
def getUserSettings(author_id):
    return {
        "offset": "+1h",
        "TZ": "-04:00"
    }

# Function to parse offsets and return a timedelta object
# Expected format is r'[+-]{1}\d+?[hm]'
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

# Function to add an event. Takes in an author ID and arguments, returns nothing on error, returns the arguments if successful
# Arugments are [eventname, startdate, startTime, endDate, endTime]
def addEvent(author_id, args):

    # Return error if arguments is not 5
    if len(args) != 5:
        return "Invalid number of arguments specified."
    else:
        eventName = args[0]
        startDate = args[1]
        startTime = args[2]
        endDate = args[3]
        endTime = args[4]

        userconfig = getUserSettings(author_id)

        try:
            # '!' for startDate represents today's date
            if startDate == "!":
                d = dt.datetime.now().date()
            else:
                d = dt.datetime.fromisoformat(startDate).date()
        except:
            return 'Unable to parse the start date.'

        try:
            # '!' for startTime represents time of the command
            if startTime == "!":
                t = dt.datetime.now().time()
            else:
                t = dt.time.fromisoformat(startTime)
        except:
            return 'Unable to parse the start time.'

        # Combine both date and time to get a datetime object
        start = dt.datetime.combine(d, t)

        try:
            # '!' for endDate represents the same value as startDate
            if endDate == "!":
                d = start
            else:
                d =  dt.datetime.fromisoformat(endDate).date()
        except:
            return 'Unable to parse end date.'

        try:
            # '!' for endDate represents the startDate + the default offset from the user configuration
            if endTime == "!":
                endTime = "+15m"

            # call the parseOffset function if the string matches the regex expression
            if re.fullmatch(r'[+-]\d+?[hm]', endTime) != None:
                # timedelta objects cannot be added to a time object, so combining into a datetime needs to occur
                end = dt.datetime.combine(d, t)
                end += parseOffset(endTime)
            else:
                # when you get here, we know that an offset is NOT provided nor used
                t = dt.time.fromisoformat(endTime)
                end = dt.datetime.combine(d, t)
        except:
            return 'Unable to parse end time.'
        try:
            with get_davclient() as client:
                cal = client.calendar(url="/dav.php/calendars/{}/personal".format(caluser))
                cal.save_event(
                    dtstart=start,
                    dtend=end,
                    summary=eventName
                )
        except:
            return 'Unable to add event, got an error.'

        return 'Added event {} starting at <t:{}:F> and ending at <t:{}:F>'.format(eventName, round(start.timestamp()), round(end.timestamp()))
