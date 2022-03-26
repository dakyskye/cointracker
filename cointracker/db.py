import os
from datetime import datetime
from typing import Callable
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

from cointracker.crawler import CrawlerResult

_TABLE_BITCOIN_PRICES = "bitcoin_prices"

_CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS %s 
    (
        id             INTEGER PRIMARY KEY AUTO_INCREMENT,
        date_inserted  DATETIME UNIQUE NOT NULL,
        price_current  DOUBLE          NOT NULL,
        price_24h_low  DOUBLE          NOT NULL,
        price_24h_high DOUBLE          NOT NULL
    )
"""

_INSERT_QUERY = """
    INSERT INTO %s (date_inserted,
                   price_current,
                   price_24h_low,
                   price_24h_high)
    VALUES (?, ?, ?, ?)
"""

_db: MySQLConnection
_cur: CMySQLCursor


def init():
    global _db
    global _cur
    _db = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        port=os.environ['MYSQL_PORT'],
        database=os.environ['MYSQL_DATABASE'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD']
    )
    _cur = _db.cursor()

    for table in [_TABLE_BITCOIN_PRICES]:
        _cur.execute(_creation_query_for_table(table))
    _db.commit()


def close():
    _db.commit()
    _db.close()


InsertFN = Callable[[CrawlerResult], None]


def _creation_query_for_table(table: str):
    return _CREATION_QUERY % table


def _insert_query_for_table(table: str):
    # the trick here is that mysql uses %s for sql parameters
    # so we have ONE %s in original insert query for formatting purposes
    # then we replace question marks with %s-s
    fmt = _INSERT_QUERY % table
    return fmt.replace('?', '%s')


def insert_bitcoin_stat(stat: CrawlerResult):
    _cur.execute(
        _insert_query_for_table(_TABLE_BITCOIN_PRICES),
        [
            str(datetime.now()),
            stat['price_current'],
            stat['price_24h_low'],
            stat['price_24h_high']
        ]
    )
    _db.commit()
