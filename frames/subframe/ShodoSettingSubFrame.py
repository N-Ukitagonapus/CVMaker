import tkinter as tk
from tkinter import StringVar, ttk
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
		dlg.geometry("400x220")	# ウィンドウサイズ(幅x高さ)
		dlg.grab_set()

		txt_user_id, txt_project, txt_token = StringVar(), StringVar(), StringVar()
		txt_status, txt_result = StringVar(), StringVar()

		txt_user_id.set(setting.user_id)
		txt_project.set(setting.project_name)
		txt_token.set(setting.token)

		txt_status.set("OK" if setting.flg_able else "NG")
		txt_result.set("...")

		frame_title = tk.Frame(dlg,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="Shodo設定", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=3)

		frame_setting = tk.Frame(dlg,borderwidth=2,relief="groove")
		frame_setting.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=20,pady=2)
		tk.Label(frame_setting,text="ユーザID").grid(row=0,column=0)
		tk.Label(frame_setting,text="プロジェクト名").grid(row=1,column=0)
		tk.Label(frame_setting,text="トークン").grid(row=2,column=0)
		ttk.Entry(frame_setting,width=40,textvariable=txt_user_id).grid(row=0,column=1)
		ttk.Entry(frame_setting,width=40,textvariable=txt_project).grid(row=1,column=1)
		ttk.Entry(frame_setting,width=40,textvariable=txt_token).grid(row=2,column=1)

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
		btn_nosave = ttk.Button(subframe_button, width=15,text="保存せずに閉じる")
		btn_save = ttk.Button(subframe_button, width=15,text="保存して閉じる")
		btn_nosave.pack(side=tk.LEFT)
		btn_save.pack(side=tk.RIGHT)

		button_check["command"] = lambda: check_usage()
		btn_nosave["command"] = lambda: close_nosave()
		btn_save["command"] = lambda: close_save()

		def check_usage():
			setting.set_preference(txt_user_id.get(), txt_project.get(), txt_token.get())
			result = ShodoApi.check_availablity(setting)
			txt_status.set("OK" if setting.flg_able else "NG")
			txt_result.set(result)

		def close_nosave():
			dlg.destroy()

		def close_save():
			setting.set_preference(txt_user_id.get(), txt_project.get(), txt_token.get())
			ShodoApi.check_availablity(setting)
			conf = copa.ConfigParser()
			conf.add_section('ShodoSetting')
			conf.set("ShodoSetting","UserId",util.encode_key(txt_user_id.get()))
			conf.set("ShodoSetting","Project",util.encode_key(txt_project.get()))
			conf.set("ShodoSetting","Token",util.encode_key(txt_token.get()))
			with open(FILE["SHODO_SETTING"], 'w') as configfile:
				conf.write(configfile)
			dlg.destroy()