# セッション変数の取得
from words import Words
from setting import session


class DbClient(object):

    def __init__(self):
        self.words = Words()

    def get_words(self):
        words = session.query(Words).all()
        return words
