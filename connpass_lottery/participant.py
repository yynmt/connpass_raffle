import csv
import logging

logger = logging.getLogger(__name__)


def load(csv_path=''):
    """
    connpassからダウンロードできるcsvファイルの読み込み
    """

    tmp_list = []

    # connpassからダウンロードできるcsvファイルはShift-JIS
    with open(csv_path, encoding='cp932') as f:
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
            # 更新日時
            tmp_part.update_time = row[7]
            # 受付番号
            tmp_part.rcpt_number = row[8]

            # 参加ステータスがキャンセルの参加者は除外
            if 'キャンセル' in tmp_part.status_part:
                continue

            # リストに参加者を追加
            tmp_list.append(tmp_part)

        return tmp_list


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
        # 更新日時
        self.update_time = ''
        # 受付番号
        self.rcpt_number = -1
