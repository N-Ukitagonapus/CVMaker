import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from fileio.ExcelOutput import ExcelOutput
from utils.Validation import DynamicValidation as dval
from frames.PersonalDataFrame import PersonalDataFrame
from frames.SkillDataFrame import SkillDataFrame
from frames.CareerHistoryFrame import CareerHistoryFrame
from utils.Utilities import Utilities as util, resource_path
from constants.message import DialogMessage as diag

VERSION = 1.00
class Application(tk.Frame):
	global icon
	def __init__(self, master = None):
		super().__init__(master)
  
		#ウィンドウ設定
		self.master.title("K.S.A.M")
		self.master.geometry("1200x900")

		self.create_widgets()

	def create_widgets(self):
		"""
		ウィジェット生成
		"""
		#タイトル設定
		self.frame_title = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.icon_zone = tk.Canvas(self.frame_title, bg="#deb887", height=50, width=50)
		self.icon_zone.pack(side=tk.LEFT,padx=10,pady=10)
		icon = Image.open(resource_path("ksam_icon.png"))
		icon = icon.resize((50,50))
		self.icon = ImageTk.PhotoImage(icon)
		self.icon_zone.create_image(27, 27, image=self.icon)
		#タイトル
		tk.Label(self.frame_title, text="Kushimsoft Skillsheet Automatic Maker", font=("Meiryo UI",20,"bold","italic")).pack(side=tk.LEFT,padx=10,pady=10)
		# バージョン
		tk.Label(self.frame_title, text="Version {0}".format(VERSION), font=("Meiryo UI",10,"italic")).pack(anchor=tk.NE,padx=5,pady=5)
		# 作者
		tk.Label(self.frame_title, text="Created by N.Ukita", font=("Meiryo UI",10,"italic")).pack(anchor=tk.SE,padx=5,pady=5)

		self.frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=10)

		#Exportボタン
		self.frame_bottombutton = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.button_export = ttk.Button(self.frame_bottombutton,width=15,text="Excel書出")
		self.button_export.pack(side=tk.RIGHT,padx=10,pady=5)
		self.frame_bottombutton.pack(side=tk.BOTTOM,fill=tk.X,padx=20,pady=10)

		self.frame_personal = PersonalDataFrame(self.master)
		self.frame_personal.pack()

		self.frame_skill = SkillDataFrame(self.master)
		self.frame_skill.pack()

		self.frame_history = CareerHistoryFrame(self.master)
		self.frame_history.pack()

		self.frame_personal.data.shain_num.trace('w',self.sync_shain_num)
		self.button_export["command"] = lambda: self.export_excel()

	def sync_shain_num(self, *args):
		"""
		社員番号更新イベント
		"""
		tgt = self.frame_personal.data.shain_num
		if args[0] == tgt._name:
			var = tgt.get()
			if dval.is_numeric(var,3):
				self.frame_skill.data.shain_num = var
				self.frame_history.data.shain_num = var


	def export_excel(self):
		"""
			EXCEL書き出し：現在の登録内容でExcelファイルを書き出す。
		"""
		out = ExcelOutput()
		try:
			out.export(self.frame_personal.data, self.frame_skill.data, self.frame_history.data)
			util.msgbox_showmsg(diag.DIALOG_SUCCESS_OUTPUT_EXCEL)
		except Exception as e:
			print(e)
			util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
		finally:
			del out

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(False,False)
	app = Application(master = root)
	app.mainloop()