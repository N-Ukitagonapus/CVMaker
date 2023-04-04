'''
職務経歴
'''
class CareerHistoryData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.flg_over = False										#終了フラグ
		self.term_start = ""										#期間：から
		self.term_end = ""											#期間：まで
		self.description_gyokai = ""						#業界
		self.description_project_overview = ""	#プロジェクト概要
		self.description_system_overview = ""		#システム概要
		self.description_work = []							#作業概要
		self.dev_env = {"srv":[] #開発環境・サーバ
										,"os" : [] #開発環境・OS
										,"db" : [] #開発環境・DB
										,"lang" : [] #開発環境・言語
										,"fw" : [] #開発環境・フレームワーク
										,"mw" : [] #開発環境・ミドルウェア
										,"tools" : [] #開発環境・ツール
										,"pkg":[]} #開発環境・パッケージ
		self.tasks = []													#作業内容
		self.scale = ""													#開発規模
		self.position = ""											#職位
		self.flg_internal_leader = False				#自社リーダーフラグ
		self.members = 0												#メンバー人数
		self.members_internal = 0								#自社メンバー人数