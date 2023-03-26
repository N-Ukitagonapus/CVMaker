import datetime
import tkinter as tk
from tkinter import ttk

class CareerHistoryFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "職務経歴")
		self.datalength=1
		self.currentnum=1

		#1行目
		##1行目
		self.top_frame=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_now_yrmth = tk.Label(self.top_frame,font=("Meiryo UI",16,"bold"),text=datetime.date.today().strftime("%Y年 %m月"))
		self.label_genzai = tk.Label(self.top_frame,text="現在")

  	#読込ボタン
		self.btn_load = tk.Button(self.top_frame,width=5,text="読込")
		#保存ボタン
		self.btn_save = tk.Button(self.top_frame,width=5,text="保存")
		#組立
		self.label_now_yrmth.pack(side=tk.LEFT,padx=5)
		self.label_genzai.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.top_frame.pack(side=tk.TOP,fill=tk.X,pady=5)
		##1行目ここまで

	#ヒストリナンバーフレーム
		self.frame_control=tk.Frame(self.ret,relief=tk.RAISED,borderwidth=2)
		#進む・戻るボタン
		self.button_upper=tk.Button(self.frame_control,text="▲")
		self.button_lower=tk.Button(self.frame_control,text="▼")

		#ページ送りフレーム
		self.subframe_page=tk.Frame(self.frame_control)
		self.curr_page=ttk.Combobox(self.subframe_page,width=3,state="readonly",justify="center",value=[i for i in range(self.currentnum,self.currentnum + 1)])
		self.curr_page.set(1)
		self.total_page=tk.Label(self.subframe_page,text=self.datalength)
		self.label_slash=tk.Label(self.subframe_page,text="／")

		#追加・削除ボタンのサブフレーム
		self.subframe_adddel=tk.Frame(self.frame_control)
		self.button_add=tk.Button(self.subframe_adddel,text="追加")
		self.button_del=tk.Button(self.subframe_adddel,text="削除")	

		#組立
		self.button_add.pack(side=tk.LEFT,padx=1)
		self.button_del.pack(side=tk.LEFT,padx=1)
		self.subframe_adddel.pack(side=tk.TOP)

		self.curr_page.pack(side=tk.TOP)
		self.label_slash.pack(side=tk.TOP)
		self.total_page.pack(side=tk.TOP)

		self.button_upper.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
		self.subframe_page.pack(side=tk.TOP)
		self.button_lower.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

		self.frame_control.pack(side=tk.RIGHT,fill=tk.Y,padx=1,pady=1)

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=20,pady=5)
