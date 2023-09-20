import copy
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from constants.const import ENV_GENRE, ENV_SET
from utils.Utilities import Utilities as util
from data_structure.EnvironmentData import EnvironmentData

class EnvironmentSubFrame:
	"""
	開発環境サブウィンドウ
	"""
	def __init__(self):
		pass

	def edit_envs(self,target:tk.Frame,title:str,data:EnvironmentData):
		"""
		開発環境編集サブウィンドウ表示
		Args:
				target (tk.Frame): サブウィンドウ表示元フレーム(=メインフレーム)
				title (str): サブウィンドウタイトル
				data (EnvironmentData): 開発環境データ
		"""
		subwindow = tk.Toplevel(target)
		subwindow.title(title)
		subwindow.geometry("1000x320")
		subwindow.resizable(False,False)
		subwindow.grab_set()
  
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text=title, font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)
  
		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		label_desc = tk.Label(subwindow, text="複数ある場合は改行区切りで入力してください。")
		label_desc.pack(side=tk.TOP,pady=5)

		frame_edit = tk.Frame(subwindow)
		envs = list(ENV_GENRE.items())
		label_envs={}
		text_envs={}
		entry_envs=data.get_values()
		for i in range(len(envs)):
			label_envs[envs[i][0]]=tk.Label(frame_edit, text=envs[i][1])
			text_envs[envs[i][0]]=ScrolledText(frame_edit,wrap=tk.WORD)
			text_envs[envs[i][0]].insert('1.0',"\n".join(entry_envs[envs[i][0]]))
			label_envs[envs[i][0]].grid(row=0,column=i,padx=2,pady=5)
			text_envs[envs[i][0]].grid(row=1,column=i,padx=2,pady=5)
			frame_edit.grid_columnconfigure(i, weight=1)
		frame_edit.grid_rowconfigure(1, weight=1)
		frame_edit.pack(side=tk.TOP,expand=True,padx=10,pady=5)
		btn_ok["command"] = lambda: update()
		btn_cancel["command"] = lambda: cancel()

		def update():
			"""
   		データ更新
			"""
			env_set = copy.deepcopy(ENV_SET)
			for key in text_envs.keys():
				env_set[key] = util.tidy_list(str.strip(text_envs[key].get('1.0',tk.END)).split("\n"))
			data.set_values(env_set)
			subwindow.destroy()

		def cancel():
			"""
   		キャンセル
			"""
			subwindow.destroy()