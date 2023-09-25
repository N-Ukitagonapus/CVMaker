from datetime import date, datetime
import re
from constants.const import VALID_ERR, VALID_OK, VALID_WARN
from constants.message import Message as msg
class DynamicValidation:
	"""
	動的入力チェック
	"""
	@staticmethod
	def length_limit(input, ketasu):
		"""
		文字数チェック
		Args:
				input (Any): 入力値
				ketasu (int): 最大桁数

		Returns:
				bool: 桁数以内であればTrue
		"""
		return len(input) <= int(ketasu)
  
	@staticmethod
	def is_numeric(input, ketasu):
		"""
		数字チェック
		Args:
				input (Any): 入力値
				ketasu (int): 最大桁数

		Returns:
				bool: 全て数時かつ桁数以内であればTrue
		"""
		return (re.fullmatch("[0-9]*", input) != None) and len(input) <= int(ketasu)
	
	@staticmethod
	def validate_romaji(input, ketasu):
		"""
		英字チェック
		Args:
				input (Any): 入力値
				ketasu (int): 最大桁数

		Returns:
				bool: 全て英字かつ桁数以内であればTrue
		"""
		return (re.fullmatch("[a-zA-Z]*", input) != None) and len(input) <= int(ketasu)
	

class StaticValidation:
	"""
	静的入力チェック
	"""
	@staticmethod
	def out_is_not_empty(dict, *input):
		"""
		未入力チェック(エラー)

		Args:
				dict (dict): チェック結果格納用
				*input (any): 入力値
		"""
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if read == "" or re.fullmatch("(\s|\n)*", read):
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_ERR_EMPTY
				break

	@staticmethod
	def out_warn_if_empty(dict, *input):
		"""
		未入力チェック(警告)

		Args:
				dict (dict): チェック結果格納用
				*input (any): 入力値
		"""
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if read == "" or re.fullmatch("(\s|\n)*", read):
				dict["result"] = VALID_WARN
				dict["msg"] = msg.MSG_WARN_EMPTY
				break

	@staticmethod
	def out_regex_match(dict, regex, msg_param, *input):
		"""
		正規表現チェック

		Args:
				dict (dict): チェック結果格納用
				regex (str): 正規表現
				msg_param (str): メッセージパラメータ
				*input (any): 入力値
		"""
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if re.fullmatch(regex, read) is None:
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_INVALID.format(msg_param)
				break

	@staticmethod
	def out_date_check(dict, input):
		"""
		現在日付超過チェック

		Args:
				dict (dict): チェック結果格納用
				*input (any): 入力値
		"""
		if input > date.today():
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_DAY_AFTER
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK

	@staticmethod
	def in_is_not_empty(dict):
		"""
		読込値未入力チェック(エラー)

		Args:
				dict (dict): 入力値チェック結果格納用
		"""
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_ERR_EMPTY
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
   
	@staticmethod
	def in_regex_match(dict, regex, msg_param):
		"""
		読込値正規表現チェック

		Args:
				dict (dict): 入力値チェック結果格納用
				regex (str): 正規表現
				msg_param (str): メッセージパラメータ
		"""
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_ERR_EMPTY
		elif re.fullmatch(regex, dict["value"]):
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
		else:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)

	@staticmethod
	def in_regex_and_length(dict, maxlength, regex, msg_param):
		"""
		読込値正規表現チェック(文字数制限付き)

		Args:
				dict (dict): 入力値チェック結果格納用
				maxlength (int): 最大文字数
				regex (str): 正規表現
				msg_param (str): メッセージパラメータ
		"""
		
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_ERR_EMPTY
		elif re.fullmatch(regex, dict["value"]) is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)
		elif len(dict["value"]) > maxlength:
			dict["result"] = VALID_WARN
			dict["msg"] = msg.MSG_WARN_LENGTH.format(maxlength)
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK

	@staticmethod
	def in_maxlength_check(dict, maxlength):
		"""
		読込値文字数チェック

		Args:
				dict (dict): 入力値チェック結果格納用
				maxlength (int): 最大文字数
		"""
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_ERR_EMPTY
		elif len(dict["value"]) > maxlength:
			dict["result"] = VALID_WARN
			dict["msg"] = msg.MSG_WARN_LENGTH.format(maxlength)
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
  
	@staticmethod
	def in_date_check(dict):
		"""
		読込値日付チェック

		Args:
				dict (dict): 入力値チェック結果格納用

		"""
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_ERR_EMPTY   
		else:
			try:
				entered = datetime.strptime(dict["value"],"%Y%m%d").date() 
				dict["result"] = VALID_ERR if entered > date.today() else VALID_OK
				dict["msg"] = msg.MSG_DAY_AFTER if entered > date.today() else msg.MSG_OK
			except Exception as e:
				print(e)
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_DATEFORMAT_FAILURE

	@staticmethod
	def in_number_between(dict,min,max,msg_param):
		"""
  	読込値数値チェック(最小値・最大値)
		Args:
				dict (dict): 入力値チェック結果格納用
				min (int): 最小値
				max (int): 最大値
				msg_param (str): メッセージパラメータ
		"""
		try:
			if int(dict["value"]) >= min and int(dict["value"]) <= max:
				dict["result"] = VALID_OK
				dict["msg"] = msg.MSG_OK
			else:
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_INVALID.format(msg_param)
		except Exception as e:
			print(e)
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)
   
	@staticmethod
	def io_novalidation(dict):
		"""
  	読込値判定なし
		Args:
				dict (dict): 入力値チェック結果格納用
		"""
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_NOVALIDATION   