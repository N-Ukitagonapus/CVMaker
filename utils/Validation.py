from datetime import date, datetime
import re
from constants.const import VALID_ERR, VALID_OK, VALID_WARN
from constants.message import Message as msg
class DynamicValidation:
	
  #入力がn文字以内かどうか
	def length_limit(input, ketasu):
		return len(input) <= int(ketasu)
  
  #入力が数字n桁以内かどうか
	def is_numeric(input, ketasu):
		return (re.fullmatch("[0-9]*", input) != None) and len(input) <= int(ketasu)
	
  #入力が英字n桁以内かどうか
	def validate_romaji(input, ketasu):
		return (re.fullmatch("[a-zA-Z]*", input) != None) and len(input) <= int(ketasu)
	

class StaticValidation:
	def out_is_not_empty(dict, *input):
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if read == "" or re.fullmatch("\s*", read):
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_EMPTY
				break

	def out_regex_match(dict, regex, msg_param, *input):
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_OK
		for read in input:
			if re.fullmatch(regex, read) is None:
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_INVALID.format(msg_param)
				break

	def out_date_check(dict, input):
		if input > date.today():
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_DAY_AFTER
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK

	def in_is_not_empty(dict):
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_EMPTY
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
   
	def in_regex_match(dict, regex, msg_param):
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_EMPTY
		elif re.fullmatch(regex, dict["value"]):
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
		else:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)

	def in_regex_and_length(dict, maxlength, regex, msg_param):
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_EMPTY
		elif re.fullmatch(regex, dict["value"]) is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_INVALID.format(msg_param)
		elif len(dict["value"]) > maxlength:
			dict["result"] = VALID_WARN
			dict["msg"] = msg.MSG_WARN_LENGTH.format(maxlength)
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK

	def in_maxlength_check(dict, maxlength):
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_EMPTY
		elif len(dict["value"]) > maxlength:
			dict["result"] = VALID_WARN
			dict["msg"] = msg.MSG_WARN_LENGTH.format(maxlength)
		else:
			dict["result"] = VALID_OK
			dict["msg"] = msg.MSG_OK
  
	def in_date_check(dict):
		if dict["value"] is None:
			dict["result"] = VALID_ERR
			dict["msg"] = msg.MSG_EMPTY   
		else:
			try:
				entered = datetime.strptime(dict["value"],"%Y%m%d").date() 
				dict["result"] = VALID_ERR if entered > date.today() else VALID_OK
				dict["msg"] = msg.MSG_DAY_AFTER if entered > date.today() else msg.MSG_OK
			except Exception as e:
				print(e)
				dict["result"] = VALID_ERR
				dict["msg"] = msg.MSG_DATEFORMAT_FAILURE

	def in_number_between(dict,min,max,msg_param):
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
   
	def in_novalidation(dict):
		dict["result"] = VALID_OK
		dict["msg"] = msg.MSG_NOVALIDATION   