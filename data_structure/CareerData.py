import datetime
from tkinter import BooleanVar, StringVar, Text
from tkinter.scrolledtext import ScrolledText
import uuid
from constants.const import TASKS
from data_structure.EnvironmentData import EnvironmentData
from data_structure.ScaleData import ScaleData
from utils.Utilities import Utilities as util
class CareerData:
	"""
	職務経歴レコードデータ
	"""
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.flg_over = False																					#終了フラグ
		self.term_start = util.get_first_date(datetime.date.today())	#期間：から
		self.term_end = util.get_last_date(datetime.date.today())			#期間：まで
		self.description_gyokai = ""																	#業界
		self.description_project_overview = ""												#プロジェクト概要
		self.description_system_overview = ""													#システム概要
		self.description_work = ""																		#作業概要
		self.environment = EnvironmentData()													#開発環境
		self.tasks = []																								#作業内容
		self.tasks_etc = ""																						#作業内容その他
		self.scale = ScaleData()																			#開発規模
		self.position = ""																						#職位
		self.position_etc = ""																				#職位その他
		self.flg_internal_leader = False															#自社リーダーフラグ
		self.members = 0																							#メンバー人数
		self.members_internal = 0																			#自社メンバー人数

	def set_flg_over(self,input:BooleanVar):
		"""
		終了フラグ設定
		Args:
				input (BooleanVar): 入力値
		"""
		self.flg_over = input.get()

	def set_term_start(self,input):
		"""
		業務開始月設定
		Args:
				input : 入力値
    """
		self.term_start = util.get_dateclass(input)
  
	def set_term_end(self,input):
		"""
		業務終了月設定
		Args:
				input : 入力値
    """
		self.term_end = util.get_dateclass(input) if self.flg_over else util.get_dateclass(util.get_last_date(datetime.date.today()))

	def set_gyokai(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.description_gyokai = input.get()

	def set_proj_overview(self,input:ScrolledText):
		"""
		終了フラグ設定
		Args:
				input (ScrolledText): 入力値
		"""
		self.description_project_overview = str.strip(input.get('1.0','end'))

	def set_sys_overview(self,input:ScrolledText):
		"""
		終了フラグ設定
		Args:
				input (ScrolledText): 入力値
		"""
		self.description_system_overview = str.strip(input.get('1.0','end'))

	def set_works(self,input:Text):
		"""
		終了フラグ設定
		Args:
				input (Text): 入力値
		"""
		self.description_work = str.strip(input.get('1.0','end'))

	def set_tasks(self,input:dict):
		"""
		終了フラグ設定
		Args:
				input (dict): 入力値
		"""
		self.tasks = []
		task_keys=list(TASKS.keys())
		for i in range(len(task_keys)):
			if input[task_keys[i]].get():
				self.tasks.append(task_keys[i])

	def set_tasks_etc(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.tasks_etc = input.get()

	def set_position(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.position = input.get()

	def set_position_etc(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.position_etc = input.get()

	def set_flg_internal_leader(self,input:BooleanVar):
		"""
		終了フラグ設定
		Args:
				input (BooleanVar): 入力値
		"""
		self.flg_internal_leader = input.get()

	def set_members(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.members = util.int_from_str(input.get())

	def set_members_internal(self,input:StringVar):
		"""
		終了フラグ設定
		Args:
				input (StringVar): 入力値
		"""
		self.members_internal = util.int_from_str(input.get())