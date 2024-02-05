import datetime
from datetime import datetime as dt
import tkinter as tk
from tkinter import BooleanVar, IntVar, StringVar, ttk
from tkcalendar import DateEntry
from tkinter import scrolledtext
from constants.const import POSITIONS, TASKS
from data_structure.CareerData import CareerData
from data_structure.CareerHistoryData import CareerHistoryData
from fileio.CareerHistoryDataIO import CareerHistoryDataInput, CareerHistoryDataOutput
from frames.subframe.EnvironmentSubFrame import EnvironmentSubFrame
from frames.subframe.ScaleDataSubFrame import ScaleDataSubFrame
from utils.Utilities import Utilities as util
from constants.message import DialogMessage as diag
from utils.Validation import DynamicValidation as dval
class CareerHistoryFrame(tk.Frame):
	"""
	職務経歴情報フレーム
	"""
	def __init__(self, target):

		self.data=CareerHistoryData()
		self.data_num=1

		self.area_define(target)
		self.button_control(target)
		self.input_control()
		self.assembly()

	def area_define(self, target):
		"""
		エリア定義
		Args:
				target (tk.Frame): 設置対象
		"""
		#バリデーション定義
		is_numeric = target.register(dval.is_numeric)
   
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "職務経歴")

		#トップフレーム
		self.top_frame=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_now_yrmth = tk.Label(self.top_frame,font=("Meiryo UI",16,"bold"),text=datetime.date.today().strftime("%Y年 %m月"))
		self.label_genzai = tk.Label(self.top_frame,text="現在")

  	#読込ボタン
		self.btn_load = ttk.Button(self.top_frame,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.top_frame,width=5,text="保存")

	#メインフレーム
		self.frame_main = tk.Frame(self.ret,relief=tk.RAISED,borderwidth=2)

	#ヒストリナンバーフレーム
		self.frame_control = tk.Frame(self.frame_main)
		#進む・戻るボタン
		self.button_prev = ttk.Button(self.frame_control,text="▲前")
		self.button_next = ttk.Button(self.frame_control,text="▼次")

		#ページ送りフレーム
		self.subframe_page = tk.Frame(self.frame_control)
		self.page_num = IntVar()
		self.page_num.set(self.data_num)
		self.curr_page = ttk.Combobox(self.subframe_page,width=3,textvariable=self.page_num,state="readonly",justify="center",value=[1])
		self.total_page = tk.Label(self.subframe_page,text=1)
		self.label_slash_page = tk.Label(self.subframe_page,text="／")

		#追加・削除ボタンのサブフレーム
		self.subframe_adddel = tk.Frame(self.frame_control)
		self.button_add = ttk.Button(self.subframe_adddel,text="追加",width=5)
		self.button_del = ttk.Button(self.subframe_adddel,text="削除",width=5)	 

		#1行目
		self.first_line = tk.Frame(self.frame_main)

  	#フレーム・ラベル定義
		self.label_kara = tk.Label(self.first_line,text="～")
    
		#業務期間
		##開始年月
		self.str_term_start = StringVar()
		self.term_start = DateEntry(self.first_line, day=1, locale='ja_JP', date_pattern='yyyy/mm/dd', textvariable=self.str_term_start)
		##終了年月
		self.str_term_end = StringVar()
		self.term_end = DateEntry(self.first_line, day=util.get_last_date(datetime.date.today()).day, locale='ja_JP', date_pattern='yyyy/mm/dd', textvariable=self.str_term_end)
		self.term_end["state"] = tk.DISABLED

		#終了フラグ
		self.flg_bus_end = BooleanVar(value = False)
		self.chk_bus_end = ttk.Checkbutton(self.first_line,text="業務終了", variable=self.flg_bus_end)

		#2行目
		self.second_line = tk.Frame(self.frame_main)
  
  	#フレーム・ラベル定義
		self.label_gyokai = tk.Label(self.second_line,text="業種")
    
		#業務期間
		self.str_gyokai = StringVar()
		self.text_gyokai = ttk.Entry(self.second_line, width=10, textvariable=self.str_gyokai)

		#3行目
		self.third_line = tk.Frame(self.frame_main)
  
  	#フレーム・ラベル定義
		self.label_proj_ov = tk.Label(self.third_line,text="プロジェクト概要")
		self.label_sys_ov = tk.Label(self.third_line,text="システム概要") 
		self.label_disc_work = tk.Label(self.third_line,text="作業概要") 

		self.text_proj_ov = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)  
		self.text_sys_ov = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)  
		self.text_disc_work = scrolledtext.ScrolledText(self.third_line,wrap=tk.WORD,width=80,height=3)

		#4行目
		self.fourth_line = tk.Frame(self.frame_main)
  	#フレーム・ラベル定義
		self.label_env = tk.Label(self.fourth_line,text="開発環境")
		self.label_scale = tk.Label(self.fourth_line,text="開発規模")
		self.label_position = tk.Label(self.fourth_line,text="職位") 
		self.label_members = tk.Label(self.fourth_line,text="開発メンバー数(自社/総数)") 
		self.label_slash_member = tk.Label(self.fourth_line,text="/")

		#開発環境
		self.btn_env_edit = ttk.Button(self.fourth_line,width=5,text="編集")
		#開発規模
		self.btn_scale_edit = ttk.Button(self.fourth_line,width=5,text="編集")
		#職位
		self.str_position = StringVar()
		self.select_position = ttk.Combobox(self.fourth_line, width=16, state="readonly", value=[val for val in POSITIONS.keys()], textvariable=self.str_position)
		self.str_position_etc = StringVar()
		self.text_position_etc = ttk.Entry(self.fourth_line, width=16, state="disabled", textvariable=self.str_position_etc) 
		#開発メンバ数
		self.str_members_internal = StringVar()
		self.text_members_internal = ttk.Entry(self.fourth_line, width=5,
          textvariable=self.str_members_internal,
				  validatecommand = (is_numeric, '%P', 5),
					validate='key')
		self.str_members_total = StringVar()
		self.text_members_total = ttk.Entry(self.fourth_line, width=5,
          textvariable=self.str_members_total,
				  validatecommand = (is_numeric, '%P', 5),
					validate='key')
		self.flg_internal_leader = BooleanVar(value = False)
		self.chk_internal_leader = ttk.Checkbutton(self.fourth_line, text="自社リーダー", variable=self.flg_internal_leader)

		#5行目
		self.fifth_line = tk.Frame(self.frame_main)
  	#フレーム・ラベル定義
		self.label_task = tk.Label(self.fifth_line,text="作業内容")
		self.label_task.grid(row=0,column=0,rowspan=2,padx=5)

		#作業内容
		self.flg_tasks={}
		self.chk_tasks={}
		task_keys=list(TASKS.keys())
  
		for i in range(len(task_keys)):
			self.flg_tasks[task_keys[i]] = BooleanVar(value = False)
			self.chk_tasks[task_keys[i]] = ttk.Checkbutton(self.fifth_line,text=TASKS[task_keys[i]],variable=self.flg_tasks[task_keys[i]])
			self.chk_tasks[task_keys[i]].grid(row=i//10,column=(i%10)+1,padx=5,sticky=tk.W)

		#作業内容その他
		self.str_tasks_etc = StringVar()
		self.text_tasks_etc = ttk.Entry(self.fifth_line, width=16, state="disabled", textvariable=self.str_tasks_etc) 
		self.text_tasks_etc.grid(row=1,column=(len(task_keys)%10)+1,padx=5,sticky=tk.W)

	def assembly(self):
		"""
		組み立て
		"""
		#トップフレーム
		self.label_now_yrmth.pack(side=tk.LEFT,padx=5)
		self.label_genzai.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.top_frame.pack(side=tk.TOP,fill=tk.X,pady=5)

		#メイン&ページ送りフレーム
		self.button_add.pack(side=tk.LEFT,padx=1)
		self.button_del.pack(side=tk.LEFT,padx=1)
		self.subframe_adddel.pack(side=tk.TOP)
		self.curr_page.pack(side=tk.TOP)
		self.label_slash_page.pack(side=tk.TOP)
		self.total_page.pack(side=tk.TOP)
		self.button_prev.pack(side=tk.TOP,expand=True,fill=tk.Y)
		self.subframe_page.pack(side=tk.TOP)
		self.button_next.pack(side=tk.TOP,expand=True,fill=tk.Y)
		self.frame_control.pack(side=tk.RIGHT,padx=2,fill=tk.Y)
		self.frame_main.pack(side=tk.TOP,expand=True,fill=tk.BOTH,padx=2,pady=2)  

		#1行目
		self.term_start.pack(side=tk.LEFT,padx=5)
		self.label_kara.pack(side=tk.LEFT,padx=5)
		self.term_end.pack(side=tk.LEFT,padx=5)
		self.chk_bus_end.pack(side=tk.LEFT,padx=5)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#2行目
		self.label_gyokai.pack(side=tk.LEFT,padx=5)
		self.text_gyokai.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#3行目
		self.label_proj_ov.grid(row=0,column=0,padx=5)
		self.text_proj_ov.grid(row=0,column=1,padx=5,sticky=tk.NSEW)
		self.label_sys_ov.grid(row=1,column=0,padx=5)
		self.text_sys_ov.grid(row=1,column=1,padx=5,sticky=tk.NSEW)
		self.label_disc_work.grid(row=2,column=0,padx=5)
		self.text_disc_work.grid(row=2,column=1,padx=5,sticky=tk.NSEW)
		self.third_line.grid_columnconfigure(1, weight=1)
		self.third_line.pack(side=tk.TOP,expand=True,fill=tk.X)

   	#4行目
		self.label_env.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)

		self.label_scale.pack(side=tk.LEFT,padx=5)
		self.btn_scale_edit.pack(side=tk.LEFT,padx=5)

		self.label_position.pack(side=tk.LEFT,padx=5)
		util.mark_required(self.fourth_line,self.label_position)
		self.select_position.pack(side=tk.LEFT,padx=5)
		self.text_position_etc.pack(side=tk.LEFT,padx=5)

		self.label_members.pack(side=tk.LEFT,padx=5)
		util.mark_required(self.fourth_line,self.label_members)
		self.text_members_internal.pack(side=tk.LEFT,padx=5)
		self.label_slash_member.pack(side=tk.LEFT,padx=5)
		self.text_members_total.pack(side=tk.LEFT,padx=5)
		self.chk_internal_leader.pack(side=tk.LEFT,padx=5)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X)
  
		#5行目
		self.fifth_line.pack(side=tk.TOP,fill=tk.X)
  
	def button_control(self, target):
		"""
		ボタンコントロール
		Args:
				target (tk.Frame): サブウィンドウ表示元(=メインフレーム)
		"""
		def prev():
			"""
			前レコードへ
			"""
			if self.data_num > 1:
				self.data_num -= 1
				self.page_num.set(self.data_num)
		def next():
			"""
			次レコードへ
			"""
			if self.data_num < len(self.data.history_list):
				self.data_num += 1
				self.page_num.set(self.data_num)
		def add_data():
			"""
			データ追加
			"""
			self.data.history_list.append(CareerData())
			update_datanum()
		def del_data():
			"""
			データ削除
			"""
			if len(self.data.history_list) > 1 :
				if util.msgbox_ask(diag.DIALOG_ASK_DELETE_CAREERDATA):
					del self.data.history_list[self.data_num - 1]
					update_datanum()
					if self.data_num > 1:
						self.data_num -= 1
						self.page_num.set(self.data_num)
			else:
				util.msgbox_showmsg(diag.DIALOG_CANT_DELETE)
		def update_datanum():
			"""
			ページ更新
			"""
			data_total = len(self.data.history_list)
			self.total_page["text"] = data_total
			self.curr_page["value"]=[i for i in range(1,data_total+1)]
   
		def edit_envs():
			"""
			開発環境サブウィンドウ
			"""
			try:
				env_sub = EnvironmentSubFrame()
				env_sub.edit_envs(target, "開発環境編集", self.get_current().environment)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
			finally:
				del env_sub

		def edit_scales():
			"""
			開発規模サブウィンドウ
			"""
			try:
				scale_sub =  ScaleDataSubFrame()
				scale_sub.edit_scale(target, self.get_current().scale)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
			finally:
				del scale_sub

		def read_file():
			"""
			ファイル読込
			"""
			if self.data.first_name_kanji == "" and self.data.last_name_kanji == "":
				util.msgbox_showmsg(diag.DIALOG_ERROR_NO_PERSONAL_DATA)
				return
			try:
      
				io = CareerHistoryDataInput()
				read_data = io.read(self.data.last_name_kanji,self.data.first_name_kanji)
				if read_data is not None :
					self.data = read_data
					update_datanum()
					self.data_num = 1
					self.updadte_widget(self.data_num)
					util.msgbox_showmsg(diag.DIALOG_SUCCESS_READ_CAREERDATA)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
			finally:
				del io

		def save_file():
			"""
			ファイルへ保存
			"""
			try:
				io = CareerHistoryDataOutput(self.data)
				io.check_input(target)
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			finally:
				del io

		self.btn_load["command"] = lambda: read_file()
		self.btn_save["command"] = lambda: save_file()
		self.button_prev["command"] = lambda: prev()
		self.button_next["command"] = lambda: next()
		self.button_add["command"] = lambda: add_data()
		self.button_del["command"] = lambda: del_data()
		self.btn_env_edit["command"] = lambda: edit_envs()
		self.btn_scale_edit["command"] = lambda: edit_scales()

	#入力コントロール
	def input_control(self):
		"""
		入力コントロール
		"""
   
		def set_datanum(*args):
			self.data_num = int(self.page_num.get())
			self.updadte_widget(self.data_num)

		def set_flg_over():
			self.get_current().set_flg_over(self.flg_bus_end)
			if self.flg_bus_end.get() == True:
				self.term_end["state"] = tk.NORMAL
			else :
				self.get_current().set_term_end(util.get_last_date(datetime.date.today()))
				self.term_end.set_date(util.get_last_date(datetime.date.today()))
				self.term_end["state"] = tk.DISABLED

		def set_term_first(event):
			try:
				conv = util.get_first_date(dt.strptime(self.str_term_start.get(),"%Y/%m/%d"))
				self.get_current().set_term_start(conv)
				self.term_start.set_date(conv)
			except ValueError:
				return
		def set_term_last(event):
			try:
				conv = util.get_last_date(dt.strptime(self.str_term_end.get(),"%Y/%m/%d"))
				self.get_current().set_term_end(conv)
				self.term_end.set_date(conv)
			except ValueError:
				return
		def set_gyokai(event):
			self.get_current().set_gyokai(self.str_gyokai)
		def proj_ov_set(event):
			self.get_current().set_proj_overview(self.text_proj_ov)
		def sys_ov_set(event):
			self.get_current().set_sys_overview(self.text_sys_ov)
		def disc_work_set(event):
			self.get_current().set_works(self.text_disc_work)
		def set_tasks():
			self.get_current().set_tasks(self.flg_tasks)
			if self.flg_tasks["ETC"].get() and self.text_tasks_etc["state"] != tk.NORMAL :
				self.text_tasks_etc["state"] = tk.NORMAL 
			else:
				self.text_tasks_etc["state"] = tk.DISABLED
				self.str_tasks_etc.set("")
		def set_task_etc(event):
			self.get_current().set_tasks_etc(self.str_tasks_etc)
		def set_position(event):
			self.get_current().set_position(self.str_position)
			if self.str_position.get() == "その他" and self.text_position_etc["state"] != tk.NORMAL :
				self.text_position_etc["state"] = tk.NORMAL 
			else:
				self.text_position_etc["state"] = tk.DISABLED
				self.str_position_etc.set("")
		def set_position_etc(event):
			self.get_current().set_position_etc(self.str_position_etc)
		def set_members_internal(event):
			self.get_current().set_members_internal(self.str_members_internal)
		def set_members_total(event):
			self.get_current().set_members(self.str_members_total)
		def set_internal_leader():
			self.get_current().set_flg_internal_leader(self.flg_internal_leader)
  
		self.page_num.trace('w',set_datanum)
		self.chk_bus_end["command"] = lambda:set_flg_over()
		self.term_start.bind("<FocusOut>",func = set_term_first)
		self.term_end.bind("<FocusOut>",func = set_term_last)
		self.text_gyokai.bind("<FocusOut>",func = set_gyokai)

		self.text_proj_ov.bind("<FocusOut>",func = proj_ov_set)
		self.text_sys_ov.bind("<FocusOut>",func = sys_ov_set)
		self.text_disc_work.bind("<FocusOut>",func = disc_work_set)

		task_keys=list(TASKS.keys())
		for i in range(len(task_keys)):
			self.chk_tasks[task_keys[i]]["command"] = lambda:set_tasks()
		self.text_tasks_etc.bind("<FocusOut>",func = set_task_etc)

		self.select_position.bind('<<ComboboxSelected>>',func = set_position)
		self.text_position_etc.bind("<FocusOut>",func = set_position_etc)
		self.text_members_internal.bind("<FocusOut>",func = set_members_internal)
		self.text_members_total.bind("<FocusOut>",func = set_members_total)
		self.chk_internal_leader["command"] = lambda:set_internal_leader()


	def updadte_widget(self,page):
		"""
		画面更新
		"""
		self.page_num.set(page)
		self.set_from_data(self.get_current())


	def set_from_data(self, data:CareerData):
		"""
		フォームに値を設定
		"""
		self.flg_bus_end.set(data.flg_over)
		self.term_start.set_date(data.term_start)
		if data.flg_over:
			self.term_end["state"] = tk.NORMAL
			self.term_end.set_date(data.term_end)
		else :
			self.term_end.set_date(data.term_end)
			self.term_end["state"] = tk.DISABLED
		self.str_gyokai.set(data.description_gyokai)
		self.text_proj_ov.delete("1.0","end")
		self.text_proj_ov.insert('1.0',(data.description_project_overview))
		self.text_sys_ov.delete("1.0","end")
		self.text_sys_ov.insert('1.0',(data.description_system_overview))
		self.text_disc_work.delete("1.0","end")
		self.text_disc_work.insert('1.0',(data.description_work))
		keys=list(TASKS.keys())
		for i in keys:
			if i in data.tasks:
				self.flg_tasks[i].set(True)
			else:
				self.flg_tasks[i].set(False)
		if self.flg_tasks["ETC"].get():
			self.text_tasks_etc["state"] = tk.NORMAL
			self.str_tasks_etc.set(data.tasks_etc)
		else:
			self.str_tasks_etc.set(data.tasks_etc)
			self.text_tasks_etc["state"] = tk.DISABLED
		self.str_position.set(data.position)
		if data.position == POSITIONS["その他"]:
			self.text_position_etc["state"] = tk.NORMAL 
			self.str_position_etc.set(data.position_etc)
		else:
			self.str_position_etc.set(data.position_etc)
			tk.DISABLED
		self.flg_internal_leader.set(data.flg_internal_leader)
		self.str_members_total.set(str(data.members))
		self.str_members_internal.set(str(data.members_internal))

	def get_current(self) -> CareerData:
		"""
		現在の経歴データ呼出
		データ番号に応じた経歴データを呼び出す。

		Returns
		-------
		CareerData
				番号に応じた経歴データ
		"""
		return self.data.history_list[self.data_num - 1]

	def pack(self):
		"""
		メインウィンドウへ配置(mainからの呼び出し)
		"""
		self.ret.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=20,pady=5)
