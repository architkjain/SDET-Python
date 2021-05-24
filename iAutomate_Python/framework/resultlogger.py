# -*- coding: utf-8 -*-
#
from os import path
import framework
from framework.interfaces.resultlogger import IDefaultResultLogger
from framework.screenshots import image_to_binary
from framework.paths import DirPaths
import logging
import sqlite3

flogger = logging.getLogger(__name__)


class SQLiteLogger(IDefaultResultLogger):
    db_file = None
    cursor = None
    conn = None
    logtestresult = None
    logstepresult = None
    create_logtest_table = 'CREATE TABLE testresult (' \
                           'GroupName  text,' \
                           'TestCase  text,' \
                           'Status  text' \
                           ')'

    create_logteststep_table = 'CREATE TABLE stepresult (' \
                               'TestName  text, ' \
                               'StepName  text, ' \
                               'StepDescription  text, ' \
                               'StepVerification  text, ' \
                               'ActualResult  text, ' \
                               'Status  text,' \
                               'Comment  text, ' \
                               'SnapShot  text,' \
                               'SnapShotSecondary  blob, ' \
                               'SnapShotlink  blob' \
                               ')'

    def __new__(cls, *args, **kwargs):
        return super(SQLiteLogger, cls).__new__(cls)

    def __init__(self, db_file):
        self.db_file = db_file
        try:
            self.conn = sqlite3.connect(db_file)
            cursor = self.conn.cursor()
            cursor.execute(self.create_logtest_table)
            cursor.execute(self.create_logteststep_table)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        return self.conn

    def log_test_result(self, group_name, testcase, status):
        """
        logs test result into db
        :param group_name: script name
        :param testcase: Case name in script
        :param status: new Status one of the - Pass Fail Error Skip
        :return: None
        """
        conn = None
        try:
            conn = self.create_connection()
            self.cursor = conn.cursor()
            query = "INSERT INTO testresult (GroupName, TestCase, Status) values (?,?,?)"
            param = (group_name, testcase, status)
            data = self.cursor.execute(query, param)
            conn.commit()
            self.cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()
                # print("The SQLite connection is closed")

    def log_step_result(self, testname, stepname, stepdescription, stepverify,
                        actualresult, status, comment="", snapshotlinks=()):
        """ Logs step result into db
        :param stepname: Name of the Step
        :param stepdescription: Step to execute
        :param stepverify: Verification for the step to perform
        :param actualresult: Customized Actual result
        :param status: Status one of the - Pass Fail Error Skip
        :param comment: Comment if any
        :param snapshot: binary data of the image or None
        :param secondary_snapshot: binary data of the image or None
        :param snapshotlink: link of both the snapshots on host
        :return: None
        """

        snapshot = image_to_binary(snapshotlinks, 1)
        secondary_snapshot = image_to_binary(snapshotlinks, 2)
        conn = self.create_connection()
        cursor = None
        if len(snapshotlinks) > 0:
            snapshotlinks = ', '.join(snapshotlinks)
        else:
            snapshotlinks = ''
        try:
            cursor = conn.cursor()

            if snapshot is not None and secondary_snapshot is not None:
                query = "INSERT INTO stepresult " \
                        "(TestName, StepName, StepDescription, StepVerification, ActualResult, Status, Comment, " \
                        "SnapShot, SnapShotSecondary, SnapShotlink) " \
                        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?)"

                params = (testname, stepname, stepdescription, stepverify, actualresult, status, comment,
                          snapshot, secondary_snapshot, snapshotlinks)

            elif snapshot is not None:
                query = "INSERT INTO stepresult " \
                        "(TestName, StepName, StepDescription, StepVerification, ActualResult, Status, Comment, " \
                        "SnapShot, SnapShotlink) " \
                        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"

                params = (testname, stepname, stepdescription, stepverify, actualresult, status, comment,
                          snapshot, snapshotlinks)

            elif secondary_snapshot is not None:
                query = "INSERT INTO stepresult " \
                        "(TestName, StepName, StepDescription, StepVerification, ActualResult, Status, Comment, " \
                        "SnapShotSecondary, SnapShotlink ) " \
                        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"

                params = (testname, stepname, stepdescription, stepverify, actualresult, status, comment,
                          secondary_snapshot, snapshotlinks)

            else:
                query = "INSERT INTO stepresult " \
                        "(TestName, StepName, StepDescription, StepVerification, ActualResult, Status, Comment, SnapShotlink )" \
                        " VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

                params = (testname, stepname, stepdescription, stepverify, actualresult, status, comment,
                          snapshotlinks)

            cursor.execute(query, params)
            conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        except Exception as e:
            print(e)

        finally:
            if conn:
                conn.close()
                # print("The SQLite connection is closed")

    def readtestresult(self):
        query = "SELECT * from testresult"
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor = cursor.execute(query)
        for item in cursor.fetchall():
            print(item)

    def readstepresult(self):
        query = "SELECT * from stepresult"
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor = cursor.execute(query)
        for item in cursor.fetchall():
            print(item)


class CSVLogger(IDefaultResultLogger):
    stepresultfilepath = 'None'
    testresultfilepath = 'None'

    def __init__(self, test_result_file_path, step_result_file_path):
        self.stepresultfilepath = step_result_file_path
        self.testresultfilepath = test_result_file_path

    def log_test_result(self, group_name, testcase, status):
        """
        logs test result into csv
        :param group_name: script name
        :param testcase: Case name in script
        :param status: new Status one of the - Pass Fail Error Skip
        :return: None
        """
        if path.isfile(self.testresultfilepath):
            with open(self.testresultfilepath, "a") as resopen:
                resopen.write(group_name + ',' + testcase + ',' + status + '\n')
        else:
            with open(self.testresultfilepath, "a") as resopen:
                resopen.write('GROUPNAME,TESTCASE,STATUS\n')
                resopen.write(group_name + ',' + testcase + ',' + status + '\n')

    def log_step_result(self, testname, stepname, stepdescription, stepverify,
                        actualresult, status, comment="", snapshotlinks=()):
        """ Logs step result into csv
        :param stepname: Name of the Step
        :param stepdescription: Step to execute
        :param stepverify: Verification for the step to perform
        :param actualresult: Customized Actual result
        :param status: Status one of the - Pass Fail Error Skip
        :param comment: Comment if any
        :param snapshotlinks: link of both the snapshots on host
        :return: None
        """
        if len(snapshotlinks) > 0:
            snapshotlink = ', '.join(snapshotlinks)
        else:
            snapshotlink = ''

        if path.isfile(self.stepresultfilepath):
            with open(self.stepresultfilepath, "a") as resopen:
                resopen.write(testname + ',' + stepname + ',' + stepdescription + ',' + stepverify
                              + ',' + actualresult + ',' + status + ',' + comment + ',' + snapshotlink + '\n')
        else:
            with open(self.stepresultfilepath, "a") as resopen:
                resopen.write('TESTNAME,STEPNAME,STEPDESCRIPTION,STEPVERIFY,ACTUALRESULT,STATUS,COMMENT,SNAPSHOTLINK\n')
                resopen.write(testname + ',' + stepname + ',' + stepdescription + ',' + stepverify
                              + ',' + actualresult + ',' + status + ',' + comment + ',' + snapshotlink + '\n')


class Logging:
    db = 'db'
    csv = 'csv'
    both = 'both'
    __mode = None
    logger_objects = []

    @staticmethod
    def set_result_logging_mode(mode):
        mode = str(mode).lower()
        log_str = ''
        if mode not in [Logging.both, Logging.db, Logging.csv]:
            log_str += 'Invalid logging mode is passed. Logging mode is set to default.\n'
            Logging.__mode = Logging.csv
        else:
            Logging.__mode = mode

        log_str += 'Logging Mode: ' + Logging.__mode
        logging.info(log_str)
        print(log_str)

    @staticmethod
    def get_logging_mode():
        return Logging.__mode

    @staticmethod
    def initialize(log_level='INFO', logging_mode=''):
        """
        :param log_level:
        :param logging_mode:
        :return:
        """
        logging.basicConfig(format='%(asctime)s ::: %(pathname)s,%(lineno)d :::  %(levelname)s ::: %(message)s',
                            filename=DirPaths.log_file_path, level=log_level.upper())
        Logging.set_result_logging_mode(logging_mode)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        c_handler = logging.StreamHandler()
        c_handler.setLevel(log_level)
        c_format = logging.Formatter('%(message)s')
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        global flogger
        flogger = logger

        csvl = CSVLogger(DirPaths.testresultsfilepath, DirPaths.stepresultsfilepath)
        sqll = SQLiteLogger(path.join(DirPaths.logs_dir, framework.Run.id + '.db'))
        Logging.logger_objects.append(csvl)
        Logging.logger_objects.append(sqll)


def log_test_result(group_name, testcase, status):
    try:
        for logger in Logging.logger_objects:
            logger.log_test_result(group_name, testcase, status)
    except:
        pass

def log_step_result(testname, stepname, stepdescription, expected, actual, status, comment='', snapshots_links=()):
    """
    :param stepname:
    :param stepdescription:
    :param expected:
    :param actual:
    :param status:
    :param comment:
    :param snapshots_links:
    :return:
    """
    try:
        for logger in Logging.logger_objects:
            logger.log_step_result(testname, stepname, stepdescription, expected, actual, status, comment, snapshots_links)
    except:
        pass