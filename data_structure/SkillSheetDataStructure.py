'''
データ基本構造
'''
from data_structure.CareerHistoryData import CareerHistoryData
from data_structure.PersonalData import PersonalData
from data_structure.SkillData import SkillData

class SkillSheetDataStructure:
  def __init__(self):
    self.personal_data = PersonalData()
    self.create_year = 2000
    self.create_month = 1
    self.skill_data = SkillData()
    self.career_history_datas = []
    self.career_history_datas.append(CareerHistoryData())