import logging

logger = logging.getLogger(__name__)


class Participant:
    def __init__(self):
        # 参加枠
        self.frame_name = ''
        # ユーザー名
        self.user_name = ''
        # 表示名
        self.display_name = ''
        # 利用開始日
        self.start_date = ''
        # コメント
        self.comment = ''
        # 参加ステータス
        self.status_part = ''
        # 出欠ステータス
        self.status_att = ''
        # PayPal取引ID
        self.paypal_id = ''
        # 請求書ID
        self.invoice_id = ''
        # 更新日時
        self.update_time = ''
        # 受付番号
        self.rcpt_number = -1

    def from_cvs_row(self, row):
        # 参加枠
        self.frame_name = row[0]
        # ユーザー名
        self.user_name = row[1]
        # 表示名
        self.display_name = row[2]
        # 利用開始日
        self.start_date = row[3]
        # コメント
        self.comment = row[4]
        # 参加ステータス
        self.status_part = row[5]
        # 出欠ステータス
        self.status_att = row[6]
        # PayPal取引ID
        self.paypal_id = row[7]
        # 請求書ID
        self.invoice_id = row[8]
        # 更新日時
        self.update_time = row[9]
        # 受付番号
        self.rcpt_number = row[10]

    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return self.user_name == other.user_name

    def __ne__(self, other):
        return not self.__eq__(other)
