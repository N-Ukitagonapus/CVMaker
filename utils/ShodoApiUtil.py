import time
import requests,json
from datetime import datetime as dt

from data_structure.ShodoPreference import ShodoPreference

URL = {
  "usage":"https://api.shodo.ink/@{0}/{1}/usage/",
	"request":"https://api.shodo.ink/@{0}/{1}/lint/",
  "result":"https://api.shodo.ink/@{0}/{1}/lint/{2}/"
}
STATUS_OK = 200

class ShodoApi:
  @staticmethod
  def check_availablity(pref:ShodoPreference):
    response = requests.get(URL["usage"].format(pref.user_id, pref.project_name), headers=ShodoApi.__get_header(pref.token))
    if response.status_code == STATUS_OK:
      limit = int(json.loads(response.text)["monthly_amount"])
      for usage_list in json.loads(response.text)["usage"]:
        if usage_list["year"] == dt.now().year and usage_list["month"] == dt.now().month: 
          usage = usage_list["amount"]
          ret = usage <= limit
          print("本年月度利用状況\n現在の利用文字数：{0}\n制限文字数：{1}\n結果：{2}".format(usage, limit, "OK" if ret else "NG"))
          pref.flg_able = ret
          return
      print("本年月度の利用状況が見つかりません。")
      pref.flg_able = False
    else:
      print("[ERROR] ShodoApiで問題が発生しました。エラーコード:{0}".format(response.status_code))
      pref.flg_able = False
  @staticmethod
  def lint_request(pref, *text):
    if len(text) == 0:
      raise ShodoApiError("入力パラメータがありません。処理を中止します。")
    elif len(text) == 1:
      lint_id = ShodoApi.__lint_request_single(pref, text)
    else:
      texts = []
      for input in text:
        texts.append(input)
      lint_id = ShodoApi.__lint_request_multi(pref, texts)

    return ShodoApi.__get_result(lint_id)
  
  @staticmethod
  def __lint_request_single(pref:ShodoPreference, text) -> int:
    response = requests.post(URL["request"].format(pref.user_id, pref.project_name), json={"body": text}, headers=ShodoApi.__get_header(pref.token))
    if response.status_code == STATUS_OK:
      return json.loads(response.text)["lint_id"]
    else:
      raise ShodoApiRequestError(response.status_code)
    
  @staticmethod
  def __lint_request_multi(pref:ShodoPreference, texts:list) -> int:
    response = requests.post(URL["request"].format(pref.user_id, pref.project_name), json={"bulk_body": texts}, headers=ShodoApi.__get_header(pref.token))
    if response.status_code == STATUS_OK:
      return json.loads(response.text)["lint_id"]
    else:
      raise ShodoApiRequestError(response.status_code)
    
  @staticmethod
  def __get_result(pref:ShodoPreference, lint_id):
    for i in range(1,10):
      response = requests.get(URL["result"].format(pref.user_id, pref.project_name, lint_id), headers=ShodoApi.__get_header(pref.token))
      if response.status_code == STATUS_OK:
        texts = json.loads(response.text)
        if texts["status"] == "done":
          return texts
      else:
        raise ShodoApiRequestError(response.status_code)
      time.sleep(1)
    raise ShodoApiError("試行回数内にチェックが完了しませんでした。")
  
  @staticmethod
  def __get_header(token):
      headers = {}
      headers["Authorization"] = "Bearer {0}".format(token)
      return headers

class ShodoApiError(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self) -> str:
    return "[ERROR] ShodoApiで問題が発生しました。:{0}".format(self.message)

class ShodoApiRequestError(Exception):
  def __init__(self, status_code):
    self.status_code = status_code
  def __str__(self) -> str:
    return "[ERROR] ShodoApiで問題が発生しました。エラーコード:{0}".format(self.status_code)