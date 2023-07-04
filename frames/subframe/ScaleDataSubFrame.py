'''
開発規模サブウィンドウ
'''
import tkinter as tk
from tkinter import ttk

from data_structure.ScaleData import ScaleData
from utils.Validation import DynamicValidation as dval

class ScaleDataSubFrame:
	def __init__(self):
		pass

	def edit_scale(self,target:tk.LabelFrame,data:ScaleData):
		subwindow = tk.Toplevel(target)
		subwindow.title("開発規模編集")
		subwindow.geometry("320x500")
		subwindow.resizable(False,False)
		subwindow.grab_set()
		is_numeric = subwindow.register(dval.is_numeric)
  
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="開発規模編集", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		label_desc= tk.Label(subwindow, text="覚えている限り記入してください。")
		label_desc.pack(side=tk.TOP,pady=5)

		edit_frame=tk.Frame(subwindow,borderwidth=0)
		edit_frame.pack(side=tk.TOP,expand=True,padx=20,pady=5)

		#ラベル定義
		tk.label(edit_frame, text="画面数：").grid(row=0,column=0,padx=2,pady=5)
		tk.label(edit_frame, text="バッチ数：").grid(row=1,column=0,padx=2,pady=5)
		tk.label(edit_frame, text="帳票数：").grid(row=2,column=0,padx=2,pady=5)

		#画面数
		text_gamens = ttk.Entry(edit_frame, width=5, textvariable=data.gamens,
				  validatecommand =(is_numeric, '%P', 3), validate='all')
		text_gamens.grid(row=0,column=1,padx=2,pady=5)
  
		#バッチ数
		text_batches = ttk.Entry(edit_frame, width=5, textvariable=data.batches,
				  validatecommand =(is_numeric, '%P', 3), validate='all')
		text_batches.grid(row=1,column=1,padx=2,pady=5)
  
		#帳票数
		text_forms = ttk.Entry(edit_frame, width=5, textvariable=data.forms,
				  validatecommand =(is_numeric, '%P', 3), validate='all')
		text_forms.grid(row=2,column=1,padx=2,pady=5)

		btn_ok["command"] = lambda: update(data)
		btn_cancel["command"] = lambda: cancel()

		def update(data:ScaleData):
			subwindow.destroy()

		def cancel():
			subwindow.destroy()
