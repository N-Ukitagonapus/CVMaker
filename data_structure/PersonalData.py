'''
個人基本情報
'''
class PersonalData:
  #コンストラクタ(のようなもの)
	def __init__(self):
		self.shain_num = 0						#社員番号
		self.name_last_kanji = ""			#姓-漢字
		self.name_first_kanji = ""		#名-漢字
		self.name_last_romaji = ""		#姓-ローマ字
		self.name_first_romaji = ""		#名-ローマ字
		self.gender = ""							#性別
		self.birthday = ""						#誕生日
		self.current_address = ""			#現住所
		self.nearest_station = ""			#最寄り駅
		self.academic_background = ""	#最終学歴