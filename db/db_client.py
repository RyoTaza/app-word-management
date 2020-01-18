# セッション変数の取得
from db.words import Words
from db.setting import session


class DbClient(object):

    def __init__(self):
        self.words = Words()

    def insert_word(self, tgt_word, word_meaning):
        try:
            word = Words()
            word.word = tgt_word
            word.japanese = word_meaning
            session.add(word)
            session.commit()
        except Exception:
            session.rollback()
            raise Exception()
        finally:
            session.close()

    def get_all_words(self):
        try:
            words = session.query(Words).all()
            return words
        except Exception:
            session.rollback()
            raise Exception()
        finally:
            session.close()
