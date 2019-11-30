# セッション変数の取得
from db.words import Words
from db.setting import session


class DbClient(object):

    def __init__(self):
        self.words = Words()

    def insert_word(self, tgt_word, word_meaning):
        word = Words()
        word.word = tgt_word
        word.japanese = word_meaning
        session.add(word)
        session.commit()

    def get_all_words(self):
        words = session.query(Words).all()
        return words
