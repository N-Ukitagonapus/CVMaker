import copy, base64
from constants.const import ENV_GENRE, ENV_SET
from data_structure.CareerData import CareerData
from data_structure.EnvironmentData import EnvironmentData
from data_structure.CareerHistoryData import CareerHistoryData
from data_structure.ScaleData import ScaleData
from data_structure.ShodoSetting import ShodoSetting
from utils.ShodoApiUtil import ShodoApi, ShodoApiError, ShodoApiRequestError
from utils.Utilities import Utilities as util
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, filedialog as fd
from constants.message import DialogMessage as diag
import datetime
from datetime import datetime as dt
import xml.etree.ElementTree as et

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"
BORDER = "-------------------------------------------------"

class CareerHistoryDataOutput():
	"""
	職務経歴データ出力クラス
	"""
  # 初期化
	def __init__(self, data:CareerHistoryData):
		self.data = data
		self.result_txt = []
		self.has_pointout = False
  
	def validation(self, shodo:ShodoSetting):
		"""
		データチェック
		"""

		def check_env_variants(envs:EnvironmentData) -> dict:
			def add_list(result:dict, check_list:list, key_name:str):
				check_res = util.check_valiant(check_list)
				if len(check_res) > 0:
					check_result = []
					for base in check_res.keys():
						check_result.append(" | ".join([base]+ check_res[base]))
					result[key_name] = check_result
			ret = {}
			add_list(ret,envs.server,"サーバ：")
			add_list(ret,envs.os,"OS：")
			add_list(ret,envs.db,"DB：")
			add_list(ret,envs.lang,"言語：")
			add_list(ret,envs.fw,"フレームワーク：")
			add_list(ret,envs.mw,"ミドルウェア：")
			add_list(ret,envs.tools,"ツール：")
			add_list(ret,envs.pkg,"パッケージ：")
			return ret

		def shodo_lint(descriptions:tuple) -> list:
			ret = [[], [], []]
			for i in range(0,3):
				result = []
				if shodo.is_active() :
					try:
						res = ShodoApi.lint_request(shodo, descriptions[i])
						for siteki in res:
							result.append(util.parse_shodo_response(siteki))
					except ShodoApiError :
						pass
					except ShodoApiRequestError as err:
						print(err)
						util.msgbox_showmsg(diag.DIALOG_ERROR_SHODO)
						shodo.deactivate()
						result = []
					ret[i] = result
			return ret
 
		result = []
		env_variants = EnvironmentData()
		err_total,warn_total = 0, 0
		i = 1
		shodo_warnings = shodo_lint(self.data.get_descriptions())
  
		# 経歴データごとに参照。
		for history in self.data.history_list:
			err, warn = 0, 0
			result.append("【経歴データ：{0}】".format(i))
			# 業務開始日が今日より未来の場合はエラー
			if history.term_start > datetime.date.today():
				result.append("[エラー]業務開始日に未来日付は入力できません。")
				err += 1
			# 業務開始日 ＜ 業務終了日の場合はエラー
			if history.term_start > history.term_end:
				result.append("[エラー]業務開始日に業務終了日以降の日付は入力できません。")
				err += 1
			# 業界は入力推奨(未入力の場合は警告)
			if str.strip(history.description_gyokai) == "":
				result.append("[警告]業界が未入力です。")
				warn += 1

			# プロジェクト概要は入力推奨(未入力の場合は警告)
			if str.strip(history.description_project_overview) == "":
				result.append("[警告]プロジェクト概要が未入力です。")
				warn += 1
    	# プロジェクト概要のShodo指摘
			if len(shodo_warnings[0]) > 0 and len(shodo_warnings[0][i-1])> 0:
				result.append("[警告]プロジェクト概要にShodoの校正指摘があります。")
				result.extend(shodo_warnings[0][i-1])
				warn += 1
    
			if str.strip(history.description_system_overview) == "":
				result.append("[警告]システム概要が未入力です。")
				warn += 1
    	# システム概要のShodo指摘
			if len(shodo_warnings[1]) > 0 and len(shodo_warnings[1][i-1])> 0:
				result.append("[警告]システム概要にShodoの校正指摘があります。")
				result.extend(shodo_warnings[1][i-1])
				warn += 1

    	# 作業内容のShodo指摘
			if len(shodo_warnings[2]) > 0 and len(shodo_warnings[2][i-1])> 0:
				result.append("[警告]作業内容にShodoの校正指摘があります。")
				result.extend(shodo_warnings[2][i-1])
				warn += 1
     
			# 開発規模の製造その他の名称が未入力の際に本数が入っていたらエラー
			scl = history.scale
			if scl.etc1_name == "" and scl.etc1_num > 0:
				result.append("[エラー]開発規模の「その他(1)」名称が未入力です。")
				err += 1
			if scl.etc2_name == "" and scl.etc2_num > 0:
				result.append("[エラー]開発規模の「その他(2)」名称が未入力です。")
				err += 1
			# 職位が「その他」で未入力の場合はエラー
			if history.position == "":
				result.append("[エラー]職位が未選択です。")
				err += 1
			# 職位が「その他」で未入力の場合はエラー
			if history.position == "その他" and str.strip(history.position_etc) == "":
				result.append("[エラー]職位が「その他」の場合は職位名を入力してください。")
				err += 1
			# 総メンバー数　＜　自社メンバー数の場合はエラー。
			if history.members < history.members_internal:
				result.append("[エラー]自社メンバー数が総メンバー数よりも多いです。確認してください。")
				err += 1
			# 総メンバー数　＜　自社メンバー数の場合はエラー。
			if history.members == 0:
				result.append("[エラー]総メンバー数が入力されていません。")
				err += 1
			# 作業内容「その他」にチェックがついているのに未入力の場合はエラー
			if len(history.tasks) == 0:
				result.append("[警告]作業内容にチェックが入っていません。")
				warn += 1
			# 作業内容「その他」にチェックがついているのに未入力の場合はエラー
			if "ETC" in history.tasks and str.strip(history.tasks_etc) == "":
				result.append("[エラー]作業内容の「その他」を入力してください。")
				err += 1
			#エラー総数
			if err == 0 and warn == 0:
				result.append("指摘なし")
			else:
				result.append("エラー：{0}　警告：{1}".format(err if err > 0 else "なし", warn if warn > 0 else "なし"))
			err_total += err
			warn_total += warn 
			i += 1
			result.append(BORDER)
			env_variants.extend(history.environment)
		result.append("【開発環境表記ゆれ】")
		variants = check_env_variants(env_variants)
		if len(variants) == 0:
			result.append("表記ゆれなし")
		else:
			for key in variants.keys():
				result.append("【{0}】".format(key))
				result += variants[key]
				warn_total += 1

		# 指摘総数出力
		result.append("【指摘総数】")
		if err_total == 0 and warn_total == 0:
			result.append("指摘なし")
		else:
			result.append("エラー：{0}　警告：{1}".format(err_total if err_total > 0 else "なし", warn_total if warn_total > 0 else "なし"))
			
		self.result_txt = result
		self.has_pointout = err_total > 0 or warn_total > 0

	#入力チェック画面
	def check_input(self,target:tk.LabelFrame, shodo:ShodoSetting):
		"""
		入力チェック画面表示
		Args:
				target (tk.LabelFrame): 表示元フレーム
		"""
		self.validation(shodo)
		subwindow = tk.Toplevel(target)
		subwindow.title("職務経歴情報チェック")
		subwindow.geometry("640x480")
		subwindow.resizable(False,False)
		subwindow.grab_set()
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="職務経歴情報チェック", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="強制出力" if self.has_pointout else "出力")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		text_result=ScrolledText(subwindow,wrap=tk.WORD)
		text_result.pack(side=tk.TOP,expand=True,padx=10,pady=5)
		text_result.insert('1.0',"\n".join(self.result_txt))
		text_result["state"]=tk.DISABLED
		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
	
		btn_ok["command"] = lambda: do_output()
		btn_cancel["command"] = lambda: cancel()

		def do_output():
			"""
			出力処理実行
			"""
			try:
				self.output()
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			subwindow.destroy()
		def cancel():
			"""
			キャンセル
			"""
			subwindow.destroy()
    
	def output(self):
		"""
  	ファイル出力
		"""
		def set_value(tgt,tag,value):
			"""
   		値設定
			Args:
					tgt (str): 設定先タグ
					tag (str): タグ名
					value (str,int,bool): 設定値
			"""
			if value is not None:
				if (type(value) == str and value != "") or (type(value) == int and value > 0) or (type(value) == bool and value):
					et.SubElement(tgt,tag).text = str(value)

		def create_list(tgt, base_title, list:list):
			"""
			リストからのタグ生成
			Args:
					tgt (dtr): 設定先タグ
					base_title (str): 親タグ名
					list (list): 設定値
			"""
			inner = et.SubElement(tgt,base_title)
			for val in list:
				et.SubElement(inner, "value").text = val

		def create_env(tgt, envs:EnvironmentData):
			"""
			開発環境タグ生成
			Args:
					tgt (str): 設定先タグ
					envs (EnvironmentData): 開発環境データ
			"""
			trunk = et.SubElement(tgt, "environments")
			create_list(trunk, "servers",envs.server)
			create_list(trunk, "os",envs.os)
			create_list(trunk, "databases",envs.db)
			create_list(trunk, "languages",envs.lang)
			create_list(trunk, "frameworks",envs.fw)
			create_list(trunk, "middlewares",envs.mw)
			create_list(trunk, "tools",envs.tools)
			create_list(trunk, "packages",envs.pkg)

		# 開発規模作成
		def create_scale(tgt, scale:ScaleData):
			"""
			開発規模タグ生成
			Args:
					tgt (str): 設定先タグ
					scale (ScaleData): 開発規模データ
			"""
			trunk = et.SubElement(tgt, "scale")
			## 設計
			set_value(trunk, "des_base", scale.des_base)				#基本設計
			set_value(trunk, "des_detail", scale.des_detail)			#詳細設計
			## 製造
			set_value(trunk, "gamens", scale.gamens)					#画面数
			set_value(trunk, "batches", scale.batches)				#バッチ数
			set_value(trunk, "forms", scale.forms)					#帳票数
			set_value(trunk, "etc1_name", scale.etc1_name)			#その他1：名称
			set_value(trunk, "etc1_num", scale.etc1_num)				#その他1：数
			set_value(trunk, "etc2_name", scale.etc2_name)			#その他2：名称
			set_value(trunk, "etc2_num", scale.etc2_num)				#その他2：数
			set_value(trunk, "total_steps", scale.total_steps)		#総ステップ
			## テスト
			set_value(trunk, "uts", scale.uts)						#単体テスト
			set_value(trunk, "its", scale.its)						#結合テスト
			set_value(trunk, "sts", scale.sts)						#総合テスト

		# 経歴作成
		def create_career(tgt, career:CareerData):
			"""
   		職務経歴レコード作成
			Args:
					tgt (str): 設定先タグ
					career (CareerData): 職務経歴レコードデータ
			"""
			trunk = et.SubElement(tgt, "Career")
			set_value(trunk, "flg_over", str(career.flg_over))										#終了フラグ
			set_value(trunk, "term_start", career.term_start.strftime("%Y%m"))		#期間：から
			set_value(trunk, "term_end", career.term_end.strftime("%Y%m"))				#期間：まで
			set_value(trunk, "gyokai", career.description_gyokai)														#業界
			set_value(trunk, "project_gaiyo", career.description_project_overview)					#プロジェクト概要
			set_value(trunk, "system_gaiyo", career.description_system_overview)						#システム概要
			set_value(trunk, "work", career.description_work)																#作業概要
			create_env(trunk, career.environment)																						#開発環境
			create_list(trunk, "task", career.tasks)																				#作業内容
			set_value(trunk, "task_etc", career.tasks_etc)																	#作業内容その他
			create_scale(trunk, career.scale)																								#開発規模
			set_value(trunk, "position", career.position)																		#職位
			set_value(trunk, "position_etc", career.position_etc)														#職位その他
			set_value(trunk, "flg_internal_leader", career.flg_internal_leader)							#自社リーダーフラグ
			set_value(trunk, "members", career.members)																			#メンバー人数
			set_value(trunk, "members_internal", career.members_internal)										#自社メンバー人数
   
		### ここから本処理 ###
		base = et.Element("CareerData")
		tree = et.ElementTree(element=base)
  
		et.SubElement(base,"key").text = util.encode_key(self.data.last_name_kanji + self.data.first_name_kanji)
  
		for career in self.data.history_list:
			create_career(base, career)
		et.indent(tree,"\t")

		filename = fd.asksaveasfilename(
			title = "職務経歴情報保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			defaultextension = DEFAULT_EXT
    )
		if filename != "":
			tree.write(filename, encoding="utf-8", xml_declaration=True)

class CareerHistoryDataInput():
	"""
	職務経歴データ読込クラス
	"""
	def __init__(self):
		self.filename = fd.askopenfilename(
		title = "職務経歴データ読込",
		filetypes = FILE_TYPES,
		initialdir = INITIAL_DIR,
		defaultextension = DEFAULT_EXT
    )

	def read(self, last_name:str, first_name:str) -> CareerHistoryData:

		def keycheck(key, name: str) -> bool:
			"""
			キー項目チェック
			Args:
					input (dict): 読込結果
					data (SkillData): 技術情報データ
			"""
			if key is not None and util.decode_key(key.text) == name:
				return True
			else:
				return util.msgbox_ask(diag.DIALOG_WARN_KEYINVALID)

		def read_value(tag):
			"""
			文字列読込
			Args:
					tag (str): 読込元タグ

			Returns:
					str: 読込結果 
			"""
			return "" if tag is None else tag.text

		def read_int(tag):
			"""
			数値読込
			Args:
					tag (str): 読込元タグ

			Returns:
					int: 読込結果 
			"""
			return 0 if tag is None else util.int_from_str(tag.text)

		def read_bool(tag):
			"""
			ブール値読込
			Args:
					tag (str): 読込元タグ

			Returns:
					bool: 読込結果 
			"""
			return False if tag is None else tag.text == "True"

		def read_list(tag):
			"""
			リスト読込
			Args:
					tag (str): 読込元タグ

			Returns:
					list: 読込結果
			"""
			ret = []
			if tag is not None:
				for value in tag.iter("value"):
					ret.append(value.text)
			return ret

		def read_env(tree) -> EnvironmentData:
			"""
   		開発環境データ読込

			Args:
					tree (str): 読込元

			Returns:
					EnvironmentData: 読込結果
			"""
			keys=[
				("servers","srv"),
				("os","os"),
				("databases","db"),
				("languages","lang"),
				("frameworks","fw"),
				("middlewares","mw"),
				("tools","tools"),
				("packages","pkg")
			]
			dish = copy.deepcopy(ENV_SET)
			if tree is not None:
				for key in keys:
					subtree = tree.find(key[0])
					if subtree is not None:
						for value in subtree.iter("value"):
							dish[key[1]].append(value.text)
			ret = EnvironmentData()
			ret.set_values(dish)
			return ret
		
		def read_scale(scale) -> ScaleData:
			"""
			開発規模データ読込

			Args:
					scale (Element): 読込内容

			Returns:
					ScaleData: 読込結果
			"""
			ret = ScaleData()
			## 設計
			ret.des_base = read_int(scale.find("des_base"))					#基本設計
			ret.des_detail = read_int(scale.find("des_detail"))			#詳細設計
			## 製造
			ret.gamens = read_int(scale.find("gamens"))							#画面数
			ret.batches = read_int(scale.find("batches"))						#バッチ数
			ret.forms = read_int(scale.find("forms"))								#帳票数
			ret.etc1_name = read_value(scale.find("etc1_name"))			#その他1：名称
			ret.etc1_num = read_int(scale.find("etc1_num"))					#その他1：数
			ret.etc2_name = read_value(scale.find("etc2_name"))			#その他2：名称
			ret.etc2_num = read_int(scale.find("etc2_num"))					#その他2：数
			ret.total_steps = read_int(scale.find("total_steps"))		#総ステップ
			## テスト
			ret.uts = read_int(scale.find("uts"))										#単体テスト
			ret.its = read_int(scale.find("its"))										#結合テスト
			ret.sts = read_int(scale.find("sts"))										#総合テスト
			return ret

		def read_career(career) -> CareerData:
			"""
			職務経歴レコードデータ読込

			Args:
					career (Element): 読込内容

			Returns:
					CareerData: 読込結果
			"""
			ret = CareerData()
			ret.flg_over = read_bool(career.find("flg_over"))																						#終了フラグ
			ret.set_term_start(dt.strptime(career.find("term_start").text,"%Y%m"))											#期間：から
			ret.set_term_end(util.get_last_date(dt.strptime(career.find("term_end").text,"%Y%m")))			#期間：まで
			ret.description_gyokai = read_value(career.find("gyokai"))																	#業界
			ret.description_project_overview = read_value(career.find("project_gaiyo"))									#プロジェクト概要
			ret.description_system_overview = read_value(career.find("system_gaiyo"))										#システム概要
			ret.description_work = read_value(career.find("work"))																			#作業概要
			ret.environment = read_env(career.find("environments"))																			#開発環境
			ret.tasks = read_list(career.find("task"))																									#作業内容
			ret.tasks_etc = read_value(career.find("task_etc"))																					#作業内容その他
			ret.scale = read_scale(career.find("scale"))																								#開発規模
			ret.position = read_value(career.find("position"))																					#職位
			ret.position_etc = read_value(career.find("position_etc"))																	#職位その他
			ret.flg_internal_leader = read_bool(career.find("flg_internal_leader"))											#自社リーダーフラグ
			ret.members = read_int(career.find("members"))																							#メンバー人数
			ret.members_internal = read_int(career.find("members_internal"))														#自社メンバー人数
			return ret

		## ここから本処理 ##
		# XMLを取得
		if self.filename == "" :
			return None
		else :
			tree = et.parse(self.filename) 
			root = tree.getroot()
			if keycheck(root.find("key"), last_name + first_name):
				# 返却クラス定義
				ret = CareerHistoryData()
				ret.last_name_kanji = last_name
				ret.first_name_kanji = first_name
				ret.history_list = []
				for career in root.iter("Career"):
					ret.history_list.append(read_career(career))
				return ret
			else :
				return None