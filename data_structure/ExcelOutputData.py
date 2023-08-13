'''
Excel出力データ
'''
from data_structure.EnvironmentData import EnvironmentData

class ExcelOutputData:
	def __init__(self):
		self.number = ""
		self.fullname = ""
		self.name_initial = ""
		self.gender = ""
		self.age = ""
		self.moyori_station = ""
		self.address = ""
		self.gakureki = ""
		self.gyokai_keiken = ""
		self.qualifications = ""
		self.tokui_bunya = ""
		self.keiken_server = ""
		self.siyoukeiken = EnvironmentData()
		self.pr = ""
		self.keireki = []

class KeirekiSubData:
		def __init__(self):
			self.text_kikan = ""
			self.text_gyomu = ""
			self.text_kankyo = ""
			self.text_kubun = ""
			self.text_sagyokibo = ""
			self.text_shokui = ""
			self.text_taisei = ""