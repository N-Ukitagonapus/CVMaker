import tkinter as tk
from tkinter import BooleanVar, ttk
from tkinter.scrolledtext import ScrolledText

from data_structure.ShodoSetting import ShodoSetting
from utils.ShodoApiUtil import ShodoApi
import threading

class ShodoLintSubFrame:
	def __init__(self, top:tk.Frame):
		self.dlg = tk.Toplevel(top)
		self.dlg.title("文章校正")	# ウィンドウタイトル
		self.dlg.geometry("500x500")	# ウィンドウサイズ(幅x高さ)
		self.dlg.grab_set()

		#フレーム
		self.frame_check = tk.LabelFrame(self.dlg,borderwidth=2,relief="groove", text ="チェック結果")
		frame_beforetext = tk.LabelFrame(self.dlg,borderwidth=2,relief="groove", text ="校正前テキスト")
		frame_aftertext = tk.LabelFrame(self.dlg,borderwidth=2,relief="groove", text ="校正後テキスト")
		frame_state = tk.LabelFrame(self.dlg,borderwidth=2,relief="groove", text ="使用状況")
		frame_button = tk.Frame(self.dlg)

		self.text_before=ScrolledText(frame_beforetext,height=8)
		self.text_before.pack(side=tk.TOP,fill=tk.X,padx=2,pady=2)
		frame_beforetext.pack(side=tk.TOP,fill=tk.X,padx=2,pady=2)

		self.btn_cancel = ttk.Button(frame_button,text="キャンセル")
		self.btn_ok = ttk.Button(frame_button,text="OK",state=tk.DISABLED)
		self.btn_cancel.grid(row=0,column=0)
		self.btn_ok.grid(row=0,column=1)
		frame_button.pack(side=tk.BOTTOM,pady=2)

		self.label_state=ttk.Label(frame_state,text="しばらくおまちください")
		self.label_state.pack(side=tk.TOP,pady=2)
		frame_state.pack(side=tk.BOTTOM,fill=tk.X,padx=2,pady=2)

		self.text_after=ScrolledText(frame_aftertext,height=8)
		self.text_after.pack(fill=tk.X,padx=2,pady=2)
		frame_aftertext.pack(side=tk.BOTTOM,fill=tk.X,padx=2,pady=2)

		self.frame_check.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=2,pady=2)
		self.label_wait=ttk.Label(self.frame_check,text="しばらくおまちください")
		self.label_wait.pack()

	def lint(self, shodo:ShodoSetting, string:str, tgt:ScrolledText):

		def rewrite(check,res):
			newstr = list(string)
			deltas = []
			for i in range(len(res)):
				if check[i].get() == True:
					delta = 0
					for d in deltas:
						if res[i]["index"] > d["index"]:
							delta = d["delta"]
					index_from = res[i]["index"] - delta
					index_to = res[i]["index_to"] - delta
					newstr[index_from:index_to] = res[i]["after"]
					deltas.append({"index":res[i]["index_to"], "delta":len(res[i]["before"]) - len(res[i]["after"])})
			self.text_after["state"] = tk.NORMAL
			self.text_after.delete('1.0',tk.END)
			self.text_after.insert('1.0', "".join(newstr))
			self.text_after["state"] = tk.DISABLED

		def return_word():
			self.text_after["state"] = tk.NORMAL
			tgt.delete('1.0',tk.END)
			tgt.insert('1.0', self.text_after.get('1.0',tk.END))
			self.dlg.destroy()

		def create_checks(res):
			self.label_wait.destroy()
			scroll_area = tk.Canvas(self.frame_check)
			scrollbar_y = tk.Scrollbar(self.frame_check, orient=tk.VERTICAL, command=scroll_area.yview)
			scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

			scroll_area.pack(side=tk.TOP,fill=tk.BOTH,padx=3,pady=2)
			inner_scr=tk.Frame(scroll_area, width=460)

			tk.Label(inner_scr,borderwidth=1,relief="solid",text="行").grid(row=0,column=0,sticky=tk.W + tk.E)
			tk.Label(inner_scr,borderwidth=1,relief="solid",text="文字").grid(row=0,column=1,sticky=tk.W + tk.E)
			tk.Label(inner_scr,borderwidth=1,relief="solid",text="内容").grid(row=0,column=2,sticky=tk.W + tk.E)
			tk.Label(inner_scr,borderwidth=1,relief="solid",text="修正前").grid(row=0,column=3,sticky=tk.W + tk.E)
			tk.Label(inner_scr,borderwidth=1,relief="solid",text="修正後").grid(row=0,column=4,sticky=tk.W + tk.E)
			tk.Label(inner_scr,borderwidth=1,relief="solid",text="適用").grid(row=0,column=5,sticky=tk.W + tk.E)
			inner_scr.grid_columnconfigure(0, weight=1)
			inner_scr.grid_columnconfigure(1, weight=1)
			inner_scr.grid_columnconfigure(2, weight=1)
			inner_scr.grid_columnconfigure(3, weight=1)
			inner_scr.grid_columnconfigure(4, weight=1)
			inner_scr.grid_columnconfigure(5, weight=1)
			checkvar = []
			checkboxes = []
			for i in range(len(res)):
				checkvar.append(BooleanVar())
				result = res[i]
				tk.Label(inner_scr,borderwidth=1,relief="solid",text=result["from"]["line"]+1).grid(row=i+1,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
				tk.Label(inner_scr,borderwidth=1,relief="solid",text="{}～{}".format(result["from"]["ch"]+1,result["to"]["ch"]+1)).grid(row=i+1,column=1,sticky=tk.W+tk.E+tk.N+tk.S)
				tk.Message(inner_scr,borderwidth=1,relief="solid",text=result["message"]).grid(row=i+1,column=2,sticky=tk.W+tk.E+tk.N+tk.S)
				tk.Message(inner_scr,borderwidth=1,relief="solid",text="‐"if result["before"] is None else result["before"]).grid(row=i+1,column=3,sticky=tk.W+tk.E+tk.N+tk.S)
				tk.Message(inner_scr,borderwidth=1,relief="solid",text="‐"if result["after"] is None else result["after"]).grid(row=i+1,column=4,sticky=tk.W+tk.E+tk.N+tk.S)
				checkboxes.append(tk.Frame(inner_scr,borderwidth=1,relief="solid"))
				checkboxes[i].grid(row=i+1,column=5,sticky=tk.W+tk.E+tk.N+tk.S)
				if result["operation"] == "replace":
					ttk.Checkbutton(checkboxes[i],
											variable=checkvar[i],
											command=lambda:rewrite(
												checkvar,
												res
											)).pack()
				else:	tk.Label(checkboxes[i],text="‐").pack()
			inner_scr.pack(fill=tk.BOTH, expand=True)
			inner_scr.update()
			scroll_area.create_window((0,0), window=inner_scr, anchor=tk.NW, width=460)
			print(inner_scr.winfo_height())
			scroll_area.configure(scrollregion=(0, 0, 480, inner_scr.winfo_height()))
			scroll_area.configure(yscrollcommand=scrollbar_y.set)
			self.btn_ok["state"] = tk.NORMAL
			self.btn_ok["command"] = lambda: return_word()

		def do_lint(shodo, string):
			res = ShodoApi.lint_request(shodo, string)
			if len(res) == 0 :
				self.label_wait["text"] = "校正の必要はありません。"
			else :
				create_checks(res)
			nums = ShodoApi.get_nums(shodo)
			self.label_state["text"] = "現在の利用文字数/制限文字数：{0}/{1}　残り：あと{2}文字".format(nums["usage"],nums["limit"],nums["left"])


		self.text_before.insert('1.0', string)
		self.text_before["state"] = tk.DISABLED
		self.text_after.insert('1.0', string)
		self.text_after["state"] = tk.DISABLED

		self.thread_lint = threading.Thread(target=do_lint,args=[shodo, string])
		self.thread_lint.start()
		self.btn_cancel["command"] = lambda: self.dlg.destroy()




		


