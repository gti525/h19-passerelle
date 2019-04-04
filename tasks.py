#!/bin/sh
import logging

logger = logging.getLogger(__name__)


#
# Small script to show PostgreSQL and Pyscopg together
#

def cancel_transaction(transaction_id=None):
    if transaction_id is None:
        pass
    import psycopg2
    import os
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    logger.info("About to clear pending transaction...")
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS)
        logger.info("Connection successful")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(str(error))


    cur = conn.cursor()

    try:
        cur.execute(
            """UPDATE transaction set status = (CASE WHEN current_timestamp > created + (15 ||' minutes')::interval THEN 
            'Canceled' ELSE 'Pending' END) WHERE id={} AND status = 'Pending' ;""".format(transaction_id))
        conn.commit()
        cur.close()
        rowcount = cur.rowcount
        if rowcount >=1:
            logger.info("Transaction {} was set to status Canceled".format(transaction_id))
        else:
            logger.info("No rows were affected")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(str(error))


