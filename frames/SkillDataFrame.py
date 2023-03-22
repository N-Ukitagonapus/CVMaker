'''
技術情報フレーム
'''
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")

		##1行目
		self.first_line=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_expr = tk.Label(self.first_line,text="業界経験")
		self.label_expr_yr = tk.Label(self.first_line,text="年")
		self.label_expr_mth = tk.Label(self.first_line,text="月")
  
		#業界経験-年
		self.text_expr_year = ttk.Entry(self.first_line, width=5)
		#業界経験-月
		self.select_expr_month = ttk.Combobox(self.first_line,width=3,state="readonly",justify="center",value=[i for i in range(1,13)])
  	#読込ボタン
		self.btn_load = tk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = tk.Button(self.first_line,width=5,text="保存")

		#組立
		self.label_expr.pack(side=tk.LEFT,padx=5)
		self.text_expr_year.pack(side=tk.LEFT,padx=5)
		self.label_expr_yr.pack(side=tk.LEFT,padx=5)
		self.select_expr_month.pack(side=tk.LEFT,padx=5)
		self.label_expr_mth.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X)
		##1行目ここまで

		##2行目
		self.second_line=tk.Frame(self.ret)
		#フレーム・ラベル定義
		self.label_specialty = tk.Label(self.second_line,text="得意分野")
		#得意分野
		self.text_specialty = ttk.Entry(self.second_line,width=100)

		#組立
		self.label_specialty.pack(side=tk.LEFT,padx=5)
		self.text_specialty.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X)

		#3行目
		self.third_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_qualifications = tk.Label(self.third_line,text="取得資格")
		self.label_kaigyokugiri = tk.Label(self.third_line,text="※複数ある場合は改行で区切ってください。")
		#取得資格
		self.text_qualifications  = scrolledtext.ScrolledText(self.third_line,  wrap = tk.WORD, width = 80,height = 5)  

		#組立
		self.label_qualifications.grid(row=0,column=0,padx=5,pady=5)
		self.label_kaigyokugiri.grid(row=0,column=1,padx=5,pady=5)
		self.text_qualifications.grid(row=1,column=1,padx=5,sticky=tk.EW)
		self.third_line.grid_columnconfigure(1, weight=1)
		self.third_line.pack(side=tk.TOP,fill=tk.X)
  
	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=10)