import calendar
from datetime import datetime, date
from monthdelta import monthmod 
import tkinter as tk
from tkinter import StringVar, messagebox as msgbox
from tkcalendar import DateEntry
from constants.const import VALID_ERR

from constants.message import DialogMessage

class Utilities:

	#読込値をセット(文字列)
	def setstr_from_read(tgt:StringVar, input:dict):
		if input["result"] != VALID_ERR:
			tgt.set(input["value"])
   
	#読込値をセット(最大文字数超過分カット)
	def setstr_from_read_cut(tgt:StringVar, input:dict, maxlength:int):
		if input["result"] != VALID_ERR:
			tgt.set(input["value"][:maxlength])
   
	#読込値をセット(日付)
	def setdate_from_read(tgtentry:DateEntry, input:dict):
		if input["result"] != VALID_ERR:
			entered_date = datetime.strptime(input["value"],"%Y%m%d")
			tgtentry.set_date(entered_date)

	#文字列⇒数値変換(読み取り失敗時は0)
	def int_from_str(input:str) -> int:
		try:
			return int(input)
		except ValueError:
			return 0
 
	#2日付間の差分(年、月)を取得
	def get_years_sub(dt_from:date, dt_to:date) -> tuple:
		monthdelta = monthmod(dt_from,dt_to)
		return monthdelta[0].months // 12, monthdelta[0].months % 12

	#年月の初日を取得
	def get_first_date(dt) -> datetime.date:
		return date(dt.year, dt.month, 1)
	
	#年月の最終日を取得
	def get_last_date(dt) -> datetime.date: 
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	#リスト整頓(空白除去、重複削除)
	def tidy_list(input: list):
		return list(set([s for s in input if s != '']))

	#必須マーク付き
	def mark_required(tgt,lbl):
		tk.Label(tgt, text="(必須)", font=("Meiryo UI",6,"bold"), foreground='red').pack(side=tk.LEFT, after=lbl)

	def get_dateclass(input) -> datetime.date:
		if type(input) == datetime:
			return input.date()
		else:
			return input

	#汎用メッセージ表示
	def msgbox_showmsg(param: DialogMessage):
		if param[0] == "info" :
			msgbox.showinfo(title=param[1], message=param[2])
		elif param[0] == "warn" :
			msgbox.showwarning(title=param[1], message=param[2])
		elif param[0] == "error" :
			msgbox.showerror(title=param[1], message=param[2])
		else:
			msgbox.showerror(title="BIG BONER DOWN THE LANE", message="This is an error message supposed NOT to be shown.")

	#汎用クエスチョンダイアログ
	def msgbox_ask(param: DialogMessage):
		return msgbox.askyesno(title=param[1], message=param[2])