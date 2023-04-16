from datetime import date
import re
from constants.const import VALID_ERR, VALID_OK
from constants.message import Message as msg
class DynamicValidation:
	
  #入力がn文字以内かどうか
	def length_limit(input, ketasu):
		return len(input) <= int(ketasu)
  
  #入力が数字n桁以内かどうか
	def is_numeric(input, ketasu):
		return re.fullmatch("[0-9]*", input) and len(input) <= int(ketasu)
	
  #入力が英字n桁以内かどうか
	def validate_romaji(input, ketasu):
		return re.fullmatch("[a-zA-Z]*", input) and len(input) <= int(ketasu)
	

class StaticValidation:
	def is_not_empty(dict, *input):
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if read == "" or re.fullmatch("\s*", read):
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_EMPTY
				break

	def regex_match(dict, input, regex, msg_param):
		if re.fullmatch(regex, input):
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
		else:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)

	def date_check(dict, input):
		if input > date.today():
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_DAY_AFTER
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK