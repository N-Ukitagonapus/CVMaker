'''
技術情報フレーム
'''
from datetime import datetime
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
from constants.const import COLOR, ENV_GENRE, ENV_SET, VALID_ERR, VALID_OK
from fileio.SkillDataIO import SkillDataInput, SkillDataOutput
from frames.subframe.EnvironmentSubFrame import EnvironmentSubFrame
from utils.Utilities import Utilities as util
from tkinter import messagebox as msg
from data_structure.SkillData import SkillData
from utils.Validation import DynamicValidation as dval
from utils.Validation import StaticValidation as sval
from constants.message import DialogMessage as diag

class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.data = SkillData()
		self.area_define(target)
		self.input_control(target)
		self.assembly()
  
	#エリア定義
	def area_define(self, target):
		#バリデーション定義
		is_numeric = target.register(dval.is_numeric)

		self.ret = tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")
		##1行目
		self.first_line=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_expr = tk.Label(self.first_line,text="業界経験開始年月")
		self.label_absense = tk.Label(self.first_line,text="休職期間")
		self.label_absense_yr = tk.Label(self.first_line,text="年")
		self.label_absense_mth = tk.Label(self.first_line,text="月")
  
		#業界経験開始年月
		self.str_start_date = StringVar()
		self.expr_start = DateEntry(self.first_line,day=1,locale='ja_JP',date_pattern='yyyy/mm/dd',textvariable=self.str_start_date)
		#休職期間-年
		self.text_absense_year = ttk.Entry(self.first_line, width=5,
				    textvariable=self.data.period_absense_year,
				 		validatecommand = (is_numeric, '%P', 3),
						validate='key')
		#休職期間-月
		self.select_absense_month = ttk.Combobox(self.first_line,width=3,state="readonly",justify="center",value=[i for i in range(0,12)],
				     textvariable=self.data.period_absense_month)
  	#読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")

		##2行目
		self.second_line=tk.Frame(self.ret)
		#フレーム・ラベル定義
		self.label_specialty = tk.Label(self.second_line,text="得意分野")
		#得意分野
		self.text_specialty = ttk.Entry(self.second_line,width=100,
				    	textvariable=self.data.specialty)

		#3行目
		self.third_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_qualifications = tk.Label(self.third_line,text="取得資格")
		self.label_environments = tk.Label(self.third_line,text="使用経験\n(業務外)")
  
		#取得資格
		self.btn_qual_edit = ttk.Button(self.third_line,width=5,text="編集")  

		#使用経験
		self.btn_env_edit = ttk.Button(self.third_line,width=5,text="編集")

		#4行目
		self.fourth_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_pr = tk.Label(self.fourth_line,text="自己PR")
		#自己PR
		self.text_pr = scrolledtext.ScrolledText(self.fourth_line,wrap=tk.WORD,width=80,height=5)  

	#組み立て
	def assembly(self):
		#1行目
		self.label_expr.pack(side=tk.LEFT)
		util.mark_required(self.first_line,self.label_expr)
		self.expr_start.pack(side=tk.LEFT,padx=5)
		self.label_absense.pack(side=tk.LEFT,padx=5)
		self.text_absense_year.pack(side=tk.LEFT,padx=5)
		self.label_absense_yr.pack(side=tk.LEFT,padx=5)
		self.select_absense_month.pack(side=tk.LEFT,padx=5)
		self.label_absense_mth.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=5)

		#2行目
		self.label_specialty.pack(side=tk.LEFT)
		self.text_specialty.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=5)
  
		#3行目
		self.label_qualifications.pack(side=tk.LEFT)
		self.btn_qual_edit.pack(side=tk.LEFT,padx=5)
		self.label_environments.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#4行目
		self.label_pr.grid(row=0,column=0,pady=5)
		self.text_pr.grid(row=1,column=1,padx=5,pady=5,sticky=tk.EW)
		self.fourth_line.grid_columnconfigure(1, weight=1)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)
  
	#入力コントロール
	def input_control(self,target):
		
		def expr_start_set(*args):
			try:
				date_conv = util.get_first_date(datetime.strptime(self.str_start_date.get(),"%Y/%m/%d"))
				self.expr_start.set_date(date_conv)
				self.data.expr_start=date_conv
			except ValueError:
				return
		def set_pr(event):
			self.data.pr=self.text_pr.get('1.0',self.text_pr.index(tk.END))
		self.btn_load["command"] = lambda: self.data_read(target)
		self.btn_save["command"] = lambda: self.data_save(target)
		self.btn_qual_edit["command"] = lambda:self.edit_qualifications(self.ret)
		self.btn_env_edit["command"]  = lambda:EnvironmentSubFrame().edit_envs(target, "使用経験編集", self.data.expr_env)
		self.str_start_date.trace('w',expr_start_set)
		self.text_pr.bind("<FocusOut>",func = set_pr)
	
	#データ出力
	def data_save(self,target):
		io = SkillDataOutput(self.data)
		io.confirm(target)
		del io

	#データ読込
	def data_read(self,target):
		io = SkillDataInput(self)
		io.read(target)
		del io
		


	#取得資格編集サブウィンドウ
	def edit_qualifications(self,target):
		subwindow = tk.Toplevel(target)
		subwindow.title("資格情報編集")
		subwindow.geometry("320x320")
		subwindow.resizable(False,False)
		subwindow.grab_set()
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="取得資格編集", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		label_desc= tk.Label(subwindow, text="複数ある場合は改行区切りで入力してください。")
		label_desc.pack(side=tk.TOP,pady=5)
		text= scrolledtext.ScrolledText(subwindow,wrap=tk.WORD)
		text.insert('1.0',"\n".join(self.data.qualifications))
		text.pack(side=tk.TOP,fill=tk.X,expand=True,padx=20,pady=5)

		btn_ok["command"] = lambda: update()
		btn_cancel["command"] = lambda: cancel()

		def update():
			self.data.qualifications = util.tidy_list((str.strip(text.get('1.0',text.index(tk.END)))).split("\n"))
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)