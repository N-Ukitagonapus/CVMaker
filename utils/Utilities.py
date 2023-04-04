import calendar
import tkinter as tk

class Utilities:
	def get_last_date(dt):
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	def tidy_list(list):
		return [s for s in list if s != '']

	#必須マーク付き
	def mark_required(tgt,lbl):
		tk.Label(tgt,text="(必須)",font=("Meiryo UI",6,"bold"),foreground='red').pack(side=tk.LEFT,after=lbl)