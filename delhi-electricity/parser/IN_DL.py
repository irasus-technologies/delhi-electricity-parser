#!/usr/bin/env python3

from sqlalchemy.orm import scoped_session, sessionmaker
from requests import Session
import os
from datetime import datetime

from .tools import web
from .tools import read
from .tools import delhi_electricity
# from .metadata import dictionary

def make_dictionary(blob, name, timetag, tabletag, value_position, value_nonnegative, sqlalchemy_session):
	# Create empty dictionary to fill measurements into
	x = {}
	# Retrieve timestamp corresponding to the set of measurements of interest
	x["timestamp"] = read.datetime_with_only_time(read.text_from_span_content(blob, timetag), 'HH:mm:ss').format('YYYY-MM-DD HH:mm:ss')
	# Retrieve rows from table containing power measurements from different entities
	rows = blob.find("table", {"id": tabletag}).findAll('tr')
	# Iterate over rows
	for index in range(0, len(rows) - 1):
		# Retrieve the power measurement and the name of the entity, and assign the measurement against the index number of the entity categorized by its type
		# x[dictionary.items[name][read.name(rows[index + 1])]] = read.value(rows[index + 1], value_position, value_nonnegative)
		x[read.name(rows[index + 1])] = read.value(rows[index + 1], value_position, value_nonnegative)
		try:
			row = delhi_electricity.power(unitName=read.name(rows[index + 1]), unitType=name, timestamp=datetime.strptime(read.datetime_with_only_time(read.text_from_span_content(blob, timetag), 'HH:mm:ss').format('YYYY-MM-DD HH:mm:ss'), '%Y-%m-%d %H:%M:%S'), power=read.value(rows[index + 1], value_position, value_nonnegative))
		except Exception as e:
			print(f"Exception \"{e}\"")
		else:
			sqlalchemy_session.add(row)
			try:
				# Commit the changes to the database
				sqlalchemy_session.commit()
				# Flush the changes to the database
				sqlalchemy_session.flush()
			except Exception as e:
				print(f"Exception \"{e}\"")
				# Rollback the current transaction
				sqlalchemy_session.rollback()
	# Return a dictionary of all power measurements and the corresponding timestamp
	return x

if __name__ == '__main__':

	# TimescaleDB configuration
	timescaledb_hostname = os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__HOSTNAME", "localhost")
	timescaledb_portnumber = int(os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__PORTNUMBER", 5432))
	timescaledb_database = os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__DATABASE", "DATABASE_NAME")
	timescaledb_username = os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__USERNAME", "delhi_electricity")
	timescaledb_password = os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__PASSWORD", "delhi_electricity")
	timescaledb_schema = os.environ.get("DELHI_ELECTRICITY__TIMESCALEDB__SCHEMA", "delhi_electricity")

	# Create the TimescaleDB engine
	db_url = f"postgresql://{timescaledb_username}:{timescaledb_password}@{timescaledb_hostname}:{timescaledb_portnumber}/{timescaledb_database}"
	engine = delhi_electricity.create_engine(db_url, pool_size=2, max_overflow=0, pool_timeout=5)

	# Create the database tables (if not already created)
	delhi_electricity.Base.metadata.create_all(engine)

	# Create a session factory
	sqlalchemy_session_factory = scoped_session(sessionmaker(bind=engine))
	sqlalchemy_session = sqlalchemy_session_factory()

	requests_session = Session()

	# Read real-time dashboard's webpage into blob using BeautifulSoup
	html = web.get_response_bs4('IN-DL', 'http://www.delhisldc.org/Redirect.aspx?Loc=0804', requests_session)

	# Retrieve frequency of the grid from span tag's content
	frequency = read.text_from_span_content(html, 'ContentPlaceHolder3_LBLFREQUENCY')
	timestamp = read.datetime_with_only_time(read.text_from_span_content(html, "ContentPlaceHolder3_ddtime"), 'HH:mm:ss').format('YYYY-MM-DD HH:mm:ss')
	# print(str(frequency) + ' ' + str(timestamp))
	try:
		row = delhi_electricity.frequency(frequency=frequency, timestamp=timestamp)
	except Exception as e:
		print(f"Exception \"{e}\"")
	else:
		sqlalchemy_session.add(row)
		try:
			# Commit the changes to the database
			sqlalchemy_session.commit()
			# Flush the changes to the database
			sqlalchemy_session.flush()
		except Exception as e:
			print(f"Exception \"{e}\"")
			# Rollback the current transaction
			sqlalchemy_session.rollback()

	# Create dictionary of power generation/consumption measurements from different entities viz. plants, companies and jurisdictions
	print(make_dictionary(html, 'plants_state', "ContentPlaceHolder3_ddgenco", "ContentPlaceHolder3_dgenco", 2, 0, sqlalchemy_session))
	print(make_dictionary(html, 'discoms', "ContentPlaceHolder3_ddtime", "ContentPlaceHolder3_DDISCOM", 2, 0, sqlalchemy_session))
	print(make_dictionary(html, 'states', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_Dstatedrawl", 4, 0, sqlalchemy_session))
	print(make_dictionary(html, 'plants_centre', "ContentPlaceHolder3_lblstatestime", "ContentPlaceHolder3_dcsgeneration", 2, 0, sqlalchemy_session))
	print(make_dictionary(html, 'substations', "ContentPlaceHolder3_lblgridtime", "ContentPlaceHolder3_dgrid", 2, 0, sqlalchemy_session))
	print(make_dictionary(html, 'energy_import', "ContentPlaceHolder3_lblimporttime", "ContentPlaceHolder3_DIMPORT", 2, 0, sqlalchemy_session))
	print(make_dictionary(html, 'energy_export', "ContentPlaceHolder3_lblexporttime", "ContentPlaceHolder3_dEXPORT", 1, 0, sqlalchemy_session))
