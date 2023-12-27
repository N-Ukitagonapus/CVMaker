import datetime
from tkinter import StringVar
from data_structure.EnvironmentData import EnvironmentData
class SkillData:
	"""
	技術情報データ
	"""
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.last_name_kanji = "" #氏(キー)
		self.first_name_kanji = "" #名(キー)
		self.specialty = StringVar() #得意分野
		self.expr_start = datetime.date.today() #業界開始年月
		self.period_absense_year = StringVar()
		self.period_absense_month = StringVar()
		self.qualifications = [] #取得資格
		self.expr_env = EnvironmentData()
		self.pr = "" #自己PR