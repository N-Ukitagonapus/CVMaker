'''
個人基本情報フレーム
'''
import datetime
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import StringVar, ttk

from data_structure.PersonalData import PersonalData
from tkinter import messagebox as msg

from utils.Utilities import Utilities as util
from utils.Validation import DynamicValidation as dval
from utils.Validation import StaticValidation as sval

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
		validate_romaji = target.register(dval.validate_romaji)
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
					validate='key')
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
				  validatecommand =(validate_romaji, '%P', 15),
					validate='key')
		self.text_mei_romaji = ttk.Entry(self.second_line, width=20,
				  textvariable=self.data.name_first_romaji,
				  validatecommand =(validate_romaji, '%P', 15),
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
		self.btn_load["command"] = lambda: msg.showinfo("Message", "Load Button Has been pushed.")
		self.btn_save["command"] = lambda: self.data_confirm(target)

	#データ出力
	def data_confirm(self,target):


		def final_validation(input_data: PersonalData):
			input_data.birthday=self.birthday_entry.get_date()
			sval.regex_match(vals["shain_num"],input_data.shain_num.get(),"[0-9]{3}","数字3桁")
			sval.is_not_empty(vals["name_kanji"],input_data.name_last_kanji.get(),input_data.name_first_kanji.get())
			sval.is_not_empty(vals["name_romaji"],input_data.name_last_romaji.get(),input_data.name_first_romaji.get())
			sval.is_not_empty(vals["gender"],input_data.gender.get())
			sval.date_check(vals["birthday"],input_data.birthday)
			sval.is_not_empty(vals["address"],input_data.current_address.get())			
			sval.is_not_empty(vals["station"],input_data.nearest_station.get())
			sval.is_not_empty(vals["gakureki"],input_data.gakureki.get())

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
			if val["result"] == False:
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
			frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID))
			frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID))
			frame_name[i].grid(row=i,column=0,sticky=tk.EW)
			frame_result[i].grid(row=i,column=1,sticky=tk.EW)
			tk.Label(frame_name[i],text=results[i][1]["label"]).pack(side=tk.LEFT,padx=3,pady=3)
			tk.Label(frame_result[i],text=results[i][1]["msg"],fg="#000000" if results[i][1]["result"] == True else "#ff0000").pack(side=tk.LEFT,padx=3,pady=3)
		frame_main_inner.columnconfigure(index=1, weight=1)	

	# フレーム描写
	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)