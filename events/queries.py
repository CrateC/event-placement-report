SELECT_ID = """SELECT id FROM events_platforms
                WHERE short_name='{0}';
            """

DROP_TABLE = """DROP TABLE IF EXISTS {0};
            """


"""MySQL"""

MYSQL_CREATE_TEMP = """
                CREATE
                TEMPORARY TABLE IF NOT EXISTS {0} AS
                SELECT name,(LINK) AS {0}, date
                FROM events_events
                WHERE platform_id =
                    (SELECT id
                     FROM events_platforms
                     WHERE short_name='{0}')
                  AND LANGUAGE = 'ru'
                GROUP BY date ORDER BY date;
            """


MYSQL_LEFT_JOIN = """
                SELECT t1.date,
                       t1.name,
                       t1.CA,
                       t2.PA,
                       t4.CO,
                       t3.KA
                FROM CA AS t1
                LEFT JOIN PA AS t2 ON t1.date = t2.date
                LEFT JOIN KA AS t3 ON t1.date = t3.date
                LEFT JOIN CO AS t4 ON t1.date = t4.date
                WHERE t1.date > CURDATE()
                ORDER BY t1.date;
            """


""" SQLite3 """

SQLITE3_CREATE_TEMP = """
                CREATE TEMP TABLE IF NOT EXISTS {} AS
                SELECT name,
                       (LINK) AS {}, date
                FROM {events_events}
                WHERE platform_id =
                    ( SELECT id
                     FROM events_platforms
                     WHERE short_name='{}' )
                  AND LANGUAGE = 'ru'
                GROUP BY date ORDER_BY date

            """

SQLITE3_LEFT_JOIN = """
                SELECT t1.date,
                       t1.name,
                       t1.CA,
                       t2.PA,
                       t4.CO,
                       t3.KA
                FROM temp.CA AS t1
                LEFT JOIN temp.PA AS t2 ON t1.date = t2.date
                LEFT JOIN temp.KA AS t3 ON t1.date = t3.date
                LEFT JOIN temp.CO AS t4 ON t1.date = t4.date
                WHERE t1.date > datetime('NOW')
                ORDER BY t1.date;

            """
