import pymssql
import logging


"""
WINDOWS : pymssql installation is required.
          use pip for pymssql installation
          command : pip install pymssql
MacOS X:
        FreeTDS is required. install FreeTDS using Homebrew and then pymssql using pip
        commands :
                    1. brew install freetds
                    2. pip install pymssql
       """


class ConnectionManager:
    """"""
    __server = ''
    __user = ''
    __password = ''
    __db_name = ''
    __conn = None

    def __init__(self, server, user, password, dbname):
        self.__server = server
        self.__user = user
        self.__password = password
        self.__db_name = dbname

    def connect_to_database(self):
        """
        :return:
        """
        try:
            logging.debug('connecting... to database "%s" on server "%s"' % (self.__db_name, self.__server))
            print('connecting to database "%s" on server "%s"' % (self.__db_name, self.__server))
            self.__conn = pymssql.connect(self.__server, self.__user, self.__password, self.__db_name)
            logging.debug('connected to database "%s" on server "%s"' % (self.__db_name, self.__server))
        except Exception as E:
            logging.debug('Error while connecting to database "%s" on server "%s"' % (self.__db_name, self.__server))
            print('Error while connecting to database "%s" on server "%s"' % (self.__db_name, self.__server))

    def execute_query(self, query, commit=False):
        """ Executes a SQL query and returns a list of rows. Each row is a dict object.
        :param String query: The sql query passed as string.
        :param String commit: The boolean flag to commit if the query is DDL or DML.
        :return: List of rows. Each row is a dictionary.
        """
        cursor = self.__conn.cursor(as_dict=True)
        return_list = []
        logging.info("Query: "+query)
        cursor.execute(query)
        if commit:
            self.__conn.commit()
            return return_list

        for row in cursor:
            return_list.append(row)
        return return_list

    def execute_stored_proc(self):
        """ NOT IMPLEMENTED YET
        :return:
        """
        pass

    def disconnect_from_database(self):
        """
        :return:
        """
        self.__conn.close()
        logging.info("Disconnecting from Database")



