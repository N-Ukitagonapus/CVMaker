'''
技術情報フレーム
'''
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
from constants.const import ENV_GENRE
from utils.Utilities import Utilities as util
from tkinter import messagebox as msg

from data_structure.SkillData import SkillData
class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.data = SkillData()
		self.data.qualifications = ["初級シスアド", "基本情報技術者", "英検2級", "Oracle Bronze 12c"]
   
		self.ret = tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")

		##1行目
		self.first_line=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_expr = tk.Label(self.first_line,text="業界経験開始年月")
		self.label_absense = tk.Label(self.first_line,text="休職期間")
		self.label_absense_yr = tk.Label(self.first_line,text="年")
		self.label_absense_mth = tk.Label(self.first_line,text="月")
  
		#業界経験開始年月
		self.expr_start = DateEntry(self.first_line,day=1,locale='ja_JP',date_pattern='yyyy/mm/dd')
		#休職期間-年
		self.text_absense_year = ttk.Entry(self.first_line, width=5)
		#休職期間-月
		self.select_absense_month = ttk.Combobox(self.first_line,width=3,state="readonly",justify="center",value=[i for i in range(0,12)])
  	#読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")

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
		self.label_environments = tk.Label(self.third_line,text="使用経験\n(業務外)")
  
		#取得資格
		self.btn_qual_edit = ttk.Button(self.third_line,width=5,text="編集")  

		#使用経験
		self.btn_env_edit = ttk.Button(self.third_line,width=5,text="編集")
  
		#組立
		self.label_qualifications.pack(side=tk.LEFT,padx=5)
		self.btn_qual_edit.pack(side=tk.LEFT,padx=5)
		self.label_environments.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#4行目
		self.fourth_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_pr = tk.Label(self.fourth_line,text="自己PR")
		#自己PR
		self.text_pr = scrolledtext.ScrolledText(self.fourth_line,wrap=tk.WORD,width=80,height=5)  

		#組立
		self.label_pr.grid(row=0,column=0,padx=5,pady=5)
		self.text_pr.grid(row=1,column=1,padx=5,sticky=tk.EW)
		self.fourth_line.grid_columnconfigure(1, weight=1)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		self.input_control()

	#ボタンコントロール
	def input_control(self):
		self.btn_load["command"] = lambda: msg.showinfo("Message", "Load Button Has been pushed.")
		self.btn_save["command"] = lambda: msg.showinfo("Message", "Save Button Has been pushed.")
		self.btn_qual_edit["command"] = lambda:self.edit_qualifications(self.ret)
		self.btn_env_edit["command"] = lambda:self.edit_environments(self.ret)

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
			self.data.qualifications = util.tidy_list((text.get('1.0',text.index(tk.END))).split("\n"))
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	#使用経験環境編集
	def edit_environments(self,target):
		subwindow = tk.Toplevel(target)
		subwindow.title("使用経験編集")
		subwindow.geometry("1000x320")
		subwindow.resizable(False,False)
		subwindow.grab_set()
  
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="使用経験編集", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)
  
		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		label_desc = tk.Label(subwindow, text="複数ある場合は改行区切りで入力してください。")
		label_desc.pack(side=tk.TOP,pady=5)

		frame_edit = tk.Frame(subwindow)
		envs = list(ENV_GENRE.items())
		label_envs={}
		text_envs={}
		for i in range(len(envs)):
			label_envs[envs[i][0]]=tk.Label(frame_edit, text=envs[i][1])
			text_envs[envs[i][0]]=scrolledtext.ScrolledText(frame_edit,wrap=tk.WORD)
			text_envs[envs[i][0]].insert('1.0',"\n".join(self.data.expr_env[envs[i][0]]))
			label_envs[envs[i][0]].grid(row=0,column=i,padx=2,pady=5)
			text_envs[envs[i][0]].grid(row=1,column=i,padx=2,pady=5)
			frame_edit.grid_columnconfigure(i, weight=1)
		frame_edit.grid_rowconfigure(1, weight=1)
		frame_edit.pack(side=tk.TOP,expand=True,padx=10,pady=5)
		btn_ok["command"] = lambda: update()
		btn_cancel["command"] = lambda: cancel()

		def update():
			for key in text_envs.keys():
				self.data.expr_env[key] = util.tidy_list((text_envs[key].get('1.0',text_envs[key].index(tk.END))).split("\n"))
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)