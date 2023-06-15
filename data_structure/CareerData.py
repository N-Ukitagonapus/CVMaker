'''
職務経歴
'''
import datetime
import uuid
from data_structure.EnvironmentData import EnvironmentData
from utils.Utilities import Utilities as util
class CareerData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.uuid = uuid.uuid4()
		self.flg_over = False										#終了フラグ
		self.term_start = datetime.date.today()	#期間：から
		self.term_end = util.get_last_date(datetime.date.today())		#期間：まで
		self.description_gyokai = ""						#業界
		self.description_project_overview = ""	#プロジェクト概要
		self.description_system_overview = ""		#システム概要
		self.description_work = []							#作業概要
		self.environment = EnvironmentData()				#開発環境
		self.tasks = []													#作業内容
		self.tasks_etc = ""											#作業内容その他
		self.scale = ""													#開発規模
		self.position = ""											#職位
		self.position_etc = ""									#職位
		self.flg_internal_leader = False				#自社リーダーフラグ
		self.members = 0												#メンバー人数
		self.members_internal = 0								#自社メンバー人数