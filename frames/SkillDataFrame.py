'''
技術情報フレーム
'''
from datetime import datetime
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
from constants.const import COLOR, ENV_GENRE, ENV_SET, VALID_ERR, VALID_OK
from fileio.SkillDataIO import SkillDataInput, SkillDataOutput
from frames.subframe.EnvironmentSubFrame import EnvironmentSubFrame
from utils.Utilities import Utilities as util
from tkinter import messagebox as msg
from data_structure.SkillData import SkillData
from utils.Validation import DynamicValidation as dval
from utils.Validation import StaticValidation as sval
from constants.message import DialogMessage as diag
from utils.Utilities import Utilities as util

class SkillDataFrame(tk.Frame):
	def __init__(self, target):
		self.data = SkillData()
		self.area_define(target)
		self.input_control(target)
		self.assembly()
  
	#エリア定義
	def area_define(self, target):
		#バリデーション定義
		is_numeric = target.register(dval.is_numeric)

		self.ret = tk.LabelFrame(target,relief=tk.RAISED,text = "技術情報")
		##1行目
		self.first_line=tk.Frame(self.ret)
  
		#フレーム・ラベル定義
		self.label_expr = tk.Label(self.first_line,text="業界経験開始年月")
		self.label_absense = tk.Label(self.first_line,text="休職期間")
		self.label_absense_yr = tk.Label(self.first_line,text="年")
		self.label_absense_mth = tk.Label(self.first_line,text="月")
  
		#業界経験開始年月
		self.str_start_date = StringVar()
		self.expr_start = DateEntry(self.first_line,day=1,locale='ja_JP',date_pattern='yyyy/mm/dd',textvariable=self.str_start_date)
		#休職期間-年
		self.text_absense_year = ttk.Entry(self.first_line, width=5,
				    textvariable=self.data.period_absense_year,
				 		validatecommand = (is_numeric, '%P', 3),
						validate='key')
		#休職期間-月
		self.select_absense_month = ttk.Combobox(self.first_line,width=3,state="readonly",justify="center",value=[i for i in range(0,12)],
				     textvariable=self.data.period_absense_month)
  	#読込ボタン
		self.btn_load = ttk.Button(self.first_line,width=5,text="読込")
		#保存ボタン
		self.btn_save = ttk.Button(self.first_line,width=5,text="保存")

		##2行目
		self.second_line=tk.Frame(self.ret)
		#フレーム・ラベル定義
		self.label_specialty = tk.Label(self.second_line,text="得意分野")
		#得意分野
		self.text_specialty = ttk.Entry(self.second_line,width=100,
				    	textvariable=self.data.specialty)

		#3行目
		self.third_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_qualifications = tk.Label(self.third_line,text="取得資格")
		self.label_environments = tk.Label(self.third_line,text="使用経験\n(業務外)")
  
		#取得資格
		self.btn_qual_edit = ttk.Button(self.third_line,width=5,text="編集")  

		#使用経験
		self.btn_env_edit = ttk.Button(self.third_line,width=5,text="編集")

		#4行目
		self.fourth_line=tk.Frame(self.ret)

		#フレーム・ラベル定義
		self.label_pr = tk.Label(self.fourth_line,text="自己PR")
		#自己PR
		self.text_pr = scrolledtext.ScrolledText(self.fourth_line,wrap=tk.WORD,width=80,height=5)  

	#組み立て
	def assembly(self):
		#1行目
		self.label_expr.pack(side=tk.LEFT)
		util.mark_required(self.first_line,self.label_expr)
		self.expr_start.pack(side=tk.LEFT,padx=5)
		self.label_absense.pack(side=tk.LEFT,padx=5)
		self.text_absense_year.pack(side=tk.LEFT,padx=5)
		self.label_absense_yr.pack(side=tk.LEFT,padx=5)
		self.select_absense_month.pack(side=tk.LEFT,padx=5)
		self.label_absense_mth.pack(side=tk.LEFT,padx=5)
		self.btn_save.pack(side=tk.RIGHT,padx=10)
		self.btn_load.pack(side=tk.RIGHT,padx=10)
		self.first_line.pack(side=tk.TOP,fill=tk.X,pady=5)

		#2行目
		self.label_specialty.pack(side=tk.LEFT)
		self.text_specialty.pack(side=tk.LEFT,padx=5)
		self.second_line.pack(side=tk.TOP,fill=tk.X,pady=5)
  
		#3行目
		self.label_qualifications.pack(side=tk.LEFT)
		self.btn_qual_edit.pack(side=tk.LEFT,padx=5)
		self.label_environments.pack(side=tk.LEFT,padx=5)
		self.btn_env_edit.pack(side=tk.LEFT,padx=5)
		self.third_line.pack(side=tk.TOP,fill=tk.X,pady=2)

		#4行目
		self.label_pr.grid(row=0,column=0,pady=5)
		self.text_pr.grid(row=1,column=1,padx=5,pady=5,sticky=tk.EW)
		self.fourth_line.grid_columnconfigure(1, weight=1)
		self.fourth_line.pack(side=tk.TOP,fill=tk.X,pady=2)
  
	#入力コントロール
	def input_control(self,target):
		def expr_start_set(*args):
			try:
				date_conv = util.get_first_date(datetime.strptime(self.str_start_date.get(),"%Y/%m/%d"))
				self.expr_start.set_date(date_conv)
				self.data.expr_start=date_conv
			except ValueError:
				return
		self.btn_load["command"] = lambda: self.data_read(target)
		self.btn_save["command"] = lambda: self.data_confirm(target)
		self.btn_qual_edit["command"] = lambda:self.edit_qualifications(self.ret)
		self.btn_env_edit["command"]  = lambda:EnvironmentSubFrame().edit_envs(target, "使用経験編集", self.data.expr_env)
		self.str_start_date.trace('w',expr_start_set)
  
	#データ出力
	def data_confirm(self,target):
		def final_validation(input_data: SkillData):
			input_data.expr_start=self.expr_start.get_date()
			input_data.pr=self.text_pr.get('1.0',self.text_pr.index(tk.END))
			sval.out_date_check(vals["expr_start"],input_data.expr_start)
			sval.io_novalidation(vals["absense"])
			sval.out_warn_if_empty(vals["specialty"],input_data.specialty.get())
			sval.io_novalidation(vals["qualifications"])
			sval.io_novalidation(vals["expr_env"])
			sval.out_warn_if_empty(vals["pr"],input_data.pr)

		vals = {
			"expr_start":{"label":"業務開始日"},
			"absense":{"label":"休職期間"},
			"specialty":{"label":"得意分野"},
			"qualifications":{"label":"取得資格"},
			"expr_env":{"label":"使用経験(業務外)"},
			"pr":{"label":"自己PR"}
		}
  
		final_validation(self.data)
		total_val = True
		for val in vals.values():
			if val["result"] == VALID_ERR:
				total_val = False
				break

		subwindow = tk.Toplevel(target)
		subwindow.title("データ確認")
		subwindow.geometry("400x330")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_output = ttk.Button(frame_button_inner,width=10)
		button_output["text"] = "出力" if total_val == True else "強制出力"
		button_cancel = ttk.Button(frame_button_inner,width=10,text="キャンセル")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
		frame_button_inner.pack(pady=5)
		button_cancel.grid(row=0,column=0,padx=15)
		button_output.grid(row=0,column=1,padx=15)

		frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "技術情報 データ出力")
		frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
		frame_main_inner=tk.Frame(frame_main)
		frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)

		frame_name = []
		frame_result = []
		results = list(vals.items())
		for i in range(len(results)):
			frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg="white"))
			frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg=COLOR[results[i][1]["result"]]))
			frame_name[i].grid(row=i,column=0,sticky=tk.EW)
			frame_result[i].grid(row=i,column=1,sticky=tk.EW)
			tk.Label(frame_name[i],text=results[i][1]["label"],bg="white").pack(side=tk.LEFT,padx=3,pady=3)
			tk.Label(frame_result[i],text=results[i][1]["msg"],bg=COLOR[results[i][1]["result"]]).pack(side=tk.LEFT,padx=3,pady=3)
		frame_main_inner.columnconfigure(index=1, weight=1)

		button_output["command"] = lambda: output()
		button_cancel["command"] = lambda: cancel()

		def output():
			if total_val == VALID_ERR:
				if util.msgbox_ask(diag.DIALOG_ASK_FORCE_OUTPUT):
					do_output()
			else:
				do_output()

		def do_output():
			try:
				SkillDataOutput(self.data).output()
			except Exception as e:
				print(e)
				util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	#データ入力
	def data_read(self,target):
		def inputcheck(input:dict):
			sval.in_date_check(input["expr_start"])
			sval.in_regex_match(input["absense_year"],"[0-9]*","数字")
			sval.in_number_between(input["absense_month"],0,11,"0から11の間")
			sval.io_novalidation(input["specialty"])
			sval.io_novalidation(input["qualifications"])
			sval.io_novalidation(input["environments"])
			sval.io_novalidation(input["pr"])
	
		def set_value(input):
			util.setdate_from_read(self.expr_start,input["expr_start"])
			self.data.expr_start = self.expr_start.get_date()
			util.setstr_from_read(self.data.period_absense_year,input["absense_year"])
			util.setstr_from_read(self.data.period_absense_month,input["absense_month"])
			util.setstr_from_read(self.data.specialty,input["specialty"])
			self.data.qualifications = input["qualifications"]["value"]
			self.data.expr_env.set_values(input["environments"]["value"])
			self.data.pr = input["pr"]["value"]
			self.text_pr.delete("1.0","end")
			self.text_pr.insert('1.0',(input["pr"]["value"]))

		#ファイル読み込み結果表示
		def show_result(input,target):
			subwindow = tk.Toplevel(target)
			subwindow.title("ファイル読込結果")
			subwindow.geometry("500x390")
			subwindow.resizable(False,False)
			subwindow.grab_set()

			frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
			frame_button_inner = tk.Frame(frame_button)
			button_ok = ttk.Button(frame_button_inner,width=10,text="OK")
			frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=8)
			frame_button_inner.pack(pady=5)
			button_ok.grid(row=0,column=0,padx=15)

			frame_main = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "技術情報 ファイル読込結果")
			frame_main.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=8)
			frame_main_inner=tk.Frame(frame_main)
			frame_main_inner.pack(fill=tk.BOTH,padx=5,pady=5)

			frame_name = []
			frame_result = []
			results = list(input.items())
			for i in range(len(results)):
				frame_name.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg="white"))
				frame_result.append(tk.Frame(frame_main_inner,borderwidth=1,relief=tk.SOLID,bg=COLOR[results[i][1]["result"]]))
				frame_name[i].grid(row=i,column=0,sticky=tk.EW)
				frame_result[i].grid(row=i,column=1,sticky=tk.EW)
				tk.Label(frame_name[i],text=results[i][1]["label"],bg="white").pack(side=tk.LEFT,padx=3,pady=3)
				tk.Label(frame_result[i],text=results[i][1]["msg"],bg=COLOR[results[i][1]["result"]]).pack(side=tk.LEFT,padx=3,pady=3)
			frame_main_inner.columnconfigure(index=1, weight=1)
			button_ok["command"] = lambda: subwindow.destroy()

		try:
			input = SkillDataInput().read()
			inputcheck(input)
			set_value(input)
			show_result(input, target)
		except Exception as e:
			print(e)
			util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)

	#取得資格編集サブウィンドウ
	def edit_qualifications(self,target):
		subwindow = tk.Toplevel(target)
		subwindow.title("資格情報編集")
		subwindow.geometry("320x320")
		subwindow.resizable(False,False)
		subwindow.grab_set()
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="取得資格編集", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		label_desc= tk.Label(subwindow, text="複数ある場合は改行区切りで入力してください。")
		label_desc.pack(side=tk.TOP,pady=5)
		text= scrolledtext.ScrolledText(subwindow,wrap=tk.WORD)
		text.insert('1.0',"\n".join(self.data.qualifications))
		text.pack(side=tk.TOP,fill=tk.X,expand=True,padx=20,pady=5)

		btn_ok["command"] = lambda: update()
		btn_cancel["command"] = lambda: cancel()

		def update():
			self.data.qualifications = util.tidy_list((text.get('1.0',text.index(tk.END))).split("\n"))
			subwindow.destroy()

		def cancel():
			subwindow.destroy()

	def pack(self):
		self.ret.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)