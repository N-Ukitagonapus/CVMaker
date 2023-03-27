'''
技術情報
'''
class SkillData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.specialty = ""	#得意分野
		self.experience_start = "" #業界開始年月
		self.period_absense = "" #休職期間
		self.qualifications = [] #取得資格
		self.experience={"srv":[] #使用経験(業務外)・サーバ
										,"os" : [] #使用経験(業務外)・OS
										,"db" : [] #使用経験(業務外)・DB
										,"lang" : [] #使用経験(業務外)・言語
										,"fw" : [] #使用経験(業務外)・フレームワーク
										,"mw" : [] #使用経験(業務外)・ミドルウェア
										,"tools" : [] #使用経験(業務外)・ツール
										,"pkg":[]} #使用経験(業務外)・パッケージ
		self.pr = [] #自己PR
