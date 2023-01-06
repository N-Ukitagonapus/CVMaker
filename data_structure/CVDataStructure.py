'''
データ基本構造
'''
from data_structure.PersonalData import PersonalData
from data_structure.SkillData import SkillData

class CVDataStructure:
  def __init__(self):
    self.__full_name = ""
    self.__date = ""
    self.__personal_data = PersonalData()
    self.__skill_data = SkillData()
    self.__career_history_datas = []