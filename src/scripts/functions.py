def get_int(value, min, default):
	try:
		value = int(value)
		assert(value >= min)
	except:
		value = default

	return value

def clamp(x, min, max):
	if x < min: return min
	if x > max: return max

	return x

def get_data(table, page = 1, per_page = 10):
	page = get_int(page, 1, 1)
	per_page = get_int(per_page, 10, 10)

	count = run_query(f"select count(*) from `{table}`").first()[0]

	# Handle no data in table
	if count < 1:
		return [], page, per_page, 1, 1

	min_page = 1
	max_page = math.ceil(count / per_page)

	page = clamp(page, min_page, max_page)

	data = get_query_rows(f"select * from `{table}` limit {per_page} offset {(page - 1) * per_page}")

	return data, page, per_page, min_page, max_page

def is_price(price):
	"""
	:param str price:

	:return:
		True if price is represented as a float

		False otherwise

	:rtype: bool
	"""

	try:
		float(price)
		return True

	except ValueError:
		return False

def pricefy(price):
	"""
	:param str or float price:

	:return: price with 2 decimal points

	:rtype: str
	"""
	if not is_price:
		return

	return f"{float(price) : 0.2f}"
