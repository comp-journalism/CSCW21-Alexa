import sqlite3
import datetime
import logging

__author__ = 'HK Dambanemuya'
__version__ = 'Python2'

'''
    Database class for reading and writing queries and responses
'''
class Database():

    def __init__(self, file_path):
        self.file_path = file_path
        # Open database connection
        connection = sqlite3.connect(file_path)
        # Read SQL query to create table
        with open('create_tables.sql', 'r') as fd:
            sqlFile = fd.read()
        # Execute SQL query
        c = connection.cursor()
        c.execute(sqlFile)
        # Close database connection
        connection.close()

    def write_response(self, source, message, response):
        # Read SQL query to write response
        with open('write_response.sql', 'r') as fd:
            sqlFile = fd.read()
        # Write transcribed smart speaker response to database
        try:
            # Open database connection
            connection = sqlite3.connect(self.file_path)
            c = connection.cursor()
            # Format query tuple
            query_tuple  = (source, message, response)
            # Execute SQL query
            c.execute(sqlFile, query_tuple)
            # Commit changes to database
            connection.commit()
        # Handle and save exceptions in error log
        except Exception as e:
            logging.info(e)
            with open('error_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),'w') as file:
                file.write(logging.info(e))
                file.write(source)
                file.write(message)
                file.write(response) 

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S')
