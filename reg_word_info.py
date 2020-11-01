import sys
import requests
from bs4 import BeautifulSoup
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/db')
from db.db_client import DbClient
import csv
import configparser
import time


class RegWordInfo(object):
    """
    引数の英単語をDBに格納し、CSVファイルに追記する
    記載されていたら、新しいファイルを作成する
    """

    def __init__(self):

        # Read config file
        self.config_init = configparser.ConfigParser()
        self.config_init.read('config/config.init')

        # Create url for research
        self.tgt_url = self.config_init['INFO']['URL']

        # Get csv file of unknown words
        self.unknown_words_file = self.config_init['INFO']['FILE']
        self.unknown_words = None

        # Get no_existing_words.csv
        self.no_exist_words_file = self.config_init['INFO']['NO_EXISTING_FILE']

        self.drop_duplicate = []
        # For drop duplicate
        with open('./csv_files/' + self.no_exist_words_file) as f:
            reader = csv.reader(f)
            self.drop_duplicate = [row[0] for row in reader]

        # Read unknown words
        with open('./csv_files/' + self.unknown_words_file) as f:
            reader = csv.reader(f)
            self.unknown_words = [row[0] for row in reader]

        self.word = None
        self.db_client = DbClient()
        self.no_exist_words = []
        self.alre_reg_words = []
        self.reg_words = []
        self.tgt_words = []
        self.total_num = 0

    def insert_word(self, tgt_word, word_meaning):
        """Insert a input word into a table"""
        try:
            self.db_client.insert_word(tgt_word, word_meaning)
        except Exception:
            raise Exception()

    def get_words(self):
        """Get all words in DB"""
        try:
            db_words = self.db_client.get_all_words()
            return db_words
        except Exception:
            raise Exception()

    def search_meaning(self, tgt_word):
        """Search the meaning of the input word"""

        search_url = None
        search_url = self.tgt_url + tgt_word
        # Get content through the URL
        res = requests.get(search_url)

        # 要素を抽出 r.contentはHTMLの内容
        soup = BeautifulSoup(res.content,
                             'html.parser')

        # Get the meaning of the word
        word_meaning = soup.find(class_="content-explanation ej")

        # Check the word exists or not
        if word_meaning:
            word_meaning = word_meaning.get_text()
        else:
            return None

        # Set returned list
        word_meaning = [tgt_word, word_meaning]

        return word_meaning

    def main(self):

        self.total_num = len(self.unknown_words)

        # 登録済みの単語を全て取得
        all_db_words = []
        try:
            all_db_words = self.get_words()
            # wordsオブジェクトのwordプロパティのみ取得
            all_db_words = list(map(lambda x: x.word, all_db_words))
        except Exception:
            print("DBから単語を取得する際にエラーが発生しました")
            sys.exit()

        # Serch the meaning of a input word
        for tgt_word in self.unknown_words:
            # 登録済みの単語であれば調べない
            if tgt_word in all_db_words:
                continue

            # スクレイピング対策のブロック対策
            # 間髪入れずにアクセスすると一時的にアクセス拒否されるっぽい
            time.sleep(0.5)

            print(tgt_word)
            word_meaning = self.search_meaning(tgt_word)

            if not word_meaning:
                print("入力された英単語は存在しません")
                self.no_exist_words.append(tgt_word)
                continue

            # Insert a input word to db table
            try:
                self.word = self.insert_word(tgt_word, word_meaning[1])
            except Exception:
                print("%s は既に登録されている単語です" % tgt_word)
                self.alre_reg_words.append(tgt_word)
                continue

            print("%sは登録されました" % tgt_word)
            print("意味: %s" % word_meaning[1])
            self.reg_words.append(tgt_word)

        print("")
        print("")
        print("単語総数: %d" % self.total_num)
        print("新たに登録された単語数: %d" % len(self.reg_words))
        if len(self.reg_words):
            print(self.reg_words)
        print("不明な単語数:")

        # 調べてもわからなかった単語を書き込む
        if len(self.no_exist_words):
            print(self.drop_duplicate)
            # すでに検索不可として記録されたデータとの差分をとる
            self.drop_duplicate = list(set(self.no_exist_words) - set(self.drop_duplicate))

            if self.drop_duplicate:
                # 検索不可の単語をファイルへ記載()
                with open('./csv_files/' + self.no_exist_words_file, 'a') as f:
                    # 1次元のリストの書き込み
                    # https://qiita.com/elecho1/items/3bc56ca55a600c2e2abc
                    self.drop_duplicate = '\n'.join(self.drop_duplicate) + '\n'
                    f.write(self.drop_duplicate)
            print(self.drop_duplicate)


if __name__ == "__main__":
    get_word_info = RegWordInfo()
    get_word_info.main()
