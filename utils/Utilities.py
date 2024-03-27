import base64
import calendar
from datetime import datetime, date
import os
import sys
import editdistance as ed
from monthdelta import monthmod 
import tkinter as tk
from tkinter import StringVar, messagebox as msgbox
from tkcalendar import DateEntry
from constants.const import VALID_ERR

from constants.message import DialogMessage
from data_structure.ShodoSetting import ShodoSetting
from utils.ShodoApiUtil import ShodoApi

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
  
class Utilities:
	"""
	ユーティリティクラス
	"""
 
	@staticmethod
	def setstr_from_read(tgt:StringVar, input:dict):
		"""
		読込結果を入力欄に設定
		Args:
				tgt (StringVar): 設定対象
				input (dict): 読込内容
		"""
		if input["result"] != VALID_ERR:
			tgt.set(input["value"])

	@staticmethod
	def setstr_from_read_cut(tgt:StringVar, input:dict, maxlength:int):
		"""
		読込結果を入力欄に設定(最大文字数超過分カット)
		Args:
				tgt (StringVar): 設定対象
				input (dict): 読込内容
    		maxlength (int): 最大文字数 
		"""
		if input["result"] != VALID_ERR:
			tgt.set(input["value"][:maxlength])
   
	@staticmethod
	def setdate_from_read(tgtentry:DateEntry, input:dict):
		"""
		読込結果を日付入力欄に設定
		Args:
				tgtentry (DateEntry): 設定対象
				input (dict): 読込内容
		"""
		if input["result"] != VALID_ERR:
			entered_date = datetime.strptime(input["value"],"%Y%m%d")
			tgtentry.set_date(entered_date)

	@staticmethod
	def int_from_str(input:str) -> int:
		"""
		文字列⇒数値変換
		Args:
				input (str): 文字列

		Returns:
				int: 変換後数値(読み取り失敗時は0)
		"""
		try:
			return int(input)
		except ValueError:
			return 0
 
	@staticmethod
	def get_years_sub(dt_from:date, dt_to:date) -> tuple:
		"""
		2日付間の差分(年、月)を取得
		Args:
				dt_from (date): 開始年月日
				dt_to (date): 終了年月日

		Returns:
				tuple: 差分(年、月)
		"""
		monthdelta = monthmod(dt_from,dt_to)
		return monthdelta[0].months // 12, monthdelta[0].months % 12


	@staticmethod
	def get_first_date(dt):
		"""
	  年月の初日を取得
		Args:
				dt (date): 入力日

		Returns:
				date : 入力年月の初日
		"""
		return date(dt.year, dt.month, 1)
	
	@staticmethod
	def get_last_date(dt): 
   
		"""
	  年月の最終日を取得
		Args:
				dt (date): 入力日

		Returns:
				date : 入力年月の最終日
		"""
		return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

	@staticmethod
	def tidy_list(input: list):
		"""
		リスト整頓
		Args:
				input (list): 整頓前リスト

		Returns:
				list: 整頓後リスト(空白除去、重複削除)
		"""
		return list(set([s for s in input if s != '']))

	@staticmethod
	def mark_required(tgt,lbl):
		"""
		必須マーク付与

		Args:
				tgt (Any): 対象フレーム
				lbl (Any): マーク付与対象
		"""
		tk.Label(tgt, text="(必須)", font=("Meiryo UI",6,"bold"), foreground='red').pack(side=tk.LEFT, after=lbl)


	@staticmethod
	def get_dateclass(input) -> datetime.date:
		"""
		date変換
		Args:
				input (Any): 日付(datetimeないしdateクラス)

		Returns:
				datetime.date: 変換後日付(dateクラス)
		"""
		if type(input) == datetime:
			return input.date()
		else:
			return input

	@staticmethod
	def encode_key(input:str):
		"""
		キーをエンコード

		Args:
				input (str): エンコード元

		Returns:
				str: エンコード結果
		"""
		return base64.b64encode(input.encode()).decode() if input is not None else ""

	@staticmethod
	def decode_key(input:str):
		"""
		キーをデコード

		Args:
				input (str): デコード元

		Returns:
				str: デコード結果
		"""
		return base64.b64decode(input).decode() if input is not None else ""

	@staticmethod
	def check_valiant(words) -> dict:
		"""
  	リスト表記ゆれチェック

		Args:
				words (list): チェック対象 
		Returns:
				dict: チェック結果
		"""
  
		def geteval(str1, str2) -> tuple:
			num = ed.eval(str1, str2) / len(str1)
			return(num, num <= 0.25)

		def add_alert(result:dict, num1:str, num2:str):
			for key in result.keys():
				if num1 in result[key] and num2 in result[key]:
					return
			if num1 not in result.keys():
				result[num1] = []
			result[num1].append(num2)

		ret = {}
		h = 1
		words.sort()
		for i in range(len(words)):
			for j in range(h,len(words)):
				ruiji = geteval(words[i],words[j])
				if ruiji[1]:
					add_alert(ret, words[i], words[j])
				print("{0} || {1} : {2} [{3}]".format(words[i],words[j],ruiji[0],"！" if ruiji[1] else "　"))
			h += 1

		return ret

	@staticmethod
	def parse_shodo_response(response:list) -> list:
		ret = []
		for siteki in response :
			if siteki["operation"] is None:
				ret.append("・{0}行目/{1}文字目：{2}".format((siteki["from"]["line"])+1, (siteki["from"]["ch"])+1, siteki["message"]))
			else :
				ret.append("・{0}行目/{1}文字目：{2} ({3} ⇒ {4})".format((siteki["from"]["line"])+1, (siteki["from"]["ch"])+1, siteki["message"], siteki["before"], siteki["after"]))
		return ret

	#汎用メッセージ表示
	@staticmethod
	def msgbox_showmsg(param: DialogMessage):
		"""
  	汎用メッセージ表示
		Args:
				param (DialogMessage): 表示メッセージ(タイトル、内容)
		"""
		if param[0] == "info" :
			msgbox.showinfo(title=param[1], message=param[2])
		elif param[0] == "warn" :
			msgbox.showwarning(title=param[1], message=param[2])
		elif param[0] == "error" :
			msgbox.showerror(title=param[1], message=param[2])
		else:
			msgbox.showerror(title="BIG BONER DOWN THE LANE", message="This is an error message supposed NOT to be shown.")

	#汎用クエスチョンダイアログ
	@staticmethod
	def msgbox_ask(param: DialogMessage):
		"""
  	汎用確認ダイアログ
		Args:
				param (DialogMessage): 表示メッセージ(タイトル、内容)
		"""
		return msgbox.askyesno(title=param[1], message=param[2])