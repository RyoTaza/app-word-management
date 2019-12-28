import sys
import requests
from bs4 import BeautifulSoup
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/db')
from db.db_client import DbClient


class RegWordInfo(object):
    """
    引数の英単語をDBに格納し、CSVファイルに追記する
    記載されていたら、新しいファイルを作成する
    """

    def __init__(self, args):
        args = sys.argv
        if len(args) > 2 or len(args) == 1:
            print(len(args))
            print("単語は1語を指定するか、2語以上の場合はダブルクォートで指定してください")
            sys.exit(1)

        self.word = None
        self.tgt_word = args[1]
        self.db_client = DbClient()

    def insert_word(self, tgt_word, word_meaning):
        """Insert a input word into a table"""
        try:
            self.db_client.insert_word(tgt_word, word_meaning)
        except Exception as e:
            print(e)
            print("DBエラーが発生しました")

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

        # Serch the meaning of a input word
        word_meaning = self.search_meaning(self.tgt_word)

        print("登録された英単語")
        print("単語: %s" % word_meaning[0])
        print("意味: %s" % word_meaning[1])

        if not word_meaning:
            print("入力された英単語は存在しません")
            sys.exit(1)

        # Insert a input word to db table
        try:
            self.word = self.insert_word(self.tgt_word, word_meaning[1])
        except Exception as e:
            print("Unknow error occured. Reffer to below")
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    get_word_info = RegWordInfo(sys.argv)
    get_word_info.main()
