import logging
from flask import Flask, render_template, request

from raffle import Raffle

CSV_PATH = r'./data.csv'

logger = logging.getLogger(__name__)
app = Flask(__name__)
raffle = Raffle(CSV_PATH)


class Core:
    def __init__(self):
        pass

    @staticmethod
    def run():
        app.run()
        # app.run(port=80, debug=False)

    @staticmethod
    @app.route('/')
    def index():
        return render_template('index.html')

    @staticmethod
    @app.route('/participant_list')
    def participant_list():
        part_list = []
        for part in raffle.participant_list:
            part_list.append([
                part.user_name,
                part.display_name,
                part.rcpt_number
            ])

        sum_part = len(raffle.participant_list)
        return render_template('participant_list.html', part_list=part_list, sum=sum_part)

    @staticmethod
    @app.route('/winner_list')
    def winner_list():
        part_list = []
        for part in raffle.winner_list:
            part_list.append([
                part.user_name,
                part.display_name,
                part.rcpt_number
            ])
        sum_part = len(raffle.winner_list)
        return render_template('winner_list.html', part_list=part_list, sum=sum_part)

    @staticmethod
    @app.route('/raffle', methods=['GET', 'POST'])
    def raffle():
        if request.method == 'POST':
            try:
                if len(raffle.participant_list) == 0:
                    # リストが空の場合
                    return render_template('index.html')

                winner = raffle.pick()

                # ユーザー表示名
                name = winner.display_name
                # 受付番号
                num = winner.rcpt_number
                # 抽選対象の参加者全員のユーザー表示名
                all_part_name_list = [p.display_name for p in raffle.participant_list]
                logger.debug('{}: {}'.format(num, name))

                return render_template('index.html', number=num, name=name, all_part_name_list=all_part_name_list)
            except ValueError:
                return render_template('error.html')
        elif request.method == 'GET':
            return render_template('index.html')
        else:
            return render_template('index.html')
