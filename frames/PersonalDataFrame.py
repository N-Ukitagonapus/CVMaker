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
from utils.Validation import Validation as validation

class PersonalDataFrame(tk.Frame):
	def __init__(self, target):
		self.data=PersonalData

		self.area_define(target)
		self.input_control(target)
		self.assembly()

	#エリア定義
	def area_define(self, target):
		#バリデーション定義
		is_numeric = target.register(validation.is_numeric)
		validate_romaji = target.register(validation.validate_romaji)
		length_limit = target.register(validation.length_limit)
  
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "個人基本情報")
		#1行目
		self.first_line=tk.Frame(self.ret)
		##フレーム・ラベル定義
		self.frame_shain_num = tk.Frame(self.first_line)
		self.label_shain_num = tk.Label(self.frame_shain_num,text="社員番号")
		##社員番号
		self.text_shain_num = ttk.Entry(self.frame_shain_num, width=5,
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
				  validatecommand =(length_limit, '%P', 10),
					validate="key")
		self.text_mei_kanji = ttk.Entry(self.second_line, width=20,
				  validatecommand =(length_limit, '%P', 10),
					validate="key")
		##名前(ローマ字)
		self.text_shi_romaji = ttk.Entry(self.second_line, width=20,
				  validatecommand =(validate_romaji, '%P', 15),
					validate="key")
		self.text_mei_romaji = ttk.Entry(self.second_line, width=20,
				  validatecommand =(validate_romaji, '%P', 15),
					validate="key")
 		##名前(性別)
		self.gender_val=StringVar()
		self.gender_male = ttk.Radiobutton(self.second_line,text="男",value="男",variable=self.gender_val)
		self.gender_female = ttk.Radiobutton(self.second_line,text="女",value="女",variable=self.gender_val)
		##生年月日
		self.birthday_entry = DateEntry(self.second_line)
		#2行目ここまで

		#3行目
		self.third_line = tk.Frame(self.ret)
  	##フレーム・ラベル定義
		self.label_address = tk.Label(self.third_line,text="現住所(市・区まで)")
		self.label_station = tk.Label(self.third_line,text="最寄り駅")
		##現住所
		self.text_address = ttk.Entry(self.third_line, width=40)
		##最寄り駅
		self.text_station = ttk.Entry(self.third_line, width=40)
		#3行目ここまで

		#4行目
		self.fourth_line = tk.Frame(self.ret)
  	#フレーム・ラベル定義
		self.label_academic = tk.Label(self.fourth_line,text="最終学歴")
		#最終学歴
		self.text_academic = ttk.Entry(self.fourth_line, width=60)
		#4行目ここまで



	#入力コントロール
	def input_control(self,target):

		self.btn_load["command"] = lambda: msg.showinfo("Message", "Load Button Has been pushed.")
		self.btn_save["command"] = lambda: save()
  
		def save():
			nenrei = util.get_year_sub(self.birthday_entry.get_date(), datetime.date.today())
			msg.showinfo("Save Test", "あなたの年齢は " + str(nenrei) +" 才ですな。")

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

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)