import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import scrolledtext
from constants.const import POSITIONS, TASKS
from utils.DatetimeUtils import DatetimeUtils as dateutil
class CareerHistoryFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "職務経歴")
		self.datalength=3
		self.currentnum=1
  
		#トップフレーム
		self.top_frame=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_now_yrmth = tk.Label(self.top_frame,font=("Meiryo UI",16,"bold"),text=datetime.date.today().strftime("%Y年 %m月"))
		self.label_genzai = tk.Label(self.top_frame,text="現在")

  	#読込ボタン
		self.btn_load = ttk.Button(self.top_frame,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.top_frame,width=5,text="保存")
		#組立
		self.label_now_yrmth.pack(side=tk.LEFT,padx=5)
		self.label_genzai.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.top_frame.pack(side=tk.TOP,fill=tk.X,pady=5)
		##1行目ここまで

	#メインフレーム
		self.frame_main = tk.Frame(self.ret,relief=tk.RAISED,borderwidth=2)

	#ヒストリナンバーフレーム
		self.frame_control = tk.Frame(self.frame_main)
		#進む・戻るボタン
		self.button_upper = ttk.Button(self.frame_control,text="▲前")
		self.button_lower = ttk.Button(self.frame_control,text="▼次")

		#ページ送りフレーム
		self.subframe_page = tk.Frame(self.frame_control)
		self.curr_page = ttk.Combobox(self.subframe_page,width=3,state="readonly",justify="center",value=[i for i in range(self.currentnum,self.datalength + 1)])
		self.curr_page.set(1)
		self.total_page = tk.Label(self.subframe_page,text=self.datalength)
		self.label_slash_page = tk.Label(self.subframe_page,text="／")

		#追加・削除ボタンのサブフレーム
		self.subframe_adddel = tk.Frame(self.frame_control)
		self.button_add = ttk.Button(self.subframe_adddel,text="追加",width=5)
		self.button_del = ttk.Button(self.subframe_adddel,text="削除",width=5)	

		#組立
		self.button_add.pack(side=tk.LEFT,padx=1)
		self.button_del.pack(side=tk.LEFT,padx=1)
		self.subframe_adddel.pack(side=tk.TOP)

		self.curr_page.pack(side=tk.TOP)
		self.label_slash_page.pack(side=tk.TOP)
		self.total_page.pack(side=tk.TOP)

		self.button_upper.pack(side=tk.TOP,expand=True,fill=tk.Y)
		self.subframe_page.pack(side=tk.TOP)
		self.button_lower.pack(side=tk.TOP,expand=True,fill=tk.Y)

		self.frame_control.pack(side=tk.RIGHT,padx=2,fill=tk.Y)
		self.frame_main.pack(side=tk.TOP,expand=True,fill=tk.BOTH,padx=2,pady=2)   

		#1行目
		self.first_line = tk.Frame(self.frame_main)

  	#フレーム・ラベル定義
		self.label_kara = tk.Label(self.first_line,text="～")
    
		#業務期間
		self.expr_start = DateEntry(self.first_line,day=1)
		self.expr_end = DateEntry(self.first_line,day=dateutil.get_last_date(datetime.date.today()).day)

		#終了フラグ
		self.flg_bus_end = tk.BooleanVar(value = False)
		self.chk_bus_end = tk.Checkbutton(self.first_line,text="業務終了", variable=self.flg_bus_end)

		#組立
		self.expr_start.pack(side=tk.LEFT,padx=5)
		self.label_kara.pack(side=tk.LEFT,padx=5)
		self.expr_end.pack(side=tk.LEFT,padx=5)
		self.chk_bus_end.pack(side=tk.LEFT,padx=5)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#2行目
		self.second_line = tk.Frame(self.frame_main)
  
  	#フレーム・ラベル定義
		self.label_gyokai = tk.Label(self.second_line,text="業界")
    
		#業務期間
		self.text_gyokai = ttk.Entry(self.second_line, width=10)

		#組立  
		self.label_gyokai.pack(side=tk.LEFT,padx=5)
		self.text_gyokai.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#3行目
		self.third_line = tk.Frame(self.frame_main)
  
  	#フレーム・ラベル定義
		self.label_proj_ov = tk.Label(self.third_line,text="プロジェクト概要")
		self.label_sys_ov = tk.Label(self.third_line,text="システム概要") 
		self.label_disc_work = tk.Label(self.third_line,text="作業概要\n(カンマ区切り)") 

		self.text_proj_ov = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)  
		self.text_sys_ov = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)  
		self.text_disc_work = tk.Text(self.third_line,wrap=tk.WORD,height=2)
  
		#組立
		self.label_proj_ov.grid(row=0,column=0,padx=5)
		self.text_proj_ov.grid(row=0,column=1,padx=5,sticky=tk.NSEW)
		self.label_sys_ov.grid(row=1,column=0,padx=5)
		self.text_sys_ov.grid(row=1,column=1,padx=5,sticky=tk.NSEW)
		self.label_disc_work.grid(row=2,column=0,padx=5)
		self.text_disc_work.grid(row=2,column=1,padx=5,sticky=tk.NSEW)
		self.third_line.grid_columnconfigure(1, weight=1)
		self.third_line.pack(side=tk.TOP,expand=True,fill=tk.X)

		#4行目
		self.fourth_line = tk.Frame(self.frame_main)

  	#フレーム・ラベル定義
		self.label_env = tk.Label(self.fourth_line,text="開発環境")
		self.label_position = tk.Label(self.fourth_line,text="職位") 
		self.label_members = tk.Label(self.fourth_line,text="開発メンバ数(自社/総数)") 
		self.label_slash_member = tk.Label(self.fourth_line,text="/")

		#開発環境
		self.btn_env_edit = ttk.Button(self.fourth_line,width=5,text="編集")
		#職位
		self.select_position = ttk.Combobox(self.fourth_line,width=16,state="readonly",value=[val for val in POSITIONS.keys()])
		self.text_position_etc = ttk.Entry(self.fourth_line,width=16,state="disabled") 
		#開発メンバ数
		self.label_members_internal = tk.Entry(self.fourth_line,width=3) 
		self.label_members_total = tk.Entry(self.fourth_line,width=3) 
		self.flg_internal_leader = tk.BooleanVar(value = False)
		self.chk_internal_leader = tk.Checkbutton(self.fourth_line,text="自社リーダー",variable=self.flg_internal_leader)

		#組立
		self.label_env.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)
		self.label_position.pack(side=tk.LEFT,padx=5)  
		self.select_position.pack(side=tk.LEFT,padx=5)
		self.text_position_etc.pack(side=tk.LEFT,padx=5)
		self.label_members.pack(side=tk.LEFT,padx=5)
		self.label_members_internal.pack(side=tk.LEFT,padx=5)
		self.label_slash_member.pack(side=tk.LEFT,padx=5)
		self.label_members_total.pack(side=tk.LEFT,padx=5)
		self.chk_internal_leader.pack(side=tk.LEFT,padx=5)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X)

		#5行目
		self.fifth_line = tk.Frame(self.frame_main)
  	#フレーム・ラベル定義
		self.label_task = tk.Label(self.fifth_line,text="作業内容")
		self.label_task.grid(row=0,column=0,rowspan=2,padx=5)

		#作業内容
		self.flg_tasks={}
		self.chk_tasks={}
		task_list=list(TASKS.items())
		for i in range(len(task_list)):
			self.flg_tasks[task_list[i][0]] = tk.BooleanVar(value = False)
			self.chk_tasks[task_list[i][0]] = tk.Checkbutton(self.fifth_line,text=task_list[i][1],variable=self.flg_tasks[task_list[i][0]])
			self.chk_tasks[task_list[i][0]].grid(row=i//7,column=(i%7)+1,padx=5,sticky=tk.W)

		#作業内容その他
		self.text_tasks_etc = ttk.Entry(self.fifth_line,width=16,state="disabled") 
		self.text_tasks_etc.grid(row=1,column=8,padx=5,sticky=tk.W)

		self.fifth_line.pack(side=tk.TOP,fill=tk.X)

		self.control_button()

	#ボタンコントロール
	def control_button():
		pass

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=20,pady=5)
