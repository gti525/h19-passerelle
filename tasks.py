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
    print("About to clear pending transaction...")
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS)
        print("Connection successful")
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))

        print("I am unable to connect to the database")

    cur = conn.cursor()

    try:
        cur.execute(
            """UPDATE transaction set status = (CASE WHEN current_date > created + (15 ||' minutes')::interval THEN 
            'Canceled' ELSE 'Pending' END) WHERE id={} ;""".format(transaction_id))
        print("Transaction pending for more than 15 minutes have been delete")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Cant update")
        print(str(error))


