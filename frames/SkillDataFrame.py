'''
技術情報フレーム
'''
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
from constants.const import ENV_GENRE

class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")

		##1行目
		self.first_line=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_expr = tk.Label(self.first_line,text="業界経験開始年月")
		self.label_absense = tk.Label(self.first_line,text="休職期間")
		self.label_absense_yr = tk.Label(self.first_line,text="年")
		self.label_absense_mth = tk.Label(self.first_line,text="月")
  
		#業界経験開始年月
		self.expr_start = DateEntry(self.first_line)
		#休職期間-年
		self.text_absense_year = ttk.Entry(self.first_line, width=5)
		#休職期間-月
		self.select_absense_month = ttk.Combobox(self.first_line,width=3,state="readonly",justify="center",value=[i for i in range(1,13)])
  	#読込ボタン
		self.btn_load = tk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = tk.Button(self.first_line,width=5,text="保存")

		#組立
		self.label_expr.pack(side=tk.LEFT,padx=5)
		self.expr_start.pack(side=tk.LEFT,padx=5)
		self.label_absense.pack(side=tk.LEFT,padx=5)
		self.text_absense_year.pack(side=tk.LEFT,padx=5)
		self.label_absense_yr.pack(side=tk.LEFT,padx=5)
		self.select_absense_month.pack(side=tk.LEFT,padx=5)
		self.label_absense_mth.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=5)
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
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=5)

		#3行目
		self.third_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_qualifications = tk.Label(self.third_line,text="取得資格")
		self.label_kaigyokugiri = tk.Label(self.third_line,text="※複数ある場合は改行で区切ってください。")
		#取得資格
		self.text_qualifications  = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)  

		#組立
		self.label_qualifications.grid(row=0,column=0,padx=5,pady=5)
		self.label_kaigyokugiri.grid(row=0,column=1,padx=5,pady=5)
		self.text_qualifications.grid(row=1,column=1,padx=5,sticky=tk.EW)
		self.third_line.grid_columnconfigure(1, weight=1)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=5)
		
    #4行目
		self.fourth_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_environments = tk.Label(self.fourth_line,text="使用経験\n(業務外)")

		#使用経験
		self.btn_env_edit = tk.Button(self.fourth_line,width=5,text="編集")

		#組立
		self.label_environments.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#5行目
		self.fifth_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_pr = tk.Label(self.fifth_line,text="自己PR")
		#取得資格
		self.text_pr  = scrolledtext.ScrolledText(self.fifth_line,wrap=tk.WORD,width=80,height=5)  

		#組立
		self.label_pr.grid(row=0,column=0,padx=5,pady=5)
		self.text_pr.grid(row=1,column=1,padx=5,sticky=tk.EW)
		self.fifth_line.grid_columnconfigure(1, weight=1)
		self.fifth_line.pack(side=tk.TOP,fill=tk.X,pady=5)

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)