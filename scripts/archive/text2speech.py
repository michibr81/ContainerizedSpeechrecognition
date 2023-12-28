#!/usr/bin/env python

import subprocess
#import geodata as GEO
import datetime
import paho.mqtt.client as mqtt


def TextWithESpeak(text):
	print(text)
	command = 'espeak -s 170 -g 16 -vde "' + text + '"'
	process = subprocess.Popen([command], shell=True)
	process.wait()
	return

def Text(text):
	TextWithESpeak(text)

def Time(dateTime):
	Text(getTimeText(dateTime))
	return

def Date(dateTime):
	Text(getDateText(dateTime))

def DateWithWeekday(dateTime):
	Text(getWeekDayText(dateTime) + " der " + getDateText(dateTime))

def TimeAndDate(dateTime):
	Text(getTimeText(dateTime) + " am " + getDateText(dateTime))

def TimeAndDateWithWeekday(dateTime):
	Text(getTimeText(dateTime) + " am " + getWeekDayText(dateTime) + " der " + getDateText(dateTime))

def icsCalendarEvent(event, leaveAtTextAm=False, withWeekDay=False):
    
	eventSummary = event['SUMMARY']
	startDt = event['DTSTART'].dt

	if(leaveAtTextAm):
		eventSummary = eventSummary.split("am")[0]
	Text(eventSummary)

	if(withWeekDay):
		DateWithWeekday(startDt)
	else:
		Date(withWeekDay)
	
#
#text-Helper Area for date and time starts here
#
def getDateText(date):

	dateDelimiter = "."
	year = str(date.year)
	month = str(date.month)
	day = str(date.day)
	return str(day) + dateDelimiter + str(month) + dateDelimiter + year

def getTimeText(dateTime):
	return str(dateTime.hour) + " Uhr " + str(dateTime.minute)

def getWeekDayText(datetime):
    week = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    return week[datetime.weekday()]

# [START run_application]
if __name__ == '__main__':
    #TimeAndDateWithWeekday(datetime.datetime.now())
    Text("Computer bereit")
	
    
# [END run_application]<
