import logging
from itertools import zip_longest
from flask import Flask, render_template, request, redirect

from raffle import Raffle

PART_CSV_PATH = r'./part.csv'
ITEM_CSV_PATH = r'./item.csv'

logger = logging.getLogger(__name__)
app = Flask(__name__)
raffle = Raffle(PART_CSV_PATH, ITEM_CSV_PATH)


class Core:
    def __init__(self):
        pass

    @staticmethod
    def run():
        app.run(debug=False, host='0.0.0.0', port=5000)
        # app.run(debug=True, host='0.0.0.0', port=5000)
        # app.run(debug=False, host='0.0.0.0', port=80)   # 実行時要root権限

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
    @app.route('/winner_list/<user_name>')
    def remove_winnner(user_name):
        raffle.remove_winner(user_name)
        return redirect('/winner_list')

    @staticmethod
    @app.route('/winner_list')
    def winner_list():
        winner_list = []
        for winner, item in zip_longest(raffle.winner_list, raffle.item_list):
            row = []
            if item is not None:
                row.extend([
                    item.provider,
                    item.name,
                ])
            else:
                row.extend(['-', '-'])

            if winner is not None:
                row.extend([
                    winner.user_name,
                    winner.display_name,
                    winner.rcpt_number,
                ])
            else:
                row.extend(['-', '-', '-'])

            winner_list.append(row)
        sum_part = len(raffle.winner_list)
        return render_template('winner_list.html', part_list=winner_list, sum=sum_part)

    @staticmethod
    @app.route('/raffle', methods=['GET', 'POST'])
    def raffle():
        if request.method == 'POST':
            try:
                if len(raffle.participant_list) == 0:
                    # リストが空の場合
                    return render_template('index.html')

                winner = raffle.pick()

                # ユーザーID
                id = winner.user_name
                # ユーザー表示名
                name = winner.display_name
                # 受付番号
                num = winner.rcpt_number
                # 抽選対象の参加者全員のユーザー表示名
                all_part_name_list = [p.display_name for p in raffle.participant_list]
                # 抽選対象の景品名
                item_idx = len(raffle.winner_list) - 1
                print(item_idx)
                if item_idx < len(raffle.item_list):
                    provider = raffle.item_list[item_idx].provider
                    item = raffle.item_list[item_idx].name
                else:
                    provider = ''
                    item = ''
                logger.debug('{}({}) -> {}({}):{}'.format(item, provider, name, id, num))

                return render_template(
                    'index.html',
                    number=num,
                    id=id,
                    name=name,
                    all_part_name_list=all_part_name_list,
                    item=item,
                    provider=provider
                )
            except ValueError:
                return render_template('error.html')
        elif request.method == 'GET':
            return render_template('index.html')
        else:
            return render_template('index.html')

    @staticmethod
    @app.route('/rm/<user_name>')
    def remove_last_winner(user_name):
        raffle.remove_winner(user_name)
        return redirect('/')
