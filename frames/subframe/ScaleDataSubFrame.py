'''
開発規模サブウィンドウ
'''
import tkinter as tk
from tkinter import StringVar, ttk

from data_structure.ScaleData import ScaleData
from utils.Utilities import Utilities as util
from utils.Validation import DynamicValidation as dval

class ScaleDataSubFrame:
  #初期化
	def __init__(self):
		pass
	#開発規模編集
	def edit_scale(self,target:tk.LabelFrame,data:ScaleData):
		#入力部品構築
		def grid_input(frame:tk.LabelFrame,row:int,var:StringVar,tani:str):
			f_inner = tk.Frame(frame, borderwidth=0)
			ttk.Entry(f_inner, width=10 , textvariable = var, validatecommand =(is_numeric, '%P', 6), validate='all').pack(side=tk.LEFT)
			tk.Label(f_inner, text=tani).pack(side=tk.LEFT,padx=5)
			f_inner.grid(row=row,column=1,padx=2,pady=5)
   
		subwindow = tk.Toplevel(target)
		subwindow.title("開発規模編集")
		subwindow.geometry("320x600")
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

		f_designing=tk.LabelFrame(subwindow,relief=tk.RAISED,text = "設計")
		f_designing.pack(side=tk.TOP,fill=tk.X,expand=True,padx=20,pady=5)
  
		f_coding=tk.LabelFrame(subwindow,relief=tk.RAISED,text = "製造")
		f_coding.pack(side=tk.TOP,fill=tk.X,expand=True,padx=20,pady=5)

		f_testing=tk.LabelFrame(subwindow,relief=tk.RAISED,text = "テスト")
		f_testing.pack(side=tk.TOP,fill=tk.X,expand=True,padx=20,pady=5)

		#入力変数定義
		val_bds = StringVar()				#設計：基本
		val_dds = StringVar()				#設計：詳細
		val_gamens = StringVar()		#製造：画面数
		val_batches = StringVar()		#製造：バッチ数
		val_forms = StringVar()			#製造：帳票
		val_etc1_name = StringVar()	#製造：その他1名称
		val_etc1_num = StringVar()	#製造：その他1本数
		val_etc2_name = StringVar()	#製造：その他2名称
		val_etc2_num = StringVar()	#製造：その他2本数
		val_total_steps = StringVar()
		val_uts = StringVar()				#設計：基本
		val_its = StringVar()				#設計：詳細
		val_sts = StringVar()				#設計：基本
  
		#ラベル定義
		##設計
		tk.Label(f_designing, text="基本設計").grid(row=0,column=0,padx=2,pady=5)
		tk.Label(f_designing, text="詳細設計").grid(row=1,column=0,padx=2,pady=5)
		##製造
		tk.Label(f_coding, text="画面").grid(row=0,column=0,padx=2,pady=5)
		tk.Label(f_coding, text="バッチ").grid(row=1,column=0,padx=2,pady=5)
		tk.Label(f_coding, text="帳票").grid(row=2,column=0,padx=2,pady=5)
		ttk.Entry(f_coding, width=15, textvariable = val_etc1_name).grid(row=3,column=0,padx=2,pady=5)
		ttk.Entry(f_coding, width=15, textvariable = val_etc2_name).grid(row=4,column=0,padx=2,pady=5)
		tk.Label(f_coding, text="総ステップ").grid(row=5,column=0,padx=2,pady=5)
		##テスト
		tk.Label(f_testing, text="単体テスト").grid(row=0,column=0,padx=2,pady=5)
		tk.Label(f_testing, text="結合テスト").grid(row=1,column=0,padx=2,pady=5)
		tk.Label(f_testing, text="総合テスト").grid(row=2,column=0,padx=2,pady=5)

		#入力定義
		##設計
		grid_input(f_designing,0,val_bds,"機能")
		grid_input(f_designing,1,val_dds,"機能")
		##製造
		grid_input(f_coding,0,val_gamens,"本")
		grid_input(f_coding,1,val_batches,"本")
		grid_input(f_coding,2,val_forms,"本")
		grid_input(f_coding,3,val_etc1_num,"本")
		grid_input(f_coding,4,val_etc2_num,"本")
		grid_input(f_coding,5,val_total_steps,"ステップ")
		##テスト
		grid_input(f_testing,0,val_uts,"ケース")
		grid_input(f_testing,1,val_its,"ケース")
		grid_input(f_testing,2,val_sts,"ケース")

		#グリッド調整
		f_designing.grid_columnconfigure(0, weight=1)
		f_designing.grid_columnconfigure(1, weight=1)
		f_coding.grid_columnconfigure(0, weight=1)
		f_coding.grid_columnconfigure(1, weight=1)
		f_testing.grid_columnconfigure(0, weight=1)
		f_testing.grid_columnconfigure(1, weight=1)

		#データ取込
		##設計
		val_bds.set(data.des_base)
		val_dds.set(data.des_detail)
		##製造
		val_gamens.set(data.gamens)
		val_batches.set(data.batches)
		val_forms.set(data.forms)
		val_etc1_name.set(data.etc1_name)
		val_etc1_num.set(data.etc1_num)
		val_etc2_name.set(data.etc2_name)
		val_etc2_num.set(data.etc2_num)
		val_total_steps.set(data.total_steps)
		##テスト
		val_uts.set(data.uts)
		val_its.set(data.its)
		val_sts.set(data.sts)


		btn_ok["command"] = lambda: update(data)
		btn_cancel["command"] = lambda: cancel()

		#データ更新
		def update(data:ScaleData):
    	##設計
			data.des_base=util.int_from_str(val_bds.get())
			data.des_detail=util.int_from_str(val_dds.get())
			##製造
			data.gamens = util.int_from_str(val_gamens.get())
			data.batches = util.int_from_str(val_batches.get())
			data.forms   = util.int_from_str(val_forms.get())
			data.etc1_name = val_etc1_name.get()
			data.etc1_num  = util.int_from_str(val_etc1_num.get())
			data.etc2_name = val_etc2_name.get()
			data.etc2_num  = util.int_from_str(val_etc2_num.get())
			data.total_steps  = util.int_from_str(val_total_steps.get())
			##テスト
			data.uts=util.int_from_str(val_uts.get())
			data.its=util.int_from_str(val_its.get())
			data.sts=util.int_from_str(val_sts.get())
			subwindow.destroy()

		#キャンセル
		def cancel():
			subwindow.destroy()
