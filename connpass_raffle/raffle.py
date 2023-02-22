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
        winner = self.__participant_list.pop(idx)
        print(self.__winner_list)
        self.__winner_list.append(winner)
        print(self.__winner_list)
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

            writer.writerows(rows)
