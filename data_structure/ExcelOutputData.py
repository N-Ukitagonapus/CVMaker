import datetime
from constants.const import TASKS, POSITIONS, TASKS_MERGE
from data_structure.EnvironmentData import EnvironmentData
from data_structure.ScaleData import ScaleData
from utils.Utilities import Utilities as util
from datetime import timedelta as td

class ExcelOutputData:
	"""
	EXCEL出力データ本クラス
	"""
	def __init__(self):
		self.number = ""											#社員番号
		self.fullname = ""										#氏名フルネーム
		self.name_initial = ""								#氏名イニシャル
		self.gender = ""											#性別
		self.age = ""													#年齢
		self.moyori_station = ""							#最寄駅
		self.address = ""											#住所
		self.gakureki = ""										#学歴
		self.gyokai_keiken = ""								#業界経験
		self.qualifications = ""							#取得資格
		self.tokui_bunya = ""									#得意分野
		self.siyoukeiken = EnvironmentData()	#使用経験
		self.pr = ""													#自己PR
		self.keireki = []											#職務経歴

class KeirekiSubData:
	"""
	EXCEL出力データ経歴サブクラス(基底)
	"""
	def __init__(self):
		self.text_kikan = ""
		self.text_gyomu = ""
		self.text_kankyo = ""
		self.text_sagyokibo = ""
		self.text_shokui = ""
		self.text_taisei = ""

	def set_kikan(self, term_start:datetime.date, term_end:datetime.date):
		"""
		期間列に設定するテキストを編集する。

		Parameters
		----------
		term_start : datetime.date
				業務開始年月
		term_end : datetime.date
				業務終了年月
		"""
		self.text_kikan = "{0}\n～\n{1}\n".format(term_start.strftime("%Y年%m月"), term_end.strftime("%Y年%m月"))
		self.text_kikan += "\n"
		monthdelta = util.get_years_sub(term_start, (term_end + td(days = 1)))
		self.text_kikan += "（{0}ヶ月）".format(monthdelta[1]) if monthdelta[0] == 0 else "（{0}年）".format(monthdelta[0],monthdelta[1]) if monthdelta[1] == 0 else "（{0}年{1}ヶ月）".format(monthdelta[0],monthdelta[1])

	def set_gyomu(self, gyokai:str, proj_gaiyo:str, sys_gaiyo:str, sagyo:str):
		"""
		業務内容列に設定するテキストを編集する。

		Parameters
		----------
		gyokai : str
				業界
		proj_gaiyo : str
				プロジェクト概要
		sys_gaiyo : str
				システム概要
		sagyo : str
				作業内容
		"""
		self.text_gyomu = ""
		if gyokai != "":
			self.text_gyomu += "【業種】\n"
			self.text_gyomu += gyokai
			self.text_gyomu += "\n"
		if proj_gaiyo != "":
			self.text_gyomu += "【プロジェクト概要】\n"
			self.text_gyomu += proj_gaiyo
			self.text_gyomu += "\n"
		if sys_gaiyo != "":
			self.text_gyomu += "【システム概要】\n"
			self.text_gyomu += sys_gaiyo
			self.text_gyomu += "\n"
		if sagyo != "":
			self.text_gyomu += "【業務内容】\n"
			self.text_gyomu += sagyo
			self.text_gyomu += "\n"

	def set_kankyo(self, env:EnvironmentData):
		"""
		開発環境列に設定するテキストを編集する。

		Parameters
		----------
		env : EnvironmentData
				開発環境データ
		"""
		self.text_kankyo = ""
		if len(env.server) > 0:
			self.text_kankyo += "【Server】{0}\n".format(",".join(env.server))
		if len(env.os) > 0:
			self.text_kankyo += "【OS】{0}\n".format(",".join(env.os))
		if len(env.db) > 0:
			self.text_kankyo += "【DB】{0}\n".format(",".join(env.db))
		if len(env.lang) > 0:
			self.text_kankyo += "【Lang】{0}\n".format(",".join(env.lang))
		if len(env.fw) > 0:
			self.text_kankyo += "【F/W】{0}\n".format(",".join(env.fw))
		if len(env.mw) > 0:
			self.text_kankyo += "【M/W】{0}\n".format(",".join(env.mw))
		if len(env.tools) > 0:
			self.text_kankyo += "【Tool】{0}\n".format(",".join(env.tools))
		if len(env.pkg) > 0:
			self.text_kankyo += "【PKG】{0}\n".format(",".join(env.pkg))

	def set_sagyo_kibo(self, scale:ScaleData):
		"""
		作業規模列に設定するテキストを編集する。

		Parameters
		----------
		scale : ScaleData
				作業規模データ
		"""
		self.text_sagyokibo = ""
		## 設計
		if scale.des_base > 0:
			self.text_sagyokibo += "基本設計：{0}本\n".format(scale.des_base) 
		if scale.des_detail > 0:
			self.text_sagyokibo += "詳細設計：{0}本\n".format(scale.des_detail) 
		## 製造
		if scale.gamens > 0:
			self.text_sagyokibo += "画面：{0}本\n".format(scale.gamens) 
		if scale.batches > 0:
			self.text_sagyokibo += "バッチ：{0}本\n".format(scale.batches) 
		if scale.forms > 0:
			self.text_sagyokibo += "帳票：{0}本\n".format(scale.forms) 
		if scale.etc1_name != "" and scale.etc1_num > 0:
			self.text_sagyokibo += "{0}：{1}本\n".format(scale.etc1_name, scale.etc1_num)
		if scale.etc2_name != "" and scale.etc2_num > 0:
			self.text_sagyokibo += "{0}：{1}本\n".format(scale.etc2_name, scale.etc2_num)
		if scale.total_steps > 0:
			self.text_sagyokibo += "総ステップ数：{0}\n".format(scale.total_steps) 
		## テスト
		if scale.uts > 0:
			self.text_sagyokibo += "単体テスト：{0}ケース\n".format(scale.uts) 
		if scale.its > 0:
			self.text_sagyokibo += "結合テスト：{0}ケース\n".format(scale.its) 
		if scale.sts > 0:
			self.text_sagyokibo += "システムテスト：{0}ケース\n".format(scale.sts) 

	def set_shokui(self, shokui:str, etc:str, leader_flg:bool):
		"""
		職位列に設定するテキストを編集する。

		Parameters
		----------
		shokui : str
				職位
		etc : str
				職位その他
		leader_flg : bool
				自社リーダーフラグ
		"""
		try:
			self.text_shokui = etc if (shokui == "その他" and etc != "") else POSITIONS[shokui]
			if leader_flg:
				self.text_shokui += "\n自社リーダー"
		except Exception as e:
			self.text_shokui = ""

	def set_taisei(self, total:int, jisha:int):
		"""
		体制列に設定するテキストを編集する。

		Parameters
		----------
		total : int
				総メンバー数
		jisha : int
				自社メンバー数
		"""
		self.text_taisei = "{0}名".format(total)
		if jisha > 0:
			self.text_taisei += "\n（自社メンバー{0}名）".format(jisha)


class KeirekiSubDataTypeA(KeirekiSubData) :
	"""
	EXCEL出力データ経歴サブクラス(Aタイプ)
	"""
	def __init__(self):
		super().__init__
		self.text_work_kbn = ""
	
	def set_work_kbn(self, works:list, etc:str):
		"""
		作業区分列に設定するテキストを編集する。

		Parameters
		----------
		works : list
				作業区分
		etc : str
				その他
		"""
		self.text_work_kbn = "\n".join([TASKS[s] for s in works if s != "ETC"])
		if etc != "":
			self.text_work_kbn += "\n" if self.text_work_kbn != "" else ""
			self.text_work_kbn += etc
    
class KeirekiSubDataTypeB(KeirekiSubData) :
	"""
	EXCEL出力データ経歴サブクラス(Bタイプ)
	"""
	def __init__(self):
		super().__init__
		self.list_work_kbn = []

	def set_work_kbn(self, works:list):
		"""
		作業区分群のフラグを設定する。

		Parameters
		----------
		works : list
				作業区分
		"""
		keys = TASKS_MERGE.keys()
		for key in keys:
			matching = set(works) & set(TASKS_MERGE[key])
			self.list_work_kbn.append(len(matching) > 0)