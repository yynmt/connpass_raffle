import csv
import logging

logger = logging.getLogger(__name__)


def load(part_csv_path, win_csv_path):
    """
    connpassからダウンロードできるcsvファイルの読み込み
    """

    tmp_part_list = []
    tmp_win_list = []

    # 当選者の読み込み
    with open(win_csv_path, encoding='cp932') as f:
        reader = csv.reader(f)

        # 1行ずつ読み込み
        for row in reader:
            tmp_part = Participant()

            # 参加枠
            tmp_part.frame_name = row[0]
            # ユーザー名
            tmp_part.user_name = row[1]
            # 表示名
            tmp_part.display_name = row[2]
            # 利用開始日
            tmp_part.start_date = row[3]
            # コメント
            tmp_part.comment = row[4]
            # 参加ステータス
            tmp_part.status_part = row[5]
            # 出欠ステータス
            tmp_part.status_att = row[6]
            # PayPal取引ID
            tmp_part.paypal_id = row[7]
            # 請求書ID
            tmp_part.invoice_id = row[8]
            # 更新日時
            tmp_part.update_time = row[9]
            # 受付番号
            tmp_part.rcpt_number = row[10]

            # リストに参加者を追加
            tmp_win_list.append(tmp_part)

    # connpassからダウンロードできるcsvファイルはShift-JIS
    with open(part_csv_path, encoding='cp932') as f:
        reader = csv.reader(f)
        # 1行目のヘッダーをスキップ
        next(reader)

        # 1行ずつ読み込み
        for row in reader:
            tmp_part = Participant()

            # 参加枠
            tmp_part.frame_name = row[0]
            # ユーザー名
            tmp_part.user_name = row[1]
            # 表示名
            tmp_part.display_name = row[2]
            # 利用開始日
            tmp_part.start_date = row[3]
            # コメント
            tmp_part.comment = row[4]
            # 参加ステータス
            tmp_part.status_part = row[5]
            # 出欠ステータス
            tmp_part.status_att = row[6]
            # PayPal取引ID
            tmp_part.paypal_id = row[7]
            # 請求書ID
            tmp_part.invoice_id = row[8]
            # 更新日時
            tmp_part.update_time = row[9]
            # 受付番号
            tmp_part.rcpt_number = row[10]

            # 更新日時,受付番号
            # 参加ステータスがキャンセルの参加者は除外
            if 'キャンセル' in tmp_part.status_part:
                continue

            # 当選者に含まれているため除外
            flag = False
            for tmp_win in tmp_win_list:
                if tmp_win.user_name == tmp_part.user_name:
                    flag = True
                    continue

            if flag:
                continue

            # リストに参加者を追加
            tmp_part_list.append(tmp_part)

        return tmp_part_list, tmp_win_list


def save(csv_path, part_list):
    # 当選者の読み込み
    with open(csv_path, 'w', encoding='cp932', newline='') as f:
        writer = csv.writer(f)
        rows = []
        for part in part_list:
            row = [
                part.frame_name,
                part.user_name,
                part.display_name,
                part.start_date,
                part.comment,
                part.status_part,
                part.status_att,
                part.paypal_id,
                part.invoice_id,
                part.update_time,
                str(part.rcpt_number)
            ]
            rows.append(row)

        print(rows)
        writer.writerows(rows)


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
