
class Message:
	MSG_OK = "OK."
	MSG_EMPTY = "NG：未入力です。"
	MSG_INVALID = "NG：{0}で入力してください。"
	MSG_DAY_AFTER = "NG：本日より未来の日付は入力できません。"
	MSG_DATEFORMAT_FAILURE= "NG：日付変換に失敗しました。"
	MSG_WARN_LENGTH= "WARN：最大文字数({0}文字)を超えている部位は切り取られます。"

class DialogMessage:
	DIALOG_TEST = ("info","TEST","【メッセージ未実装】\nこれはテストメッセージです。")
	DIALOG_OUTPUT_ERROR = ("error","出力失敗","ファイル出力に失敗しました。\n詳細はコンソールログを参照してください。")
	DIALOG_INPUT_ERROR = ("error","読込失敗","ファイル読込に失敗しました。\n詳細はコンソールログを参照してください。")
	DIALOG_ASK_FORCE_OUTPUT= ("yesno","強制出力","入力項目にエラーがありますが、強制的に出力してもよろしいですか？")