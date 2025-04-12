from tkcalendar import DateEntry
import tkinter as tk
from tkinter import  BooleanVar, ttk

from data_structure.PersonalData import PersonalData

from fileio.PersonalDataIO import PersonalDataInput, PersonalDataOutput

from utils.Utilities import Utilities as util
from utils.Validation import DynamicValidation as dval

from constants.message import DialogMessage as diag
class PersonalDataFrame(tk.Frame):
	"""
 	個人基本情報フレーム
	"""
	def __init__(self, target):
		self.data=PersonalData()

		self.area_define(target)
		self.input_control(target)
		self.assembly()

	#エリア定義
	def area_define(self, target):
		"""
		エリア定義
		Args:
				target (tk.Frame): 設置対象
		"""
		#バリデーション定義
		length_limit = target.register(dval.length_limit)
  
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "個人基本情報")
		#1行目
		self.first_line=tk.Frame(self.ret)
		##編集ボタン
		self.btn_edit = ttk.Button(self.first_line,width=5,text="編集",state=tk.DISABLED)
		##読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		##保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")
		##1行目ここまで

		#2行目
		self.second_line = tk.Frame(self.ret)
  	##フレーム・ラベル定義
		self.label_shimei = util.requiredLabel(self.second_line,"氏名")
		self.label_kanji = tk.Label(self.second_line,text="漢字")
		self.label_romaji = tk.Label(self.second_line,text="ローマ字")

		##名前(漢字)
		self.text_shi_kanji = ttk.Entry(self.second_line,
				  textvariable=self.data.name_last_kanji,
				  validatecommand = (length_limit, '%P', 10),
					validate='key')
		self.text_mei_kanji = ttk.Entry(self.second_line,
				  textvariable=self.data.name_first_kanji,
				  validatecommand = (length_limit, '%P', 10),
					validate='key')
		##名前(ローマ字)
		self.text_shi_romaji = ttk.Entry(self.second_line,
				  textvariable=self.data.name_last_romaji,
				  validatecommand =(length_limit, '%P', 15),
					validate='key')
		self.text_mei_romaji = ttk.Entry(self.second_line,
				  textvariable=self.data.name_first_romaji,
				  validatecommand =(length_limit, '%P', 15),
					validate='key')
		self.second_line.columnconfigure(2,weight=1)
		self.second_line.columnconfigure(3,weight=1)
		#2行目ここまで

		#3行目
		self.third_line = tk.Frame(self.ret)
 		##名前(性別)
		self.gender_male = ttk.Radiobutton(self.third_line,text="男",value="男",variable=self.data.gender)
		self.gender_female = ttk.Radiobutton(self.third_line,text="女",value="女",variable=self.data.gender)
		##生年月日
		self.label_birthday = tk.Label(self.third_line,text="生年月日")
		self.birthday_entry = DateEntry(self.third_line,locale='ja_JP',date_pattern='yyyy/mm/dd')
		#3行目ここまで

		#4行目
		self.fourth_line = tk.Frame(self.ret)
  	##フレーム・ラベル定義
		self.label_address = tk.Label(self.fourth_line,text="現住所(市・区まで)")
		self.label_station = tk.Label(self.fourth_line,text="最寄り駅")
		##現住所
		self.text_address = ttk.Entry(self.fourth_line, textvariable=self.data.current_address)
		##最寄り駅
		self.text_station = ttk.Entry(self.fourth_line, textvariable=self.data.nearest_station)
		self.fourth_line.columnconfigure(1,weight=1)
		self.fourth_line.columnconfigure(3,weight=1)
		#4行目ここまで

		#5行目
		self.fifth_line = tk.Frame(self.ret)
  	#フレーム・ラベル定義
		self.label_academic = tk.Label(self.fifth_line,text="最終学歴")
		#最終学歴
		self.text_academic = ttk.Entry(self.fifth_line, textvariable=self.data.gakureki)
		#5行目ここまで

	def assembly(self):
		"""
  	組立
		"""
		#1行目
		self.btn_edit.pack(side=tk.RIGHT,padx=10)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#2行目
		self.label_shimei.grid(row=0,column=0,rowspan=2)
		self.label_kanji.grid(row=0,column=1)
		self.label_romaji.grid(row=1,column=1)
		self.text_shi_kanji.grid(row=0,column=2,padx=5,sticky=tk.NSEW)
		self.text_mei_kanji.grid(row=0,column=3,padx=5,sticky=tk.NSEW)
		self.text_shi_romaji.grid(row=1,column=2,padx=5,sticky=tk.NSEW)
		self.text_mei_romaji.grid(row=1,column=3,padx=5,sticky=tk.NSEW)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#3行目
		self.gender_male.pack(side=tk.LEFT,padx=5)
		self.gender_female.pack(side=tk.LEFT,padx=5)
		self.label_birthday.pack(side=tk.LEFT,padx=5)
		self.birthday_entry.pack(side=tk.LEFT,fill=tk.X,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)
  
		#4行目
		self.label_address.grid(row=0,column=0)
		self.text_address.grid(row=0,column=1,padx=5,sticky=tk.NSEW)
		self.label_station.grid(row=0,column=2,padx=5)
		self.text_station.grid(row=0,column=3,padx=5,sticky=tk.NSEW)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#5行目
		self.label_academic.pack(side=tk.LEFT)
		util.mark_required(self.fifth_line,self.label_academic)
		self.text_academic.pack(side=tk.LEFT,padx=5)
		self.fifth_line.pack(side=tk.TOP,fill=tk.X,pady=2)
  
	def input_control(self,target):
		"""
		入力コントロール

		Args:
				target (tk.Frame): サブウィンドウ表示元(=メインフレーム)
		"""
		#誕生日設定
		def birthday_set(event):
			self.data.birthday=self.birthday_entry.get_date()
   
		self.btn_load["command"] = lambda: self.data_read(target)
		self.btn_save["command"] = lambda: self.data_save(target)
		self.btn_edit["command"] = lambda: self.reactivate_items(target)
		self.birthday_entry.bind("<FocusOut>",func = birthday_set)

	#データ出力
	def data_save(self,target):
		"""
		データ出力
		Args:
				target (tk.Frame): サブウィンドウ表示元(=メインフレーム)
		"""
		io = PersonalDataOutput(self.data)
		io.confirm(target, self)
		del io

	#データ読込
	def data_read(self,target):
		"""
		データ読込
		Args:
				target (tk.Frame): サブウィンドウ表示元(=メインフレーム)
		"""
		io = PersonalDataInput(self)
		io.read(target)
		del io
		
	#項目再活性
	def reactivate_items(self,target):
		"""
		項目再活性
		Args:
				target (tk.Frame): サブウィンドウ表示元(=メインフレーム)
		"""
		modes = {
			"name":BooleanVar(),
			"address":BooleanVar(),
			"all":BooleanVar()
		}
		check_modes={}

		subwindow = tk.Toplevel(target)
		subwindow.title("項目再活性")
		subwindow.geometry("300x300")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_ok = ttk.Button(frame_button_inner,width=10,text="OK")
		button_cancel = ttk.Button(frame_button_inner,width=10,text="キャンセル")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
		frame_button_inner.pack(pady=5)
		button_cancel.grid(row=0,column=0,padx=15)
		button_ok.grid(row=0,column=1,padx=15)

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "個人基本情報 再編集")
		frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
		frame_main_inner=tk.Frame(frame_main)
		frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)
		tk.Label(frame_main_inner,text="編集モードを選んでください。").pack(side=tk.TOP,padx=5,pady=5)

		check_modes["name"] =	tk.Checkbutton(frame_main_inner, variable=modes["name"], text="苗字変更\n(結婚等で苗字が変更された場合)")
		check_modes["address"] =	tk.Checkbutton(frame_main_inner, variable=modes["address"], text="住所および最寄り駅変更\n(引っ越し等で住所を変更した場合)")
		check_modes["all"] =	tk.Checkbutton(frame_main_inner, variable=modes["all"], text="全部変更\n(打ち間違いによる修正)\n※原則として推奨できません！")

		for chk in check_modes.values():
			chk.pack(anchor=tk.NW,padx=10,pady=5,fill=tk.X,expand="TRUE")
   
		def switch_state():
			"""
   		チェックボックス活性切替
			"""
			check_modes["name"]["state"] = tk.DISABLED if modes["all"].get() else tk.NORMAL
			check_modes["address"]["state"] = tk.DISABLED if modes["all"].get() else tk.NORMAL
   
		def reactivate():
			"""
   		項目再活性
			"""
			if modes["all"].get():
				if util.msgbox_ask(diag.DIALOG_ASK_EDIT_PERSONALDATA):
					do_reactivate()
			else:
				do_reactivate()

		def do_reactivate():
			"""
   		再活性実行
			"""
			self.text_shi_kanji["state"] =	 tk.NORMAL if modes["all"].get() or modes["name"].get() else tk.DISABLED
			self.text_mei_kanji["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.text_shi_romaji["state"] =	 tk.NORMAL if modes["all"].get() or modes["name"].get() else tk.DISABLED
			self.text_mei_romaji["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.gender_male["state"] =		 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.gender_female["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.birthday_entry["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			self.text_address["state"] =	 tk.NORMAL if modes["all"].get() or modes["address"].get() else tk.DISABLED
			self.text_station["state"] =	 tk.NORMAL if modes["all"].get() or modes["address"].get() else tk.DISABLED
			self.text_academic["state"] =	 tk.NORMAL if modes["all"].get() else tk.DISABLED
			subwindow.destroy()

		def cancel():
			"""
   		キャンセル
			"""
			subwindow.destroy()
   
		check_modes["all"]["command"] = lambda:switch_state()
		button_ok["command"] = lambda:reactivate()
		button_cancel["command"] = lambda: cancel()

	def pack(self):
		"""
  	フレーム描写
		"""
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)
