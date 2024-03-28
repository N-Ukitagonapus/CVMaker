import copy
import tkinter as tk
from tkinter import  ttk
from tkinter.scrolledtext import ScrolledText
from constants.const import COLOR, ENV_GENRE, ENV_SET, VALID_ERR, VALID_OK, VALID_WARN
from data_structure.EnvironmentData import EnvironmentData
from data_structure.ShodoSetting import ShodoSetting
from data_structure.SkillData import SkillData
from tkinter import filedialog as fd
import xml.etree.ElementTree as et
from utils.ShodoApiUtil import ShodoApi, ShodoApiError, ShodoApiRequestError
from utils.Utilities import Utilities as util
from utils.Validation import StaticValidation as sval

from constants.message import Message as msg
from constants.message import DialogMessage as diag

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"
class SkillDataOutput():
	"""
	技術情報データ出力クラス
	"""
	def __init__(self,data:SkillData, shodo: ShodoSetting):
		self.data = data
		self.shodo = shodo
  
	#データ出力
	def confirm(self, target):
		"""
		確認画面表示

		Args:
				target (tk.Frame): サブウィンドウ表示対象フレーム(=メインフレーム)
		"""
		def warn_variants(target, result):
			def create_text(input:dict)->list:
				ret = []
				for key in input.keys():
					ret.append("【{0}】".format(key))
					ret += input[key]
				return ret
			dlg = tk.Toplevel(target)
			dlg.title("表記ゆれ警告")   # ウィンドウタイトル
			dlg.geometry("320x240")    # ウィンドウサイズ(幅x高さ)
			frame_title = tk.Frame(dlg,borderwidth=5,relief="groove")
			label_title = tk.Label(frame_title, text="表記ゆれ警告", font=("Meiryo UI",14,"bold"))
			label_title.pack(side=tk.TOP,padx=10,pady=5)
			frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

			text_result=ScrolledText(dlg,wrap=tk.WORD)
			text_result.pack(side=tk.TOP,expand=True,padx=10,pady=5)
			text_result.insert('1.0',"\n".join(create_text(result)))
			text_result["state"]=tk.DISABLED

		def warn_kousei(target, result):
			dlg = tk.Toplevel(target)
			dlg.title("文章校正指摘")   # ウィンドウタイトル
			dlg.geometry("600x300")    # ウィンドウサイズ(幅x高さ)
			frame_title = tk.Frame(dlg,borderwidth=5,relief="groove")
			label_title = tk.Label(frame_title, text="文章校正指摘", font=("Meiryo UI",14,"bold"))
			label_title.pack(side=tk.TOP,padx=10,pady=5)
			frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

			text_result=ScrolledText(dlg,wrap=tk.WORD)
			text_result.pack(side=tk.TOP,expand=True,padx=10,pady=5)
			text_result.insert('1.0',"\n".join(result))
			text_result["state"]=tk.DISABLED

		def check_env_variants(result:dict, envs:dict) -> dict:
			ret = {}
			for key in ENV_SET.keys():
				check_res = util.check_valiant(envs[key])
				if len(check_res) > 0:
					yureterumono = []
					for base in check_res.keys():
						yureterumono.append(" | ".join([base]+ check_res[base]))
					ret[ENV_GENRE[key]] = yureterumono

			result["result"] = VALID_OK if len(ret) == 0 else VALID_WARN
			result["msg"] = msg.MSG_OK if len(ret) == 0 else msg.MSG_WARN_VARIANT
			return ret

		def check_pr(result:dict, text:str) -> list:
			ret=[]
			if self.shodo.is_active() :
				try:
					res = ShodoApi.lint_request(self.shodo, text)
					ret = util.parse_shodo_response(res)
					result["result"] = VALID_OK if len(ret) == 0 else VALID_WARN
					result["msg"] = msg.MSG_OK if len(ret) == 0 else msg.MSG_WARN_SHODO
				except ShodoApiError :
					result["result"] = VALID_WARN
					result["msg"] = msg.MSG_WARN_EMPTY
				except ShodoApiRequestError as err:
					print(err)
					util.msgbox_showmsg(diag.DIALOG_ERROR_SHODO)
					self.shodo.deactivate()
					result["result"] = VALID_OK
					result["msg"] = msg.MSG_NOVALIDATION
			else :
				result["result"] = VALID_OK if len(text) > 0 else VALID_WARN
				result["msg"] = msg.MSG_NOVALIDATION if len(text) > 0 else msg.MSG_WARN_EMPTY
			return ret
 
		def final_validation(input_data: SkillData):
			sval.out_date_check(vals["expr_start"],input_data.expr_start)
			sval.io_novalidation(vals["absense"])
			sval.out_warn_if_empty(vals["specialty"],input_data.specialty.get())
			sval.io_novalidation(vals["qualifications"])
			sval.io_novalidation(vals["expr_env"])

		vals = {
			"expr_start":{"label":"業界経験開始年月"},
			"absense":{"label":"休職期間"},
			"specialty":{"label":"得意分野"},
			"qualifications":{"label":"取得資格"},
			"expr_env":{"label":"使用経験(業務外)"},
			"pr":{"label":"自己PR"}
		}
  
		final_validation(self.data)
		env_variants = check_env_variants(vals["expr_env"],self.data.expr_env.get_values())
		pr_kousei = check_pr(vals["pr"],self.data.pr)
		has_variants_warn = len(env_variants) > 0
		total_val = True
		for val in vals.values():
			if val["result"] in (VALID_ERR, VALID_WARN):
				total_val = False
				break
  
		subwindow = tk.Toplevel(target)
		subwindow.title("データ確認")
		subwindow.geometry("500x330" if has_variants_warn else "500x330")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_output = ttk.Button(frame_button_inner,width=10)
		button_output["text"] = "出力" if total_val == True else "強制出力"
		button_cancel = ttk.Button(frame_button_inner,width=10,text="キャンセル")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
		frame_button_inner.pack(pady=5)
		button_cancel.grid(row=0,column=0,padx=15)
		button_output.grid(row=0,column=1,padx=15)

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "技術情報 データ出力")
		frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
		frame_main_inner=tk.Frame(frame_main)
		frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)

		frame_name = []
		frame_result = []
		results = list(vals.items())
		for i in range(len(results)):
			frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg="white"))
			frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg=COLOR[results[i][1]["result"]]))
			frame_name[i].grid(row=i,column=0,sticky=tk.EW)
			frame_result[i].grid(row=i,column=1,sticky=tk.EW)
			tk.Label(frame_name[i],text=results[i][1]["label"],bg="white").pack(side=tk.LEFT,padx=3,pady=3)
			tk.Label(frame_result[i],text=results[i][1]["msg"],bg=COLOR[results[i][1]["result"]]).pack(side=tk.LEFT,padx=3,pady=3)
		frame_main_inner.columnconfigure(index=1, weight=1)

		button_output["command"] = lambda: output()
		button_cancel["command"] = lambda: cancel()

		if has_variants_warn:
			warn_variants(subwindow, env_variants)
   
		if len(pr_kousei) > 0:
			warn_kousei(subwindow, pr_kousei)
   
		def output():
			"""
			出力ボタン押下時動作
    	"""
			if total_val == False:
				if util.msgbox_ask(diag.DIALOG_ASK_FORCE_OUTPUT):
					do_output()
			else:
				do_output()

		def do_output():
			"""
   		出力処理本体
			"""
			try:
				self.output_file()
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			subwindow.destroy()

		def cancel():
			"""
   		キャンセル
			"""
			subwindow.destroy()
   
	def output_file(self):
		"""
		ファイル出力
		"""
		def create_list(tgt, list:list, base_title):
			"""
			リストタグ作成
			Args:
					tgt (str): 対象タグ
					list (list): 出力内容リスト
					base_title (str): 親タグ名
			"""
			if len(self.data.qualifications) > 0 :
				inner = et.SubElement(tgt,base_title)
				for val in list:
					et.SubElement(inner,"value").text = val

		def create_env(tgt, envs:EnvironmentData):
			"""
   		開発環境タグ作成
			Args:
					tgt (str): 対象タグ
					envs (EnvironmentData): 開発環境データ
			"""
			trunk = et.SubElement(tgt,"environments")
			create_list(trunk,envs.server,"servers")
			create_list(trunk,envs.os,"os")
			create_list(trunk,envs.db,"databases")
			create_list(trunk,envs.lang,"languages")
			create_list(trunk,envs.fw,"frameworks")
			create_list(trunk,envs.mw,"middlewares")
			create_list(trunk,envs.tools,"tools")
			create_list(trunk,envs.pkg,"packages")

		# ここから処理本体
		base = et.Element("SkillData")
		tree = et.ElementTree(element=base)
		et.SubElement(base,"key").text = util.encode_key(self.data.last_name_kanji + self.data.first_name_kanji)
		et.SubElement(base,"expr_start").text = self.data.expr_start.strftime("%Y%m")
		et.SubElement(base,"absense_year").text = "0" if self.data.period_absense_year.get() == "" else self.data.period_absense_year.get()
		et.SubElement(base,"absense_month").text = "0" if self.data.period_absense_month.get() == "" else self.data.period_absense_month.get()
		if self.data.specialty != "":
			et.SubElement(base,"specialty").text = self.data.specialty.get()
		create_list(base,self.data.qualifications,"qualifications")
		create_env(base,self.data.expr_env)
		if self.data.pr != "":
			et.SubElement(base,"pr").text = self.data.pr
		et.indent(tree,"\t")

		filename = fd.asksaveasfilename(
			title = "技術情報保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			defaultextension = DEFAULT_EXT
    )
		if filename != "":
			tree.write(filename, encoding="utf-8", xml_declaration=True)

class SkillDataInput():
	"""
	技術情報データ読込クラス
	"""
	def __init__(self,frame):
		self.frame = frame

	def read(self, target):
		"""
		読込実行
		Args:
				target (tk.Frame): サブウィンドウ表示元フレーム(=メインフレーム)
		"""
		filename = fd.askopenfilename(
		title = "個人基本情報読込",
		filetypes = FILE_TYPES,
		initialdir = INITIAL_DIR,
		defaultextension = DEFAULT_EXT
    )

		if filename != "":
			try:
				input = self.read_file(et.parse(filename))
				if self.keycheck(input,self.frame.data) :
					self.inputcheck(input)
					self.set_value(input)
					self.show_result(input, target)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
    
	#XML読込
	def read_file(self, tree) -> dict:
		"""
		ファイル読込
		Args:
				tree (str): 読込元

		Returns:
				dict: 読込結果
		"""
		# XMLを取得
		root = tree.getroot()
  
		def read_env(tree):
			"""
			開発環境データ読込
			Args:
					tree (str): 読込元

			Returns:
					EnvironmentData: 開発環境データ
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
			ret = copy.deepcopy(ENV_SET)
			if tree is not None :
				for key in keys:
					subtree = tree.find(key[0])
					if subtree is not None:
						for value in subtree.iter("value"):
							ret[key[1]].append(value.text)
			return ret

		#単体項目を取得
		vals = {
			"key":{"label":"KEY"},
			"expr_start":{"label":"業界開始年月"},
			"absense_year":{"label":"休職期間(年)"},
			"absense_month":{"label":"休職期間(月)"},
			"specialty":{"label":"得意分野"},
			"pr":{"label":"自己PR"}
			}
		keys = list(vals.keys())
		for key in keys:
			text = root.find(key)
			if text is not None:
				vals[key]["value"] = text.text if key != "expr_start" else text.text + "01"
			else:
				vals[key]["value"] = ""

		#資格情報を取得
		vals["qualifications"]={"label":"資格情報"}
		list_qual=[]
		sikaku = root.find("qualifications")
		if sikaku is not None:
			for value in sikaku.iter("value"):
				list_qual.append(value.text)
		vals["qualifications"]["value"] = list_qual

		#使用経験環境を取得
		vals["environments"]={"label":"使用経験(業務外)"}
		vals["environments"]["value"] = read_env(root.find("environments"))

		return vals

	def keycheck(self, input:dict, data: SkillData) -> bool:
		"""
		キー項目チェック
		Args:
				input (dict): 読込結果
				data (SkillData): 技術情報データ
		"""
		if util.decode_key(input["key"]["value"]) == data.last_name_kanji + data.first_name_kanji:
			return True
		else:
			return util.msgbox_ask(diag.DIALOG_WARN_KEYINVALID)

	def inputcheck(self, input:dict):
		"""
		読込結果チェック
		Args:
				input (dict): 読込結果
		"""
		sval.in_date_check(input["expr_start"])
		sval.in_regex_match(input["absense_year"],"[0-9]*","数字")
		sval.in_number_between(input["absense_month"],0,11,"0から11の間")
		sval.io_novalidation(input["specialty"])
		sval.io_novalidation(input["qualifications"])
		sval.io_novalidation(input["environments"])
		sval.io_novalidation(input["pr"])

	def set_value(self, input):
		"""
		読込結果設定
		Args:
				input (dict): 読込結果
		"""
		frame = self.frame
		data = frame.data
		util.setdate_from_read(frame.expr_start,input["expr_start"])
		data.expr_start = frame.expr_start.get_date()
		util.setstr_from_read(data.period_absense_year,input["absense_year"])
		util.setstr_from_read(data.period_absense_month,input["absense_month"])
		util.setstr_from_read(data.specialty,input["specialty"])
		data.qualifications = input["qualifications"]["value"]
		data.expr_env.set_values(input["environments"]["value"])
		data.pr = input["pr"]["value"]
		frame.text_pr.delete("1.0","end")
		frame.text_pr.insert('1.0',(input["pr"]["value"]))


	def show_result(self, input, target):
		"""
		読込結果表示
		Args:
				input (dict): 入力結果
				target (tk.Frame): サブウィンドウ表示対象フレーム(=メインフレーム)
		"""
		subwindow = tk.Toplevel(target)
		subwindow.title("ファイル読込結果")
		subwindow.geometry("500x390")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_ok = ttk.Button(frame_button_inner,width=10,text="OK")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
		frame_button_inner.pack(pady=5)
		button_ok.grid(row=0,column=0,padx=15)

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "技術情報 ファイル読込結果")
		frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
		frame_main_inner=tk.Frame(frame_main)
		frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)

		frame_name = []
		frame_result = []
		results = list(input.items())
		rownum = 0
		for i in range(len(results)):
			if results[i][1]["label"] != "KEY" :
				frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg="white"))
				frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg=COLOR[results[i][1]["result"]]))
				frame_name[rownum].grid(row=rownum,column=0,sticky=tk.EW)
				frame_result[rownum].grid(row=rownum,column=1,sticky=tk.EW)
				tk.Label(frame_name[rownum],text=results[i][1]["label"],bg="white").pack(side=tk.LEFT,padx=3,pady=3)
				tk.Label(frame_result[rownum],text=results[i][1]["msg"],bg=COLOR[results[i][1]["result"]]).pack(side=tk.LEFT,padx=3,pady=3)
				rownum += 1
		frame_main_inner.columnconfigure(index=1, weight=1)
		button_ok["command"] = lambda: subwindow.destroy()