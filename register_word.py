import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/db')
from db_client import DbClient

if __name__ == '__main__':
    print(sys.path)
    db_clnt = DbClient()
    words = db_clnt.get_words()
    print(words)
