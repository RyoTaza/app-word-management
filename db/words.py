from datetime import datetime
import sys
from sqlalchemy import Column, Integer, String, DateTime
from setting import Base
from setting import ENGINE


class Words(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'words'
    id = Column('id', Integer, primary_key=True)
    word = Column('word', String(200))
    created = Column('created', DateTime,
                     default=datetime.now, nullable=False)
    modified = Column('modified', DateTime,
                      default=datetime.now, nullable=False)


def main(args):
    """
    メイン関数
    """
    # テーブル作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)
