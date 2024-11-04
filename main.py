import configparser as copa
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from data_structure.ShodoSetting import ShodoSetting
from fileio.ExcelOutput import ExcelOutput
from constants.const import COLOR, FILE, STATUS_GREEN, STATUS_RED, icon
from frames.subframe.ShodoSettingSubFrame import ShodoSettingSubFrame
from utils.Validation import DynamicValidation as dval
from frames.PersonalDataFrame import PersonalDataFrame
from frames.SkillDataFrame import SkillDataFrame
from frames.CareerHistoryFrame import CareerHistoryFrame
from utils.Utilities import Utilities as util, resource_path
from utils.ShodoApiUtil import ShodoApi as shodoapi
from constants.message import DialogMessage as diag
import pyautogui as pag

VERSION = 1.29
scr_w,scr_h= pag.size()
class Application(tk.Frame):
	global icon
	def __init__(self, master = None):
		super().__init__(master)
		width = 1200
		height = 900 if scr_h > 900 else (scr_h - 50)
		#ウィンドウ設定
		self.master.title("K.S.A.M")
		self.master.geometry(f"{width}x{height}")

		self.get_shodo_setting()
		self.create_widgets()

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
			self.shodo.set_preference(user_id, project_name, token)
			shodoapi.check_availablity(self.shodo)
		except Exception as err:
			pass

	def create_widgets(self):
		"""
		ウィジェット生成
		"""
		#タイトル設定
		self.frame_title = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.icon_zone = tk.Canvas(self.frame_title, bg="#deb887", height=50, width=50)
		self.icon_zone.pack(side=tk.LEFT,padx=10,pady=10)
		icon = Image.open(resource_path("img\\ksam_icon.png"))
		icon = icon.resize((50,50))
		self.icon = ImageTk.PhotoImage(icon)
		self.icon_zone.create_image(27, 27, image=self.icon)
		#タイトル
		tk.Label(self.frame_title, text="Kushimsoft Skillsheet Automatic Maker", font=("Meiryo UI",20,"bold","italic")).pack(side=tk.LEFT,padx=10,pady=10)
		# バージョン
		tk.Label(self.frame_title, text="Version {0}".format(VERSION), font=("Meiryo UI",10,"italic")).pack(anchor=tk.NE,padx=5,pady=5)
		# 作者
		tk.Label(self.frame_title, text="Created by N.Ukita", font=("Meiryo UI",10,"italic")).pack(anchor=tk.SE,padx=5,pady=5)

		self.frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		#ボタンエリア
		self.frame_bottombutton = tk.Frame(self.master,borderwidth=5,relief=tk.GROOVE)
		self.frame_bottombutton.pack(side=tk.BOTTOM,fill=tk.X,padx=20,pady=10)
		self.buttom_buttonfieldR = tk.Frame(self.frame_bottombutton)
		self.buttom_buttonfieldR.pack(side=tk.RIGHT)
		self.buttom_buttonfieldL = tk.Frame(self.frame_bottombutton)
		self.buttom_buttonfieldL.pack(side=tk.LEFT)
		#エクスポートボタン
		self.button_export = ttk.Button(self.buttom_buttonfieldR,width=20,text="Excel出力")
		self.button_export.pack(side=tk.RIGHT,padx=10,pady=5)
		#SHODOボタン
		self.button_shodo = ttk.Button(self.buttom_buttonfieldL,width=20,text="Shodo設定")
		self.label_shodo = ttk.Label(self.buttom_buttonfieldL,text="Shodo状態：")
		self.status_shodo = ttk.Label(self.buttom_buttonfieldL)
		self.button_shodo.pack(side=tk.LEFT,padx=10,pady=5)
		self.label_shodo.pack(side=tk.LEFT,pady=5)
		self.status_shodo.pack(side=tk.LEFT,pady=5)

		#スクロール部分
		self.main_area = tk.Frame(self.master)
		self.main_area.pack(expand=True, fill=tk.BOTH)
		self.scroll_area = tk.Canvas(self.main_area, width = 1180, height = 740)
		self.scrollbar_y = tk.Scrollbar(self.main_area, orient=tk.VERTICAL, command=self.scroll_area.yview)
		self.scrollbar_x = tk.Scrollbar(self.main_area, orient=tk.HORIZONTAL, command=self.scroll_area.xview)
		self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
		self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
		self.scroll_area.configure(scrollregion=(0, 0, 1180, 740))
		self.scroll_area.configure(yscrollcommand=self.scrollbar_y.set)
		self.scroll_area.configure(xscrollcommand=self.scrollbar_x.set)
		self.scroll_area.pack(expand=True, fill=tk.BOTH)

		self.scroll_frame = tk.Frame(self.scroll_area)
		self.scroll_area.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=1180, height=740)


		self.frame_personal = PersonalDataFrame(self.scroll_frame)
		self.frame_personal.pack()

		self.frame_skill = SkillDataFrame(self.scroll_frame, self.shodo)
		self.frame_skill.pack()

		self.frame_history = CareerHistoryFrame(self.scroll_frame, self.shodo)
		self.frame_history.pack()

		self.frame_personal.data.name_last_kanji.trace_add('write',self.sync_shi)
		self.frame_personal.data.name_first_kanji.trace_add('write',self.sync_mei)
		self.button_export["command"] = lambda: self.export_excel()
		self.button_shodo["command"] = lambda: ShodoSettingSubFrame.show_setting(self.master, self.shodo)

	def sync_shi(self, *args):
		"""
		名前更新イベント
		"""
		var_out = self.frame_personal.data.name_last_kanji.get()
		self.frame_skill.data.last_name_kanji = var_out
		self.frame_history.data.last_name_kanji = var_out

	def sync_mei(self, *args):
		"""
		名前更新イベント
		"""
		var_out = self.frame_personal.data.name_first_kanji.get()
		self.frame_skill.data.first_name_kanji = var_out
		self.frame_history.data.first_name_kanji = var_out

	def export_excel(self):
		"""
  	EXCEL書き出し：現在の登録内容でExcelファイルを書き出す。

		"""
		out = ExcelOutput(self.frame_personal.data, self.frame_skill.data, self.frame_history.data)
		out.subframe_modeselect(self.master)
		del out

	def update_state(self):
		self.status_shodo["text"] = "有効" if self.shodo.is_active() else "無効"
		self.status_shodo["foreground"] = COLOR[STATUS_GREEN] if self.shodo.is_active() else COLOR[STATUS_RED]

if __name__ == "__main__":
	def upd():
		app.update_state()
		app.after(500, upd)
	root = tk.Tk()
	root.resizable(True,True)
	root.minsize(640, 480)
	app = Application(master = root)
	app.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=icon))
	upd()
	app.mainloop()