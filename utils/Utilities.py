import calendar

class Utilities:
	def get_last_date(dt):
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	def tidy_list(list):
		return [s for s in list if s != '']