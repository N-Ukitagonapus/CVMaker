import copy
import tkinter as tk
from tkinter import StringVar, ttk
from constants.const import ENV_SET, VALID_ERR
from data_structure.EnvironmentData import EnvironmentData
from data_structure.SkillData import SkillData
from tkinter import filedialog as fd
import xml.etree.ElementTree as et
from utils.Utilities import Utilities as util
from utils.Validation import StaticValidation as sval

from constants.const import COLOR, VALID_ERR, VALID_OK
from constants.message import DialogMessage as diag

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"
class SkillDataOutput():

	def __init__(self,data:SkillData):
		self.data = data
  
	#データ出力
	def confirm(self, target):
		def final_validation(input_data: SkillData):
			sval.out_date_check(vals["expr_start"],input_data.expr_start)
			sval.io_novalidation(vals["absense"])
			sval.out_warn_if_empty(vals["specialty"],input_data.specialty.get())
			sval.io_novalidation(vals["qualifications"])
			sval.io_novalidation(vals["expr_env"])
			sval.out_warn_if_empty(vals["pr"],input_data.pr)

		vals = {
			"expr_start":{"label":"業務開始日"},
			"absense":{"label":"休職期間"},
			"specialty":{"label":"得意分野"},
			"qualifications":{"label":"取得資格"},
			"expr_env":{"label":"使用経験(業務外)"},
			"pr":{"label":"自己PR"}
		}
  
		final_validation(self.data)
		total_val = True
		for val in vals.values():
			if val["result"] == VALID_ERR:
				total_val = False
				break

		subwindow = tk.Toplevel(target)
		subwindow.title("データ確認")
		subwindow.geometry("400x330")
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

		def output():
			if total_val == VALID_ERR:
				if util.msgbox_ask(diag.DIALOG_ASK_FORCE_OUTPUT):
					do_output()
			else:
				do_output()

		def do_output():
			try:
				SkillDataOutput(self.data).output()
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			subwindow.destroy()

		def cancel():
			subwindow.destroy()
	def output(self):
		def create_list(tgt, list:list, base_title):
			if len(self.data.qualifications) > 0 :
				inner = et.SubElement(tgt,base_title)
				for val in list:
					et.SubElement(inner,"value").text = val

		def create_env(tgt, envs:EnvironmentData):
			trunk = et.SubElement(tgt,"environments")
			create_list(trunk,envs.server,"servers")
			create_list(trunk,envs.os,"os")
			create_list(trunk,envs.db,"databases")
			create_list(trunk,envs.lang,"languages")
			create_list(trunk,envs.fw,"frameworks")
			create_list(trunk,envs.mw,"middlewares")
			create_list(trunk,envs.tools,"tools")
			create_list(trunk,envs.pkg,"packages")

		base = et.Element("SkillData")
		tree = et.ElementTree(element=base)

		et.SubElement(base,"shain_num").text = self.data.shain_num
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

	def __init__(self,frame):
		self.frame = frame

	def read(self, target):
		filename = fd.askopenfilename(
		title = "個人基本情報読込",
		filetypes = FILE_TYPES,
		initialdir = INITIAL_DIR,
		defaultextension = DEFAULT_EXT
    )

		if filename != "":
			try:
				input = self.read_file(et.parse(filename)) 
				self.inputcheck(input)
				self.set_value(input)
				self.show_result(input, target)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
    
	#XML読込
	def read_file(self, tree) -> dict:
		# XMLを取得
		root = tree.getroot()
  
		def read_env(tree):
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
			for key in keys:
				subtree = tree.find(key[0])
				for value in subtree.iter("value"):
					ret[key[1]].append(value.text)
			return ret

		#単体項目を取得
		vals = {
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
		for value in sikaku.iter("value"):
			list_qual.append(value.text)
		vals["qualifications"]["value"] = list_qual

		#使用経験環境を取得
		vals["environments"]={"label":"使用経験(業務外)"}
		vals["environments"]["value"] = read_env(root.find("environments"))

		print(vals)
		return vals

	#データ入力
	def inputcheck(self, input:dict):
		sval.in_date_check(input["expr_start"])
		sval.in_regex_match(input["absense_year"],"[0-9]*","数字")
		sval.in_number_between(input["absense_month"],0,11,"0から11の間")
		sval.io_novalidation(input["specialty"])
		sval.io_novalidation(input["qualifications"])
		sval.io_novalidation(input["environments"])
		sval.io_novalidation(input["pr"])

	def set_value(self, input):
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

	#ファイル読み込み結果表示
	def show_result(self, input,target):
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
		for i in range(len(results)):
			frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg="white"))
			frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg=COLOR[results[i][1]["result"]]))
			frame_name[i].grid(row=i,column=0,sticky=tk.EW)
			frame_result[i].grid(row=i,column=1,sticky=tk.EW)
			tk.Label(frame_name[i],text=results[i][1]["label"],bg="white").pack(side=tk.LEFT,padx=3,pady=3)
			tk.Label(frame_result[i],text=results[i][1]["msg"],bg=COLOR[results[i][1]["result"]]).pack(side=tk.LEFT,padx=3,pady=3)
		frame_main_inner.columnconfigure(index=1, weight=1)
		button_ok["command"] = lambda: subwindow.destroy()