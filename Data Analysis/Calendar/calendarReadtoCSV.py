# Calendar Reader.
# From Git Hub, converted to python 3
# https://github.com/erikcox/ical2csv
#
# Usage
# Call the script and pass in the location of the ics file.
# Ex: python ical2csv event.ics

import sys
import os.path
from icalendar import Calendar, vDatetime
from datetime import datetime
import csv

filename = sys.argv[1]
file_extension = str(sys.argv[1])[-3:]
headers = ['Summary', 'UID', 'Description', 'Location',\
				'Start Time', 'End Time', 'URL']

class CalendarEvent:
	"""Calendar event class"""
	# summary = ''
	uid = ''
	description = ''
	location = ''
	start = ''
	end = ''
	url = ''

	def __init__(self, name):
		self.name = name

events = []


def open_cal():
	if os.path.isfile(filename):
		if file_extension == 'ics':
			print("Extracting events from file:", filename, "\n")
			f = open(sys.argv[1], 'r')
			gcal = Calendar.from_ical(f.read())

			
			data = gcal.to_ical().decode("utf-8")
			print(data[0:400])
			formatData = data.replace('\r\n', '\n')
			print(formatData[0:400])

			for component in gcal.walk():
				event = CalendarEvent(component.get('SUMMARY'))
				event.uid = component.get('UID')
				event.description = component.get('DESCRIPTION')
				event.location = component.get('LOCATION')
				# event.start = gcal.decoded(component.get('dtstart'))
				# event.end = component.get('dtend')
				event.url = component.get('URL')

				datastring = component.to_ical().decode("utf-8")
				# now we want to find the string
				dtstart_index = datastring.find('DTSTART')
				dtstart_start = datastring.find(':', dtstart_index)
				dtstart_end = datastring.find('\r', dtstart_index)

				date = datastring[int(dtstart_start) + 1: int(dtstart_end)]
				# print(date)
				try:
					event.start = vDatetime.from_ical(date)
				except ValueError as e:
					print(e)

				# now we want to find the string
				dtend_index = datastring.find('DTEND', dtstart_end)
				dtend_start = datastring.find(':', dtend_index)
				dtend_end = datastring.find('\r', dtend_index)

				date = datastring[int(dtend_start) + 1: int(dtend_end)]
				# print(date)
				try:
					event.start = vDatetime.from_ical(date)
				except ValueError as e:
					print(e)
				

				events.append(event)
			f.close()
		else:
			print("You entered ", filename, ". ")
			print(file_extension.upper(), \
				" is not a valid file format. Looking for an ICS file.")
			exit(0)
	else:
		print("I can't find the file ", filename, ".")
		print("Please enter an ics file located in the ",\
					" same folder as this script.")
		exit(0)

def csv_headers(icsfile):
	csvfile = icsfile[:-3] + "csv"
	try:
		with open(csvfile, 'w', newline='') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(headers)
			print("Wrote to ", csvfile, "\n")
	except IOError:
		print("Could not open file! Please close Excel!")
		exit(0)

def csv_write(icsfile, events):
	csvfile = icsfile[:-3] + "csv"
	try:
		with open(csvfile, 'a', newline='') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			for event in events:
				# values = [event.name, event.uid, event.description, \
				# 	event.location, event.start, event.end, event.url]
				values = [event.name, event.description, \
				 	event.location, event.start, event.end]
				wr.writerow(values)
			print("Wrote to ", csvfile, "\n")
	except IOError:
		print("Could not open file! Please close Excel!")
		exit(0)


def debug_event(class_name):
	print ("Contents of ", class_name.name, ":")
	print (class_name.name)
	print (class_name.uid)
	print (class_name.description)
	print (class_name.location)
	print (class_name.start)
	print (class_name.end)
	print (class_name.url, "\n")


open_cal()

debug_event(events[0])
csv_headers(filename)
csv_write(filename, events)
