#!/usr/bin/env python3

from requests import Session
from .tools import web
from .tools import read
from .metadata import dictionary

def make_dictionary(blob, name, timetag, tabletag, count, value_position, value_nonnegative):
	# Create empty dictionary to fill measurements into
	x = {}
	# Retrieve timestamp corresponding to the set of measurements of interest
	x["timestamp"] = read.datetime_with_only_time(read.text_from_span_content(blob, timetag), 'HH:mm:ss').format('YYYY-MM-DD HH:mm:ss')
	# Retrieve rows from table containing power measurements from different entities
	rows = blob.find("table", {"id": tabletag}).findAll('tr')
	# Iterate over rows
	for index in range(0, count):
		# Retrieve the power measurement and the name of the entity, and assign the measurement against the index number of the entity categorized by its type
		x[dictionary.items[name][read.name(rows[index + 1])]] = read.value(rows[index + 1], value_position, value_nonnegative)
	# Return a dictionary of all power measurements and the corresponding timestamp
	return x

def fetch(session=None):
	# Read real-time dashboard's webpage into blob using BeautifulSoup
	html = web.get_response_bs4('IN-DL', 'http://www.delhisldc.org/Redirect.aspx?Loc=0804', session)

	# Retrieve frequency of the grid from span tag's content
	frequency = read.text_from_span_content(html, 'ContentPlaceHolder3_LBLFREQUENCY')
	timestamp = read.datetime_with_only_time(read.text_from_span_content(html, "ContentPlaceHolder3_ddtime"), 'HH:mm:ss').format('YYYY-MM-DD HH:mm:ss')

	# Create dictionary of power generation/consumption measurements from different entities viz. plants, companies and jurisdictions
	print(make_dictionary(html, 'plants_state', "ContentPlaceHolder3_ddgenco", "ContentPlaceHolder3_dgenco", 6, 2, 0))
	print(make_dictionary(html, 'discoms', "ContentPlaceHolder3_ddtime", "ContentPlaceHolder3_DDISCOM", 6, 2, 0))
	print(make_dictionary(html, 'states', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_Dstatedrawl", 8, 4, 0))
	print(make_dictionary(html, 'plants_centre', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_dcsgeneration", 25, 2, 0))
	print(make_dictionary(html, 'substations', "ContentPlaceHolder3_lblgridtime", "ContentPlaceHolder3_dgrid", 45, 2, 0))
	print(make_dictionary(html, 'energy_import', "ContentPlaceHolder3_lblimporttime", "ContentPlaceHolder3_DIMPORT", 33, 2, 0))
	print(make_dictionary(html, 'energy_export', "ContentPlaceHolder3_lblexporttime", "ContentPlaceHolder3_dEXPORT", 9, 1, 0))

if __name__ == '__main__':
	session = Session()
	fetch(session)
