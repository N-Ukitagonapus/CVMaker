'''
開発規模サブウィンドウ
'''
import tkinter as tk
from tkinter import ttk

from data_structure.ScaleData import ScaleData
from utils.Utilities import Utilities as util
from utils.Validation import DynamicValidation as dval

class ScaleDataSubFrame:
	def __init__(self):
		pass

	def edit_scale(self,target:tk.LabelFrame,data:ScaleData):
		subwindow = tk.Toplevel(target)
		subwindow.title("開発規模編集")
		subwindow.geometry("320x360")
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
		tk.Label(edit_frame, text="画面数：").grid(row=0,column=0,padx=2,pady=5)
		tk.Label(edit_frame, text="バッチ数：").grid(row=1,column=0,padx=2,pady=5)
		tk.Label(edit_frame, text="帳票数：").grid(row=2,column=0,padx=2,pady=5)
		tk.Label(edit_frame, text="総ステップ数：").grid(row=5,column=0,padx=2,pady=5)

		#画面数
		val_gamens = tk.StringVar()
		text_gamens = ttk.Entry(edit_frame, width=5 , textvariable = val_gamens,
			validatecommand =(is_numeric, '%P', 3), validate='all')
		text_gamens.grid(row=0,column=1,padx=2,pady=5)
  
		#バッチ数
		val_batches = tk.StringVar()
		text_batches = ttk.Entry(edit_frame, width=5, textvariable = val_batches,
			validatecommand =(is_numeric, '%P', 3), validate='all')
		text_batches.grid(row=1,column=1,padx=2,pady=5)
  
		#帳票数
		val_forms = tk.StringVar()
		text_forms = ttk.Entry(edit_frame, width=5, textvariable = val_forms,
			validatecommand =(is_numeric, '%P', 3), validate='all')
		text_forms.grid(row=2,column=1,padx=2,pady=5)

		#その他1
		val_etc1_name = tk.StringVar()
		text_etc1_name = ttk.Entry(edit_frame, width=15, textvariable = val_etc1_name)
		text_etc1_name.grid(row=3,column=0,padx=2,pady=5)
		val_etc1_num = tk.StringVar()
		text_etc1_num = ttk.Entry(edit_frame, width=5, textvariable = val_etc1_num,
			validatecommand =(is_numeric, '%P', 3), validate='all')
		text_etc1_num.grid(row=3,column=1,padx=2,pady=5)

		#その他2
		val_etc2_name = tk.StringVar()
		text_etc2_name = ttk.Entry(edit_frame, width=15, textvariable = val_etc2_name)
		text_etc2_name.grid(row=4,column=0,padx=2,pady=5)
		val_etc2_num = tk.StringVar()
		text_etc2_num = ttk.Entry(edit_frame, width=5, textvariable = val_etc2_num,
			validatecommand =(is_numeric, '%P', 3), validate='all')
		text_etc2_num.grid(row=4,column=1,padx=2,pady=5)

		#総ステップ数
		val_total_steps = tk.StringVar()
		text_total_steps = ttk.Entry(edit_frame, width=7, textvariable = val_total_steps,
			validatecommand =(is_numeric, '%P', 5), validate='all')
		text_total_steps.grid(row=5,column=1,padx=2,pady=5)
  
		edit_frame.grid_columnconfigure(0, weight=1)
		edit_frame.grid_columnconfigure(1, weight=1)
		edit_frame.grid_rowconfigure(0, weight=1)
		edit_frame.grid_rowconfigure(1, weight=1)
		edit_frame.grid_rowconfigure(2, weight=1)
		edit_frame.grid_rowconfigure(3, weight=1)
		edit_frame.grid_rowconfigure(4, weight=1)
		edit_frame.grid_rowconfigure(5, weight=1)

		val_gamens.set(data.gamens)
		val_batches.set(data.batches)
		val_forms.set(data.forms)
		val_etc1_name.set(data.etc1_name)
		val_etc1_num.set(data.etc1_num)
		val_etc2_name.set(data.etc2_name)
		val_etc2_num.set(data.etc2_num)
		val_total_steps.set(data.total_steps)

		btn_ok["command"] = lambda: update(data)
		btn_cancel["command"] = lambda: cancel()

		def update(data:ScaleData):
			data.gamens = util.int_from_str(val_gamens.get())
			data.batches = util.int_from_str(val_batches.get())
			data.forms   = util.int_from_str(val_forms.get())
			data.etc1_name = val_etc1_name.get()
			data.etc1_num  = util.int_from_str(val_etc1_num.get())
			data.etc2_name = val_etc2_name.get()
			data.etc2_num  = util.int_from_str(val_etc2_num.get())
			data.total_steps  = util.int_from_str(val_total_steps.get())
			subwindow.destroy()

		def cancel():
			subwindow.destroy()
