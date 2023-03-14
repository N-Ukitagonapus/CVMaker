'''
技術情報フレーム
'''
import tkinter as tk
from tkinter import ttk

class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.ret=tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")

		##1行目:ボタンエリア
		self.first_line=tk.Frame(self.ret)
		#読込ボタン
		self.btn_load = tk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = tk.Button(self.first_line,width=5,text="保存")
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X)
		##1行目ここまで


	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=10)