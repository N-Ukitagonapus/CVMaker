import calendar

class DatetimeUtils:
	def get_last_date(dt):
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])