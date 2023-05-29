'''
技術情報
'''
import datetime
from tkinter import IntVar, StringVar
from data_structure.EnvironmentData import EnvironmentData
class SkillData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.specialty = StringVar() #得意分野
		self.expr_start = datetime.date #業界開始年月
		self.period_absense_year = IntVar()
		self.period_absense_month = IntVar()
		self.qualifications = [] #取得資格
		self.expr_env = EnvironmentData()
		self.pr = StringVar() #自己PR