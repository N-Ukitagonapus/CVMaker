import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import xml.etree.ElementTree as et

from data_structure.PersonalData import PersonalData

from utils.Utilities import Utilities as util
from utils.Validation import StaticValidation as sval

from constants.const import COLOR, VALID_ERR, VALID_OK
from constants.message import DialogMessage as diag

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"

class PersonalDataOutput():

	def __init__(self, data:PersonalData):
		self.data = data

	def validate(self) -> dict:
		vals = {
			"shain_num":{"label":"社員番号"},
			"name_kanji":{"label":"氏名(漢字)"},
			"name_romaji":{"label":"氏名(ローマ字)"},
			"gender":{"label":"性別"},
			"birthday":{"label":"誕生日"},
			"address":{"label":"現住所"},
			"station":{"label":"最寄り駅"},
			"gakureki":{"label":"最終学歴"}
			}
		sval.out_regex_match(vals["shain_num"], r"[0-9]{3}","数字3桁", self.data.shain_num.get())
		sval.out_is_not_empty(vals["name_kanji"], self.data.name_last_kanji.get(), self.data.name_first_kanji.get())
		sval.out_regex_match(vals["name_romaji"], r"^[a-zA-Z]+$", "英字各15桁以内", self.data.name_last_romaji.get(), self.data.name_first_romaji.get())
		sval.out_is_not_empty(vals["gender"], self.data.gender.get())
		sval.out_date_check(vals["birthday"], self.data.birthday)
		sval.out_is_not_empty(vals["address"], self.data.current_address.get())			
		sval.out_is_not_empty(vals["station"], self.data.nearest_station.get())
		sval.out_is_not_empty(vals["gakureki"], self.data.gakureki.get())
		return vals

	def rock_items(self, frame, res):
		frame.text_shain_num["state"] = tk.DISABLED if res["shain_num"]["result"] == VALID_OK else tk.NORMAL
		frame.text_shi_kanji["state"] = tk.DISABLED if res["name_kanji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_mei_kanji["state"] = tk.DISABLED if res["name_kanji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_shi_romaji["state"] = tk.DISABLED if res["name_romaji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_mei_romaji["state"] = tk.DISABLED if res["name_romaji"]["result"] == VALID_OK else tk.NORMAL
		frame.gender_male["state"] = tk.DISABLED if res["gender"]["result"] == VALID_OK else tk.NORMAL
		frame.gender_female["state"] = tk.DISABLED if res["gender"]["result"] == VALID_OK else tk.NORMAL
		frame.birthday_entry["state"] = tk.DISABLED if res["birthday"]["result"] == VALID_OK else tk.NORMAL
		frame.text_address["state"] = tk.DISABLED if res["address"]["result"] == VALID_OK else tk.NORMAL
		frame.text_station["state"] = tk.DISABLED if res["station"]["result"] == VALID_OK else tk.NORMAL
		frame.text_academic["state"] = tk.DISABLED if res["gakureki"]["result"] == VALID_OK else tk.NORMAL
		frame.btn_edit["state"] = tk.NORMAL
   
	def confirm(self, target:tk.Frame, cntrl:tk.Frame):

		vals = self.validate()
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

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "個人基本情報 データ出力")
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
			subwindow.destroy()

		def do_output():
			try:
				self.output()
				self.rock_items(cntrl, vals)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)

		def cancel():
			subwindow.destroy()

	def output(self):
		base = et.Element("PersonalData")
		tree = et.ElementTree(element=base)

		if self.data.shain_num.get() != "":
			et.SubElement(base,"shain_num").text = self.data.shain_num.get()
		if self.data.name_last_kanji.get() != "":
			et.SubElement(base,"last_name_kanji").text = self.data.name_last_kanji.get()
		if self.data.name_first_kanji.get() != "":
			et.SubElement(base,"first_name_kanji").text = self.data.name_first_kanji.get()
		if self.data.name_last_romaji.get() != "":
			et.SubElement(base,"last_name_romaji").text = self.data.name_last_romaji.get()
		if self.data.name_first_romaji.get() != "":
			et.SubElement(base,"first_name_romaji").text = self.data.name_first_romaji.get()
		if self.data.gender.get() != "":
			et.SubElement(base,"gender").text = self.data.gender.get()
		et.SubElement(base,"birthday").text = self.data.birthday.strftime("%Y%m%d")
		if self.data.current_address.get() != "":
			et.SubElement(base,"current_address").text = self.data.current_address.get()
		if self.data.nearest_station.get() != "":
			et.SubElement(base,"nearest_station").text = self.data.nearest_station.get()
		if self.data.gakureki.get() != "":
			et.SubElement(base,"gakureki").text = self.data.gakureki.get()
		et.indent(tree,"\t")

		filename = fd.asksaveasfilename(
			title = "個人基本情報保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			defaultextension = DEFAULT_EXT
		)
		if filename != "":
			tree.write(filename, encoding="utf-8", xml_declaration=True)

class PersonalDataInput():
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
				self.rock_items(input)
				self.show_result(input, target)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)

	def read_file(self, tree) -> dict:
		"""
			ファイル読込
		Args:
				tree ElementTree: 読込ファイルデータ

		Returns:
				dict:XML解析結果
		"""
		# XMLを取得
		self.root = tree.getroot()
   
		vals = {
			"shain_num":{"label":"社員番号"},
			"last_name_kanji":{"label":"氏(漢字)"},
			"first_name_kanji":{"label":"名(漢字)"},
			"last_name_romaji":{"label":"氏(ローマ字)"},
			"first_name_romaji":{"label":"名(ローマ字)"},
			"gender":{"label":"性別"},
			"birthday":{"label":"誕生日"},
			"current_address":{"label":"現住所"},
			"nearest_station":{"label":"最寄り駅"},
			"gakureki":{"label":"最終学歴"}
			}
		keys = list(vals.keys())
		for key in keys:
			text = self.root.find(key)
			if text is not None:
				vals[key]["value"] = text.text
			else:
				vals[key]["value"] = None
		print(vals)
		return vals

	def inputcheck(self, input:dict):
		""" 
  		読込結果チェック
		Args:
				input (dict): XML解析結果
		"""
		sval.in_regex_match(input["shain_num"],"[0-9]{3}","数字3桁")
		sval.in_maxlength_check(input["last_name_kanji"],20)
		sval.in_maxlength_check(input["first_name_kanji"],20)
		sval.in_regex_and_length(input["last_name_romaji"],20,"[a-zA-Z]*","英字")
		sval.in_regex_and_length(input["first_name_romaji"],20,"[a-zA-Z]*","英字")
		sval.in_regex_match(input["gender"],"(男|女)","「男」または「女」")
		sval.in_date_check(input["birthday"])
		sval.in_is_not_empty(input["current_address"])			
		sval.in_is_not_empty(input["nearest_station"])
		sval.in_is_not_empty(input["gakureki"])

	def set_value(self, input):
		data = self.frame.data
		util.setstr_from_read(data.shain_num,input["shain_num"])
		util.setstr_from_read_cut(data.name_last_kanji,input["last_name_kanji"],20)
		util.setstr_from_read_cut(data.name_first_kanji,input["first_name_kanji"],20)
		util.setstr_from_read_cut(data.name_last_romaji,input["last_name_romaji"],20)
		util.setstr_from_read_cut(data.name_first_romaji,input["first_name_romaji"],20)
		util.setstr_from_read(data.gender,input["gender"])
		util.setdate_from_read(self.frame.birthday_entry,input["birthday"])
		data.birthday = self.frame.birthday_entry.get_date()
		util.setstr_from_read(data.current_address,input["current_address"])
		util.setstr_from_read(data.nearest_station,input["nearest_station"])
		util.setstr_from_read(data.gakureki,input["gakureki"])

	def rock_items(self, input):
		frame = self.frame
		frame.text_shain_num["state"] = tk.DISABLED if input["shain_num"]["result"] == VALID_OK else tk.NORMAL
		frame.text_shi_kanji["state"] = tk.DISABLED if input["last_name_kanji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_mei_kanji["state"] = tk.DISABLED if input["first_name_kanji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_shi_romaji["state"] = tk.DISABLED if input["last_name_romaji"]["result"] == VALID_OK else tk.NORMAL
		frame.text_mei_romaji["state"] = tk.DISABLED if input["first_name_romaji"]["result"] == VALID_OK else tk.NORMAL
		frame.gender_male["state"] = tk.DISABLED if input["gender"]["result"] == VALID_OK else tk.NORMAL
		frame.gender_female["state"] = tk.DISABLED if input["gender"]["result"] == VALID_OK else tk.NORMAL
		frame.birthday_entry["state"] = tk.DISABLED if input["birthday"]["result"] == VALID_OK else tk.NORMAL
		frame.text_address["state"] = tk.DISABLED if input["current_address"]["result"] == VALID_OK else tk.NORMAL
		frame.text_station["state"] = tk.DISABLED if input["nearest_station"]["result"] == VALID_OK else tk.NORMAL
		frame.text_academic["state"] = tk.DISABLED if input["gakureki"]["result"] == VALID_OK else tk.NORMAL
		frame.btn_edit["state"] = tk.NORMAL

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

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "個人基本情報 ファイル読込結果")
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

