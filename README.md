# Python-Caldav Quick Add

A quick and dirty python script that is designed to be used with a discord bot.

> [!ERROR]
> This is an WIP script that is NOT ready for public consumption. Using this will require time to configure the code to do what you want it to do.

```
!caladd [name] [start date (default is the current date for the user)] [start time (required)] [end date (default is the start date)] [end time]"

 start date (required) - formatted as YYYY-MM-DD, use '!' to use the current local date" 
 start time (required) - formatted as HH:MM[AM/PM (if HH is < 12)], use '!' to use the current local time" 
 end date (required) - use '!' to use the same value as start date" 
 end time (required) - can be formatted as +[number][h(ours)/m(inutes)], which is appended to the start time, use '!' to use the default offset value from start time")
```

## Example

`!caladd "Birthday" ! ! ! !` will add an event called Birthday to your Personal Calendar, starting from the current time and ending 15 minutes after the current time.
