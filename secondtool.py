import configparser as copa

import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.scrolledtext import ScrolledText

from data_structure.ShodoSetting import ShodoSetting
from fileio.ExcelOutput import ExcelOutput
from constants.const import COLOR, FILE, STATUS_GREEN, STATUS_RED, icon
from frames.subframe.ShodoLintSubFame import ShodoLintSubFrame
from frames.subframe.ShodoSettingSubFrame import ShodoSettingSubFrame
from utils.Utilities import Utilities as util, resource_path
from utils.ShodoApiUtil import ShodoApi as shodoapi
from constants.message import DialogMessage as diag


class Application(tk.Frame):
	def __init__(self, master = None):
		
		self.txt_org_name, self.txt_project, self.txt_token = StringVar(), StringVar(), StringVar()
		self.txt_result =  StringVar()

		super().__init__(master)
		width = 480
		height = 480
    #ウィンドウ設定
		self.master.title("K.S.A.M SubToolTest")
		self.master.geometry(f"{width}x{height}")
		self.create_widgets()
		self.get_shodo_setting()
		self.check()
		
	def get_shodo_setting(self):
		"""
		SHODO設定
		"""
		self.shodo = ShodoSetting()
		try:
			conf = copa.ConfigParser()
			conf.read(FILE["SHODO_SETTING"])
			user_id = util.decode_key(conf.get("ShodoSetting","UserId"))
			project_name = util.decode_key(conf.get("ShodoSetting","Project"))
			token = util.decode_key(conf.get("ShodoSetting","Token"))
			self.txt_org_name.set(user_id)
			self.txt_project.set(project_name)
			self.txt_token.set(token)
		except Exception as err:
			pass

	def check(self):
		self.shodo.set_preference(self.txt_org_name.get(), self.txt_project.get(), self.txt_token.get())
		result = shodoapi.check_availablity(self.shodo)
		self.button_lint["state"] = tk.ACTIVE if self.shodo.flg_able == True else tk.DISABLED
		self.txt_result.set(result)

	def lint(self, shodo:ShodoSetting, string:str, tgt:ScrolledText):
		if len(string) == 0:
			util.msgbox_showmsg(diag.DIALOG_ERROR_EMPTYTEXT)
		else:
			try:
				sub_lint = ShodoLintSubFrame(self.master)
				sub_lint.lint(shodo, string, tgt)
			except Exception as e:
				print(e)
			finally:
				del sub_lint

	def create_widgets(self):
		"""
		ウィジェット生成
		"""
		#タイトル設定
		frame_title = tk.Frame(self.master,borderwidth=5,relief="groove")
		#タイトル
		tk.Label(frame_title, text="Shodoお試しツール", font=("Meiryo UI",20,"bold","italic")).pack(side=tk.LEFT,padx=10,pady=10)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)
		
    #設定フレーム
		frame_setting = tk.LabelFrame(self.master,borderwidth=2,relief="groove", text ="設定")
		frame_setting.pack(side=tk.TOP,padx=20,pady=2)
		#入力欄
		subframe_setting = tk.Frame(frame_setting)
		subframe_setting.pack(side=tk.TOP,padx=10,pady=5)
		tk.Label(subframe_setting,text="組織名").grid(row=0,column=0)
		tk.Label(subframe_setting,text="プロジェクト名").grid(row=1,column=0)
		tk.Label(subframe_setting,text="トークン").grid(row=2,column=0)
		ttk.Entry(subframe_setting,width=40,textvariable=self.txt_org_name).grid(row=0,column=1)
		ttk.Entry(subframe_setting,width=40,textvariable=self.txt_project).grid(row=1,column=1)
		ttk.Entry(subframe_setting,width=40,show="■",textvariable=self.txt_token).grid(row=2,column=1)
  
    #ステータス
		frame_status = tk.Frame(frame_setting)
		frame_status.pack(side=tk.TOP,fill=tk.X,padx=10,pady=5)
		tk.Label(frame_status,text="ステータス：").pack(side=tk.LEFT)
		tk.Label(frame_status).pack(side=tk.LEFT)
		subframe_check = tk.Frame(frame_status,borderwidth=2,relief="groove")
		subframe_check.pack(side=tk.TOP,fill=tk.X)
		tk.Label(subframe_check,textvariable=self.txt_result).pack(side=tk.LEFT)
		button_check = ttk.Button(subframe_check,width=8,text="チェック")
		button_check.pack(side=tk.RIGHT)
		
    #ボタン
		btnarea = tk.Frame(self.master)
		btnarea.pack(side=tk.BOTTOM,pady=5)
		self.button_lint = ttk.Button(btnarea,padding=[5,5],text="校正実行",state=tk.DISABLED)
		self.button_lint.pack(side=tk.BOTTOM)
    
    #テキスト
		textframe = tk.LabelFrame(self.master,borderwidth=2,relief="groove", text ="テキスト")
		textframe.pack(side=tk.TOP,padx=20,pady=5,fill=tk.BOTH,expand=True)
		textarea = ScrolledText(textframe,wrap=tk.WORD)
		textarea.pack(side=tk.TOP,padx=5,pady=5,fill=tk.BOTH)

		#ボタン制御
		button_check["command"] = lambda: self.check()
		self.button_lint["command"] = lambda: self.lint(self.shodo,str.strip(textarea.get('1.0',tk.END)), textarea)

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(True,True)
	root.minsize(640, 480)
	app = Application(master = root)
	app.mainloop()