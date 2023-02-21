import os
import re
import random
import datetime
import logging
import logging.config
from pathlib import Path
from flask import Flask, render_template, request

import participant

LOG_FILE_NAME = '{}.log'.format(datetime.date.today().strftime('%Y%m%d'))
LOG_FILE_PATH = str(Path('./log') / LOG_FILE_NAME)
os.makedirs(Path(LOG_FILE_PATH).parent, exist_ok=True)

app = Flask(__name__)
participant_list = []
winner_list = []
logger = logging.getLogger(__name__)

part_csv_path = r'./data.csv'
win_csv_path = re.sub(r'\..+$', '_win.csv', str((Path(part_csv_path).absolute())))
Path(win_csv_path).touch(exist_ok=True)


def setup_logger():
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'consoleHnadler',
                    'logFileHnadler',
                ]
            },
            'handlers': {
                'consoleHnadler': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'consoleFormatter',
                    'stream': 'ext://sys.stdout'
                },
                'logFileHnadler': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'formatter': 'logFileFormatter',
                    'filename': LOG_FILE_PATH,
                    'mode': 'a',
                    'encoding': 'utf-8'
                }
            },
            'formatters': {
                'consoleFormatter': {
                    'format': '[%(levelname)-8s]%(funcName)s -%(message)s'
                },
                'logFileFormatter': {
                    'format': '%(asctime)s|%(levelname)-8s|%(name)s|%(funcName)s|%(message)s'
                }
            }

        }
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/participant_list')
def participant_list():
    part_list = []
    for part in participant_list:
        part_list.append([
            part.user_name,
            part.display_name,
            part.rcpt_number
        ])

    sum = len(participant_list)
    return render_template('participant_list.html', part_list=part_list, sum=sum)


@app.route('/winner_list')
def winner_list():
    part_list = []
    for part in winner_list:
        part_list.append([
            part.user_name,
            part.display_name,
            part.rcpt_number
        ])
    sum = len(winner_list)
    return render_template('winner_list.html', part_list=part_list, sum=sum)


@app.route('/lottery', methods=['GET', 'POST'])
def lottery():
    if request.method == 'POST':
        try:
            if len(participant_list) == 0:
                # リストが空の場合
                return render_template('index.html')

            # 参加者リストからランダムに選ぶ
            idx = random.randrange(0, len(participant_list))
            # 当選者をリストからpop
            part = participant_list.pop(idx)

            winner_list.append(part)
            participant.save(win_csv_path, winner_list)

            # ユーザー表示名
            name = part.display_name
            # 受付番号
            num = part.rcpt_number
            # 抽選対象の参加者全員のユーザー表示名
            all_part_name_list = [p.display_name for p in participant_list]
            logger.debug('{}: {}'.format(num, name))

            return render_template('index.html', number=num, name=name, all_part_name_list=all_part_name_list)
        except ValueError:
            return render_template('error.html')
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # ロガー設定
    setup_logger()
    # 参加者csv読み込み
    participant_list, winner_list = participant.load(part_csv_path, win_csv_path)

    app.run()
    # app.run(port=80, debug=False)

# ToDo
# 当選してpopされたユーザを別のcsvに書き出す
