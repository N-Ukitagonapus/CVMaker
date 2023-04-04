import calendar
import datetime
from monthdelta import monthmod 

class Utilities:

	#2日付間の差分(年)を取得
	def get_year_sub(dt_from,dt_to):
		monthdelta = monthmod(dt_from,dt_to)
		return monthdelta[0].months//12

	#年月の初日を取得
	def get_first_date(dt):
		return datetime.date(dt.year, dt.month,1)
	
	#年月の最終日を取得
	def get_last_date(dt):
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	#リスト整頓(空白除去、重複削除)
	def tidy_list(list):
		return [s for s in list if s != '']