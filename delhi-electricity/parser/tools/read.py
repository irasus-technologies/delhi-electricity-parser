from arrow import get, utcnow

def datetime_from_span_content(html, span_content, format):
	return get(html.find('span', {'id': span_content}).text + ' Asia/Kolkata', format + ' ZZZ')

def text_from_span_content(html, span_content):
	return html.find('span', {'id': span_content}).text

def value_from_span_content(html, span_content):
	return float(text_from_span_content(html, span_content))

def datetime_with_only_time(time_string, time_format, now=utcnow()):
	utc = now.floor('hour')
	india_now = utc.to('Asia/Kolkata')
	time = get(time_string, time_format)
	india_datetime = india_now.replace(hour=time.hour, minute=time.minute, second=time.second)
	if india_datetime > india_now:
		india_datetime.shift(days=-1)
	return india_datetime

def value(row, index=2, nonnegative=1):
	value = float(row.findAll('td')[index].text)
	if nonnegative == 1:
		return value if value >= 0.0 else 0.0
	else:
		return value

def name(row, index=0):
	return str(row.findAll('td')[index].text)
