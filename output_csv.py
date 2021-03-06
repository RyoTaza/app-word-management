import sys
# import requests
import csv
# from bs4 import BeautifulSoup
from db.db_client import DbClient


class OutputCsv(object):
    """
    wordsテーブルにある単語をCSVファイルに出力する
    """

    def __init__(self):
        self.db_client = DbClient()
        self.all_words = None

    def get_all_words(self):
        """
        Insert a input word into a table
        """
        try:
            all_words = self.db_client.get_all_words()
            return all_words
        except Exception as e:
            print("DBエラーが発生しました")
            print(e)

    def create_words_list(self, words_obj_list):
        """
        selectしたwordsオブジェクトの配列を単語と意味を
        格納した２次元配列にする
        """
        words_list = []
        for word in words_obj_list:
            words_list.append([word.word, word.japanese])
        return words_list

    def main(self):
        try:
            self.all_words = self.get_all_words()
            if not self.all_words:
                print("取得する単語がありません")
                sys.exit(1)
        except Exception as e:
            print("Unknow error occured. Reffer to below")
            print(e)
            sys.exit(1)

        # DBから取得されたデータはオブジェクトなので、英単語と意味の配列が格納された
        # 配列を作成する（入れ子）
        words_list = self.create_words_list(self.all_words)

        # wordsテーブルの単語をCSV出力する
        with open('./csv_files/words.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(words_list)


if __name__ == "__main__":
    get_word_info = OutputCsv()
    get_word_info.main()
