import requests
from bs4 import BeautifulSoup
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/db')
from db.db_client import DbClient
import csv


class RegWordInfo(object):
    """
    引数の英単語をDBに格納し、CSVファイルに追記する
    記載されていたら、新しいファイルを作成する
    """

    def __init__(self):

        self.unknown_words = None
        with open('./csv_files/unknown_words.csv') as f:
            reader = csv.reader(f)
            self.unknown_words = [row[0] for row in reader]

        self.word = None
        # self.tgt_word = args[1]
        self.db_client = DbClient()
        self.alre_reg_words = []
        self.no_exist_words = []
        self.reg_words = []
        self.total_num = 0

    def insert_word(self, tgt_word, word_meaning):
        """Insert a input word into a table"""
        try:
            self.db_client.insert_word(tgt_word, word_meaning)
        except Exception:
            raise Exception()

    def search_meaning(self, tgt_word):
        """Search the meaning of the input word"""
        # Create url for research
        TGT_URL = "https://ejje.weblio.jp/content/"
        TGT_URL = TGT_URL + tgt_word

        # Get content through the URL
        res = requests.get(TGT_URL)

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

        # Serch the meaning of a input word
        for tgt_word in self.unknown_words:
            word_meaning = self.search_meaning(tgt_word)
            # print("%s の登録開始" % tgt_word)

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
        print("登録された単語数: %d" % len(self.reg_words))
        print(self.reg_words)
        print("不明な単語数: %d" % len(self.no_exist_words))
        print(self.no_exist_words)


if __name__ == "__main__":
    get_word_info = RegWordInfo()
    get_word_info.main()
