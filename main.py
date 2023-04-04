import tkinter as tk
from tkinter import ttk
from frames.PersonalDataFrame import PersonalDataFrame
from frames.SkillDataFrame import SkillDataFrame
from frames.CareerHistoryFrame import CareerHistoryFrame

class Application(tk.Frame):

	def __init__(self, master = None):
		super().__init__(master)
  
		#ウィンドウ設定
		self.master.title("スキルシート生成ソフト")
		self.master.geometry("1200x900")

		#タイトル設定
		self.frame_title = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.label_title = tk.Label(self.frame_title, text="スキルシート生成ソフト", font=("Meiryo UI",20,"bold","italic"))
		self.label_title.pack(side=tk.TOP,padx=10,pady=10)
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

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(False,False)
	app = Application(master = root)
	app.mainloop()