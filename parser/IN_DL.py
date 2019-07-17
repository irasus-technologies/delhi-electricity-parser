#!/usr/bin/env python

from requests import Session
from .lib import web
from .lib import read
from .metadata import dictionary

def make_dictionary(blob, name, timetag, tabletag, count, value_position, value_nonnegative):
	x = {}
	x["timestamp"] = read.datetime_with_only_time(read.text_from_span_content(blob, timetag), 'HH:mm:ss')
	rows = blob.find("table", {"id": tabletag}).findAll('tr')
	for index in range(0, count):
		x[dictionary.items[name][read.name(rows[index + 1])]] = read.value(rows[index + 1], value_position, value_nonnegative)
	return x

def fetch(session=None):
	html = web.get_response_bs4('IN-DL', 'http://www.delhisldc.org/Redirect.aspx?Loc=0804', session)

	frequency = read.text_from_span_content(html, 'ContentPlaceHolder3_LBLFREQUENCY')

	print make_dictionary(html, 'Plant', "ContentPlaceHolder3_ddgenco", "ContentPlaceHolder3_dgenco", 6, 2, 0)
	print make_dictionary(html, 'DISCOM', "ContentPlaceHolder3_ddtime", "ContentPlaceHolder3_DDISCOM", 6, 2, 0)
	print make_dictionary(html, 'State', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_Dstatedrawl", 8, 4, 0)
	print make_dictionary(html, 'Centre', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_dcsgeneration", 25, 2, 0)

if __name__ == '__main__':
	session = Session()
	fetch(session)
