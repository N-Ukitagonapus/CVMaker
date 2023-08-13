'''
個人基本情報
'''
import datetime
from tkinter import StringVar
class PersonalData:
  #コンストラクタ(のようなもの)
	def __init__(self):
		self.shain_num = StringVar()						#社員番号
		self.name_last_kanji = StringVar()			#姓-漢字
		self.name_first_kanji = StringVar()			#名-漢字
		self.name_last_romaji = StringVar()			#姓-ローマ字
		self.name_first_romaji = StringVar()		#名-ローマ字
		self.gender = StringVar()								#性別
		self.birthday = datetime.date		#誕生日
		self.current_address = StringVar()			#現住所
		self.nearest_station = StringVar()			#最寄り駅
		self.gakureki = StringVar()							#最終学歴