import calendar
import datetime
from monthdelta import monthmod 
import tkinter as tk
from tkinter import messagebox as msgbox

from constants.message import DialogMessage

class Utilities:

	#2日付間の差分(年)を取得
	def get_year_sub(dt_from,dt_to):
		monthdelta = monthmod(dt_from,dt_to)
		return monthdelta[0].months//12

	#年月の初日を取得
	def get_first_date(dt):
		return datetime.date(dt.year, dt.month,1)
	
	#年月の最終日を取得
	def get_last_date(dt):
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	#リスト整頓(空白除去、重複削除)
	def tidy_list(list):
		return [s for s in list if s != '']

	#必須マーク付き
	def mark_required(tgt,lbl):
		tk.Label(tgt,text="(必須)",font=("Meiryo UI",6,"bold"),foreground='red').pack(side=tk.LEFT,after=lbl)

	#汎用メッセージ表示
	def msgbox_showmsg(param: DialogMessage):
		if param[0] == "info" :
			msgbox.showinfo(title=param[1],message=param[2])
		elif param[0] == "warn" :
			msgbox.showwarning(title=param[1],message=param[2])
		elif param[0] == "error" :
			msgbox.showerror(title=param[1],message=param[2])
		else:
			msgbox.showerror(title="BIG BONER DOWN THE LANE",message="This is an error message supposed not to be shown.")