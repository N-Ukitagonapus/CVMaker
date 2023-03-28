'''
個人基本情報フレーム
'''
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import StringVar, ttk

from data_structure.PersonalData import PersonalData
from tkinter import messagebox as msg

class PersonalDataFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "個人基本情報")

		self.data=PersonalData

		##1行目
		self.first_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.frame_shain_num = tk.Frame(self.first_line)
		self.label_shain_num = tk.Label(self.frame_shain_num,text="社員番号")
  
		#社員番号
		self.text_shain_num = ttk.Entry(self.frame_shain_num, width=5)
		#読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")

		#組み立て
		self.label_shain_num.pack(side=tk.LEFT)
		self.text_shain_num.pack(side=tk.LEFT,padx=10)
		self.frame_shain_num.pack(side=tk.LEFT)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=2)
		##1行目ここまで

		##2行目
		self.second_line = tk.Frame(self.ret)

  	#フレーム・ラベル定義
		self.label_shimei_kanji = tk.Label(self.second_line,text="氏名(漢字)")
		self.label_shimei_romaji = tk.Label(self.second_line,text="氏名(ローマ字)")
		self.label_birthday = tk.Label(self.second_line,text="生年月日")

		#名前(漢字)
		self.text_shi_kanji = ttk.Entry(self.second_line, width=20)
		self.text_mei_kanji = ttk.Entry(self.second_line, width=20)

		#名前(ローマ字)
		self.text_shi_romaji = ttk.Entry(self.second_line, width=20)
		self.text_mei_romaji = ttk.Entry(self.second_line, width=20)

 		#名前(性別)
		self.gender_val=StringVar()
		self.gender_male = ttk.Radiobutton(self.second_line,text="男",value=1,variable=self.gender_val)
		self.gender_female = ttk.Radiobutton(self.second_line,text="女",value=2,variable=self.gender_val)

		#生年月日
		self.birthday_entry = DateEntry(self.second_line)
  
		#組み立て
		self.label_shimei_kanji.pack(side=tk.LEFT)
		self.text_shi_kanji.pack(side=tk.LEFT,padx=5)
		self.text_mei_kanji.pack(side=tk.LEFT,padx=5)
		self.label_shimei_romaji.pack(side=tk.LEFT)
		self.text_shi_romaji.pack(side=tk.LEFT,padx=5)
		self.text_mei_romaji.pack(side=tk.LEFT,padx=5)
		self.gender_male.pack(side=tk.LEFT,padx=5)
		self.gender_female.pack(side=tk.LEFT,padx=5)
		self.label_birthday.pack(side=tk.LEFT,padx=5)
		self.birthday_entry.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=2)
		##2行目ここまで

		##3行目
		self.third_line = tk.Frame(self.ret)
  	#フレーム・ラベル定義
		self.label_address = tk.Label(self.third_line,text="現住所(市・区まで)")
		self.label_station = tk.Label(self.third_line,text="最寄り駅")
		#現住所
		self.text_address = ttk.Entry(self.third_line, width=40)
		#最寄り駅
		self.text_station = ttk.Entry(self.third_line, width=40)
  
		#組み立て
		self.label_address.pack(side=tk.LEFT)
		self.text_address.pack(side=tk.LEFT,padx=5)
		self.label_station.pack(side=tk.LEFT,padx=5)
		self.text_station.pack(side=tk.LEFT,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)
		##3行目ここまで

		##4行目
		self.fourth_line = tk.Frame(self.ret)
  	#フレーム・ラベル定義
		self.label_academic = tk.Label(self.fourth_line,text="最終学歴")
		#現住所
		self.text_academic = ttk.Entry(self.fourth_line, width=60)
		#組み立て
		self.label_academic.pack(side=tk.LEFT)
		self.text_academic.pack(side=tk.LEFT,padx=5)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		self.input_control()

	#ボタンコントロール
	def input_control(self):
		self.btn_load["command"] = lambda: msg.showinfo("Message", "Load Button Has been pushed.")
		self.btn_save["command"] = lambda: msg.showinfo("Message", "Save Button Has been pushed.")
  
	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)