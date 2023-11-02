import logging

logger = logging.getLogger(__name__)


class Item:
    def __init__(self):
        # 管理ID
        self.id = ''
        # 提供元
        self.provider = ''
        # 品名
        self.name = ''
