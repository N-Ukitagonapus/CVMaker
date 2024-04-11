import tkinter as tk
from tkinter import BooleanVar, StringVar, ttk
from constants.const import FILE
from data_structure.ShodoSetting import ShodoSetting
from utils.ShodoApiUtil import ShodoApi
from utils.Utilities import Utilities as util
import configparser as copa

class ShodoSettingSubFrame:
	@staticmethod
	def show_setting(target,setting:ShodoSetting):
		
		dlg = tk.Toplevel(target)
		dlg.title("Shodo設定")	# ウィンドウタイトル
		dlg.geometry("400x240")	# ウィンドウサイズ(幅x高さ)
		dlg.grab_set()

		txt_org_name, txt_project, txt_token = StringVar(), StringVar(), StringVar()
		txt_status, txt_result = StringVar(), StringVar()
		checkbox_use = BooleanVar()

		txt_org_name.set(setting.org_name)
		txt_project.set(setting.project_name)
		txt_token.set(setting.token)

		txt_status.set("OK" if setting.flg_able else "NG")
		txt_result.set("...")

		frame_title = tk.Frame(dlg,borderwidth=5,relief="groove")
		tk.Label(frame_title, text="Shodo設定", font=("Meiryo UI",16,"bold")).pack(side=tk.TOP,padx=10)
		tk.Label(frame_title, text="Shodoについてはこちら -> https://shodo.ink/", font=("Meiryo UI",8,"italic")).pack(anchor=tk.NE,padx=5,pady=2)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=3)

		frame_setting = tk.Frame(dlg,borderwidth=2,relief="groove")
		frame_setting.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=20,pady=2)
		tk.Label(frame_setting,text="組織名").grid(row=0,column=0)
		tk.Label(frame_setting,text="プロジェクト名").grid(row=1,column=0)
		tk.Label(frame_setting,text="トークン").grid(row=2,column=0)
		ttk.Entry(frame_setting,width=40,textvariable=txt_org_name).grid(row=0,column=1)
		ttk.Entry(frame_setting,width=40,textvariable=txt_project).grid(row=1,column=1)
		ttk.Entry(frame_setting,width=40,show="■",textvariable=txt_token).grid(row=2,column=1)

		frame_status = tk.Frame(dlg,borderwidth=2,relief="groove")
		frame_status.pack(side=tk.TOP,fill=tk.BOTH,padx=20,pady=2)
		subframe_status = tk.Frame(frame_status)
		subframe_status.pack(side=tk.TOP,fill=tk.X)
		tk.Label(subframe_status,text="ステータス：").pack(side=tk.LEFT)
		tk.Label(subframe_status,textvariable=txt_status).pack(side=tk.LEFT)
		subframe_check = tk.Frame(frame_status,borderwidth=2,relief="groove")
		subframe_check.pack(side=tk.TOP,fill=tk.X)
		tk.Label(subframe_check,textvariable=txt_result).pack(side=tk.LEFT)
		button_check = ttk.Button(subframe_check,width=8,text="チェック")
		button_check.pack(side=tk.RIGHT)

		frame_command = tk.Frame(dlg,borderwidth=2,relief="groove")
		frame_command.pack(side=tk.BOTTOM,fill=tk.X,padx=20,pady=3)
		subframe_button = tk.Frame(frame_command)
		subframe_button.pack(side=tk.TOP)
		checkbox_use.set(setting.use)
		chk_use = ttk.Checkbutton(subframe_button, text="文章校正を使用する", variable = checkbox_use, state=tk.NORMAL if setting.flg_able else tk.DISABLED)
		btn_nosave = ttk.Button(subframe_button, width=15,text="保存せずに閉じる")
		btn_save = ttk.Button(subframe_button, width=15,text="保存して閉じる")
		chk_use.pack(side=tk.LEFT,padx=2)
		btn_nosave.pack(side=tk.LEFT,padx=2)
		btn_save.pack(side=tk.RIGHT,padx=2)

		button_check["command"] = lambda: check_usage()
		btn_nosave["command"] = lambda: close_nosave()
		btn_save["command"] = lambda: close_save()

		def check_usage():
			setting.set_preference(txt_org_name.get(), txt_project.get(), txt_token.get())
			result = ShodoApi.check_availablity(setting)
			txt_status.set("OK" if setting.flg_able else "NG")
			txt_result.set(result)
			chk_use["state"] = tk.NORMAL if setting.flg_able else tk.DISABLED
   
		def close_nosave():
			dlg.destroy()

		def close_save():
			setting.set_preference(txt_org_name.get(), txt_project.get(), txt_token.get())

			ShodoApi.check_availablity(setting)
			conf = copa.ConfigParser()
			conf.add_section('ShodoSetting')
			conf.set("ShodoSetting","UserId",util.encode_key(txt_org_name.get()))
			conf.set("ShodoSetting","Project",util.encode_key(txt_project.get()))
			conf.set("ShodoSetting","Token",util.encode_key(txt_token.get()))
			with open(FILE["SHODO_SETTING"], 'w') as configfile:
				conf.write(configfile)
			setting.use = checkbox_use.get()
			dlg.destroy()