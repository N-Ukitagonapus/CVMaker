'''
技術情報
'''
import datetime
from tkinter import IntVar, StringVar
class SkillData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.specialty = StringVar() #得意分野
		self.expr_start = datetime.date #業界開始年月
		self.period_absense_year = IntVar()
		self.period_absense_month = IntVar()
		self.qualifications = [] #取得資格
		self.expr_env={"srv":[] #使用経験(業務外)・サーバ
										,"os" : [] #使用経験(業務外)・OS
										,"db" : [] #使用経験(業務外)・DB
										,"lang" : [] #使用経験(業務外)・言語
										,"fw" : [] #使用経験(業務外)・フレームワーク
										,"mw" : [] #使用経験(業務外)・ミドルウェア
										,"tools" : [] #使用経験(業務外)・ツール
										,"pkg":[]} #使用経験(業務外)・パッケージ
		self.pr = StringVar() #自己PR