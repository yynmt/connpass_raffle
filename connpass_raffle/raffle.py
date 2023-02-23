import csv
import random
import re
import logging
from pathlib import Path
from participant import Participant

logger = logging.getLogger(__name__)


class Raffle:
    def __init__(self, csv_path):
        # 参加者一覧のリスト
        self.__participant_list = []
        # 当選者のリスト
        self.__winner_list = []
        # connpassから取得できるCSVファイルのパス
        self.__csv_path = csv_path
        # 当選者を保存するCSVファイルのパス
        self.__winner_csv_path = re.sub(r'\..+$', '_win.csv', str((Path(self.__csv_path).absolute())))

        # 各CSVファイルのロード
        self.__load()

    @property
    def participant_list(self):
        return self.__participant_list

    @property
    def winner_list(self):
        return self.__winner_list

    def __load(self):
        self.__participant_list = []
        self.__winner_list = []

        logger.debug('Load: {}'.format(self.__winner_csv_path))
        # 当選者の読み込み
        with open(self.__winner_csv_path, encoding='cp932') as f:
            reader = csv.reader(f)

            # 1行ずつ読み込み
            for row in reader:
                tmp_part = Participant()
                tmp_part.from_cvs_row(row)

                # リストに参加者を追加
                self.__winner_list.append(tmp_part)

        logger.debug('Load: {}'.format(self.__csv_path))
        # 参加者の読み込み
        # connpassからダウンロードできるcsvファイルはShift-JIS
        with open(self.__csv_path, encoding='cp932') as f:
            reader = csv.reader(f)
            # 1行目のヘッダーをスキップ
            next(reader)

            # 1行ずつ読み込み
            for row in reader:
                tmp_part = Participant()
                tmp_part.from_cvs_row(row)

                # 参加ステータスがキャンセルの参加者は除外
                if 'キャンセル' in tmp_part.status_part:
                    continue

                # 当選者に含まれているため除外
                flag = False
                for tmp_win in self.__winner_list:
                    if tmp_win.user_name == tmp_part.user_name:
                        flag = True
                        continue
                if flag:
                    continue

                # リストに参加者を追加
                self.__participant_list.append(tmp_part)

    def pick(self):
        # 参加者リストからランダムに選ぶ
        idx = random.randrange(0, len(self.__participant_list))
        # 参加者リストから当選者をpopして削除
        winner = self.__participant_list.pop(idx)
        # popした当選者リストに追加
        self.__winner_list.append(winner)
        # 当選者リストの保存
        self.__save()

        return winner

    def __save(self):
        logger.debug('Save: {}'.format(self.__winner_csv_path))
        # 当選者の保存
        with open(self.__winner_csv_path, 'w', encoding='cp932', newline='') as f:
            writer = csv.writer(f)
            rows = []
            for part in self.__winner_list:
                row = [
                    part.frame_name,        # 参加枠
                    part.user_name,         # ユーザー名
                    part.display_name,      # 表示名
                    part.start_date,        # 利用開始日
                    part.comment,           # コメント
                    part.status_part,       # 参加ステータス
                    part.status_att,        # 出欠ステータス
                    part.paypal_id,         # PayPal取引ID
                    part.invoice_id,        # 請求書ID
                    part.update_time,       # 更新日時
                    str(part.rcpt_number)   # 受付番号
                ]
                rows.append(row)

            writer.writerows(rows)
