'''
個人基本情報フレーム
'''
import datetime
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import  BooleanVar, ttk
from constants.const import COLOR, VALID_ERR, VALID_OK

from data_structure.PersonalData import PersonalData

from fileio.PersonalDataIO import PersonalDataInput, PersonalDataOutput

from utils.Utilities import Utilities as util
from utils.Validation import DynamicValidation as dval
from utils.Validation import StaticValidation as sval

from constants.message import DialogMessage as diag
class PersonalDataFrame(tk.Frame):
	def __init__(self, target):
		self.data=PersonalData()

		self.area_define(target)
		self.input_control(target)
		self.assembly()

	#エリア定義
	def area_define(self, target):
		#バリデーション定義
		is_numeric = target.register(dval.is_numeric)
		length_limit = target.register(dval.length_limit)
  
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "個人基本情報")
		#1行目
		self.first_line=tk.Frame(self.ret)
		##フレーム・ラベル定義
		self.frame_shain_num = tk.Frame(self.first_line)
		self.label_shain_num = tk.Label(self.frame_shain_num,text="社員番号")
		##社員番号
		self.text_shain_num = ttk.Entry(self.frame_shain_num, width=5,
				  textvariable=self.data.shain_num,
				  validatecommand =(is_numeric, '%P', 3),
					validate='all')
		##編集ボタン
		self.btn_edit = ttk.Button(self.first_line,width=5,text="編集",state=tk.DISABLED)
		##読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		##保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")
		##1行目ここまで

		#2行目
		self.second_line = tk.Frame(self.ret)
  	##フレーム・ラベル定義
		self.label_shimei_kanji = tk.Label(self.second_line,text="氏名(漢字)")
		self.label_shimei_romaji = tk.Label(self.second_line,text="氏名(ローマ字)")
		self.label_birthday = tk.Label(self.second_line,text="生年月日")
		##名前(漢字)
		self.text_shi_kanji = ttk.Entry(self.second_line, width=20,
				  textvariable=self.data.name_last_kanji,
				  validatecommand = (length_limit, '%P', 10),
					validate='key')
		self.text_mei_kanji = ttk.Entry(self.second_line, width=20,
				  textvariable=self.data.name_first_kanji,
				  validatecommand = (length_limit, '%P', 10),
					validate='key')
		##名前(ローマ字)
		self.text_shi_romaji = ttk.Entry(self.second_line, width=20,
				  textvariable=self.data.name_last_romaji,
				  validatecommand =(length_limit, '%P', 15),
					validate='key')
		self.text_mei_romaji = ttk.Entry(self.second_line, width=20,
				  textvariable=self.data.name_first_romaji,
				  validatecommand =(length_limit, '%P', 15),
					validate='key')
 		##名前(性別)
		self.gender_male = ttk.Radiobutton(self.second_line,text="男",value="男",variable=self.data.gender)
		self.gender_female = ttk.Radiobutton(self.second_line,text="女",value="女",variable=self.data.gender)
		##生年月日
		self.birthday_entry = DateEntry(self.second_line,locale='ja_JP',date_pattern='yyyy/mm/dd')
		#2行目ここまで

		#3行目
		self.third_line = tk.Frame(self.ret)
  	##フレーム・ラベル定義
		self.label_address = tk.Label(self.third_line,text="現住所(市・区まで)")
		self.label_station = tk.Label(self.third_line,text="最寄り駅")
		##現住所
		self.text_address = ttk.Entry(self.third_line, width=40,textvariable=self.data.current_address)
		##最寄り駅
		self.text_station = ttk.Entry(self.third_line, width=40,textvariable=self.data.nearest_station)
		#3行目ここまで

		#4行目
		self.fourth_line = tk.Frame(self.ret)
  	#フレーム・ラベル定義
		self.label_academic = tk.Label(self.fourth_line,text="最終学歴")
		#最終学歴
		self.text_academic = ttk.Entry(self.fourth_line, width=60,textvariable=self.data.gakureki)
		#4行目ここまで

	#組み立て
	def assembly(self):
			#1行目
		self.label_shain_num.pack(side=tk.LEFT)
		util.mark_required(self.frame_shain_num,self.label_shain_num)
		self.text_shain_num.pack(side=tk.LEFT,padx=10)
		self.frame_shain_num.pack(side=tk.LEFT)
		self.btn_edit.pack(side=tk.RIGHT,padx=10)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#2行目
		self.label_shimei_kanji.pack(side=tk.LEFT)
		util.mark_required(self.second_line,self.label_shimei_kanji)
		self.text_shi_kanji.pack(side=tk.LEFT,padx=5)
		self.text_mei_kanji.pack(side=tk.LEFT,padx=5)
		self.label_shimei_romaji.pack(side=tk.LEFT)
		util.mark_required(self.second_line,self.label_shimei_romaji)
		self.text_shi_romaji.pack(side=tk.LEFT,padx=5)
		self.text_mei_romaji.pack(side=tk.LEFT,padx=5)
		self.gender_male.pack(side=tk.LEFT,padx=5)
		self.gender_female.pack(side=tk.LEFT,padx=5)
		self.label_birthday.pack(side=tk.LEFT,padx=5)
		util.mark_required(self.second_line,self.label_birthday)
		self.birthday_entry.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=2)
  
		#3行目
		self.label_address.pack(side=tk.LEFT)
		util.mark_required(self.third_line,self.label_address)
		self.text_address.pack(side=tk.LEFT,padx=5)
		self.label_station.pack(side=tk.LEFT,padx=5)
		util.mark_required(self.third_line,self.label_station)
		self.text_station.pack(side=tk.LEFT,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#4行目
		self.label_academic.pack(side=tk.LEFT)
		util.mark_required(self.fourth_line,self.label_academic)
		self.text_academic.pack(side=tk.LEFT,padx=5)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)

	#入力コントロール
	def input_control(self,target):
		def birthday_set(event):
			self.data.birthday=self.birthday_entry.get_date()
		self.btn_load["command"] = lambda: self.data_read(target)
		self.btn_save["command"] = lambda: self.data_confirm(target)
		self.btn_edit["command"] = lambda: self.reactivate_items(target)
		self.birthday_entry.bind("<FocusOut>",func = birthday_set)

	#データ出力
	def data_confirm(self,target):
		def final_validation(input_data: PersonalData):
			sval.out_regex_match(vals["shain_num"],r"[0-9]{3}","数字3桁",input_data.shain_num.get())
			sval.out_is_not_empty(vals["name_kanji"],input_data.name_last_kanji.get(),input_data.name_first_kanji.get())
			sval.out_regex_match(vals["name_romaji"],r"^[a-zA-Z]+$","英字各15桁以内",input_data.name_last_romaji.get(),input_data.name_first_romaji.get())
			sval.out_is_not_empty(vals["gender"],input_data.gender.get())
			sval.out_date_check(vals["birthday"],input_data.birthday)
			sval.out_is_not_empty(vals["address"],input_data.current_address.get())			
			sval.out_is_not_empty(vals["station"],input_data.nearest_station.get())
			sval.out_is_not_empty(vals["gakureki"],input_data.gakureki.get())

		def rock_items(res):
			self.text_shain_num["state"] = tk.DISABLED if res["shain_num"]["result"] == VALID_OK else tk.NORMAL
			self.text_shi_kanji["state"] = tk.DISABLED if res["name_kanji"]["result"] == VALID_OK else tk.NORMAL
			self.text_mei_kanji["state"] = tk.DISABLED if res["name_kanji"]["result"] == VALID_OK else tk.NORMAL
			self.text_shi_romaji["state"] = tk.DISABLED if res["name_romaji"]["result"] == VALID_OK else tk.NORMAL
			self.text_mei_romaji["state"] = tk.DISABLED if res["name_romaji"]["result"] == VALID_OK else tk.NORMAL
			self.gender_male["state"] = tk.DISABLED if res["gender"]["result"] == VALID_OK else tk.NORMAL
			self.gender_female["state"] = tk.DISABLED if res["gender"]["result"] == VALID_OK else tk.NORMAL
			self.birthday_entry["state"] = tk.DISABLED if res["birthday"]["result"] == VALID_OK else tk.NORMAL
			self.text_address["state"] = tk.DISABLED if res["address"]["result"] == VALID_OK else tk.NORMAL
			self.text_station["state"] = tk.DISABLED if res["station"]["result"] == VALID_OK else tk.NORMAL
			self.text_academic["state"] = tk.DISABLED if res["gakureki"]["result"] == VALID_OK else tk.NORMAL
			self.btn_edit["state"] = tk.NORMAL
   
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

		def do_output():
			try:
				PersonalDataOutput(self.data).output()
				rock_items(vals)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	def data_read(self,target):
		def inputcheck(input:dict):
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

		def set_value(input):
			util.setstr_from_read(self.data.shain_num,input["shain_num"])
			util.setstr_from_read_cut(self.data.name_last_kanji,input["last_name_kanji"],20)
			util.setstr_from_read_cut(self.data.name_first_kanji,input["first_name_kanji"],20)
			util.setstr_from_read_cut(self.data.name_last_romaji,input["last_name_romaji"],20)
			util.setstr_from_read_cut(self.data.name_first_romaji,input["first_name_romaji"],20)
			util.setstr_from_read(self.data.gender,input["gender"])
			util.setdate_from_read(self.birthday_entry,input["birthday"])
			self.data.birthday = self.birthday_entry.get_date()
			util.setstr_from_read(self.data.current_address,input["current_address"])
			util.setstr_from_read(self.data.nearest_station,input["nearest_station"])
			util.setstr_from_read(self.data.gakureki,input["gakureki"])

		def rock_items(input):
			self.text_shain_num["state"] = tk.DISABLED if input["shain_num"]["result"] == VALID_OK else tk.NORMAL
			self.text_shi_kanji["state"] = tk.DISABLED if input["last_name_kanji"]["result"] == VALID_OK else tk.NORMAL
			self.text_mei_kanji["state"] = tk.DISABLED if input["first_name_kanji"]["result"] == VALID_OK else tk.NORMAL
			self.text_shi_romaji["state"] = tk.DISABLED if input["last_name_romaji"]["result"] == VALID_OK else tk.NORMAL
			self.text_mei_romaji["state"] = tk.DISABLED if input["first_name_romaji"]["result"] == VALID_OK else tk.NORMAL
			self.gender_male["state"] = tk.DISABLED if input["gender"]["result"] == VALID_OK else tk.NORMAL
			self.gender_female["state"] = tk.DISABLED if input["gender"]["result"] == VALID_OK else tk.NORMAL
			self.birthday_entry["state"] = tk.DISABLED if input["birthday"]["result"] == VALID_OK else tk.NORMAL
			self.text_address["state"] = tk.DISABLED if input["current_address"]["result"] == VALID_OK else tk.NORMAL
			self.text_station["state"] = tk.DISABLED if input["nearest_station"]["result"] == VALID_OK else tk.NORMAL
			self.text_academic["state"] = tk.DISABLED if input["gakureki"]["result"] == VALID_OK else tk.NORMAL
			self.btn_edit["state"] = tk.NORMAL

		#ファイル読み込み結果表示
		def show_result(input,target):
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
   
		try:
			input = PersonalDataInput().read()
			inputcheck(input)
			set_value(input)
			rock_items(input)
			show_result(input, target)
		except Exception as e:
			print(e)
			util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)

	#項目再活性
	def reactivate_items(self,target):
		modes = {
			"name":BooleanVar(),
			"address":BooleanVar(),
			"all":BooleanVar()
		}
		check_modes={}

		subwindow = tk.Toplevel(target)
		subwindow.title("項目再活性")
		subwindow.geometry("300x300")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_ok = ttk.Button(frame_button_inner,width=10,text="OK")
		button_cancel = ttk.Button(frame_button_inner,width=10,text="キャンセル")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
		frame_button_inner.pack(pady=5)
		button_cancel.grid(row=0,column=0,padx=15)
		button_ok.grid(row=0,column=1,padx=15)

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "個人基本情報 再編集")
		frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
		frame_main_inner=tk.Frame(frame_main)
		frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)
		tk.Label(frame_main_inner,text="編集モードを選んでください。").pack(side=tk.TOP,padx=5,pady=5)

		check_modes["name"] =	tk.Checkbutton(frame_main_inner, variable=modes["name"], text="苗字変更\n(結婚等で苗字が変更された場合)")
		check_modes["address"] =	tk.Checkbutton(frame_main_inner, variable=modes["address"], text="住所および最寄り駅変更\n(引っ越し等で住所を変更した場合)")
		check_modes["all"] =	tk.Checkbutton(frame_main_inner, variable=modes["all"], text="全部変更\n(打ち間違いによる修正)\n※原則として推奨できません！")

		for chk in check_modes.values():
			chk.pack(anchor=tk.NW,padx=10,pady=5,fill=tk.X,expand="TRUE")
   
		def switch_state():
			check_modes["name"]["state"] = tk.DISABLED if modes["all"].get() else tk.NORMAL
			check_modes["address"]["state"] = tk.DISABLED if modes["all"].get() else tk.NORMAL
   
		def reactivate():
			if modes["all"].get():
				if util.msgbox_ask(diag.DIALOG_ASK_EDIT_PERSONALDATA):
					do_reactivate()
			else:
				do_reactivate()

		def do_reactivate():
			self.text_shain_num["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.text_shi_kanji["state"] =	 tk.NORMAL if modes["all"].get() or modes["name"].get() else tk.DISABLED
			self.text_mei_kanji["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.text_shi_romaji["state"] =	 tk.NORMAL if modes["all"].get() or modes["name"].get() else tk.DISABLED
			self.text_mei_romaji["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.gender_male["state"] =		 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.gender_female["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.birthday_entry["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.text_address["state"] =	 tk.NORMAL if modes["all"].get() or modes["address"].get() else tk.DISABLED
			self.text_station["state"] =	 tk.NORMAL if modes["all"].get() or modes["address"].get() else tk.DISABLED
			self.text_academic["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			subwindow.destroy()

		def cancel():
			subwindow.destroy()
   
		check_modes["all"]["command"] = lambda:switch_state()
		button_ok["command"] = lambda:reactivate()
		button_cancel["command"] = lambda: cancel()

	# フレーム描写
	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)
