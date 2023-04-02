import re

class Validation:
  #入力が数字n桁以内かどうか
	def is_numeric(input, ketasu):
		return re.fullmatch("[0-9]*", input) and len(input) <= int(ketasu)
	
  #入力が英字n桁以内かどうか
	def validate_romaji(input, ketasu):
		return re.fullmatch("[A-Z][a-z]*", input) and len(input) <= int(ketasu)