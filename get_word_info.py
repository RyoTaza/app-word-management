import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/db')
from db_client import DbClient


class GetWrodInfo(object):
    """
    引数の英単語をDBに格納し、CSVファイルに追記する
    CSVファイルは100個ごとで分けるため、単語が100個
    記載されていたら、新しいファイルを作成する
    """

    def __init__(self, args):
        args = sys.argv
        if len(args) > 2 or len(args) == 1:
            print(len(args))
            print("単語は1語を指定するか、2語以上の場合はダブルクォートで指定してください")
            sys.exit(1)

        self.tgt_word = args[1]
        self.db_client = DbClient()

    def insert_word(self, tgt_word):
        self.db_client.insert_word(tgt_word)

    def main(self):
        self.insert_word(self.tgt_word)


if __name__ == "__main__":
    get_word_info = GetWrodInfo(sys.argv)
    get_word_info.main()
