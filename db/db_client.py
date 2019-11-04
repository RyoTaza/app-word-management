# セッション変数の取得
from words import Words
from setting import session


class DbClient(object):

    def __init__(self):
        self.words = Words()

    def insert_word(self, tgt_word):
        word = Words()
        word.word = tgt_word
        session.add(word)
        session.commit()

    def get_words(self):
        words = session.query(Words).all()
        return words
