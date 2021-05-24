from framework import PropertyFileParser
from framework import Paths as fpaths
from framework.resultlogger import Logging, log_test_result
from framework import Status
from framework.resultlogger import flogger
from framework.reporting.ExtentHTMLReport import HTMLTestRunner
import framework
import csv
import sys
import logging
import os
import datetime
from math import ceil
from threading import Thread


class _Test:
    name = None
    status = Status.PENDING
    result = None
    stacktrace = None  # decide DS for this
    group_name = None

    def __init__(self, name, group_name):
        """
        :param name:
        :param group_name:
        """
        self.name = name
        self.status = Status.PENDING
        self.result = []
        self.stacktrace = None
        self.group_name = group_name

    def set_info(self, testobj):
        """
        :param testobj:
        :return:
        """
        self.__doc__ = testobj.__doc__

    def set_status(self, status: str, result=[]):
        """
        :param status:
        :param result:
        :return:
        """
        # based on the status of the tests associa
        self.status = status
        self.result.extend(result)

    @staticmethod
    def create_tests(tests_in_group) -> list:
        """
        :param tests_in_group:
        :return:
        """
        tests_in_group.sort(key=lambda x: x['testcase'])
        list_t = []
        for test in tests_in_group:
            t = _Test(test['testcase'], test['groupname'])
            list_t.append(t)
        return list_t


class _Group:
    name = None
    count = None
    tests = []
    group_init = None
    group_cleanup = None
    group_data_setup = None
    status = Status.PENDING
    start_time = None
    end_time = None
    test_status_counts = {}

    def set_status(self):
        """
        :return:
        """
        # based on the status of the tests associated

        status = None
        test_statuses = set([s.status for s in self.tests])

        # Ordering as following
        # [PENDING, EXECUTING, SKIP, ERROR, FAIL, PASS]

        if Status.PENDING in test_statuses:
            status = Status.PENDING
        elif Status.EXECUTING in test_statuses:
            status = Status.EXECUTING
        elif Status.ERROR in test_statuses:
            status = Status.ERROR
        elif Status.FAIL in test_statuses:
            status = Status.FAIL
        elif Status.SKIP in test_statuses:
            status = Status.SKIP
        else:
            status = Status.PASS

        self.status = status

        test_status_counts = dict.fromkeys(Status.get_ordered_status(), 0)
        for test in self.tests:
            test_status_counts[test.status] += 1

        self.test_status_counts = test_status_counts

    @staticmethod
    def create_groups(list_of_tests) -> list:
        """
        :param list_of_tests:
        :return: list(_Group)
        """
        list_grps = []
        grps = list(set([g['groupname'] for g in list_of_tests]))
        grps.sort()

        for grp_name in grps:
            g = _Group()
            g.name = grp_name
            tests = list(filter(lambda x: x['groupname'] == g.name, list_of_tests))
            g.tests = _Test.create_tests(tests)
            g.count = len(g.tests)
            list_grps.append(g)
        return list_grps


class _TestSuite:
    groups = []
    _start_time = None
    _end_time = None

    def __init__(self, list_of_tests):
        """ Creates group and also creates the list of cases inside it """
        self.groups = _Group.create_groups(list_of_tests)
        self.count = len(self.groups)

    def run(self):
        """ Runs the entire test suite"""
        fp = open(fpaths.htmlreportfilepath, 'wb')
        extent_report = HTMLTestRunner(stream=fp)

        flogger.info('--' * 10 + ' EXECUTION STARTED ' + '--' * 25)
        threaded_groups = self.__get_threads()
        livethreads = []

        for grps in threaded_groups:
            t = ThreadRunner(grps)
            t.start()
            livethreads.append(t)

        for t in livethreads:
            if t.is_alive():
                t.join()

        flogger.info('--' * 10 + ' EXECUTION COMPLETED ' + '--' * 20 + '\n')
        flogger.info('                --- x0x--- END --- x0x---')
        extent_report.stopTime = datetime.datetime.now()
        extent_report.generateReport(self)

    def __get_threads(self):
        """
        :return:
        """
        # get fraction from properties
        try:
            num = int(PropertyFileParser.get_value("TotalThreads"))
        except:
            num = 1

        if num <= 0:
            num = 1

        num_threads = ceil(len(self.groups) / num)
        start = 0
        end = num_threads
        threaded_groups = []
        total_groups = len(self.groups)
        while start < total_groups:
            threaded_groups.append(self.groups[start:end])
            start = end
            end += num_threads
        return threaded_groups

    @staticmethod
    def _run_group_init(group: _Group):
        """
        :param group:
        :return:
        """
        group.start_time = datetime.datetime.now()
        groupinitfunc = framework.PyUtils.get_group_init('tests.' + group.name)
        group.group_init = groupinitfunc
        # handle call and if any exception skip all the tests
        try:
            if groupinitfunc is not None:
                flogger.info('running groupInit for group "' + group.name + '" ...')
                group_data_setup = groupinitfunc.__call__()
                group.group_data_setup = group_data_setup
                flogger.info('groupInit for group "' + group.name + '" Completed.')
        except Exception as ee:
            flogger.error('Exception in the groupInit function.')
            flogger.error(str(ee) + '\n')
            # mark all cases as skipped
            try:
                for test in group.tests:
                    test.status = Status.SKIP
                    d = {'status': Status.SKIP, 'step': 'Skipping test ' + test.name + '. groupInit failed'}

                    # test.set_status()
                    # test.stacktrace.append(str(ee)) # None object
                    # test.stacktrace = ee.with_traceback()  # need to check
            except:
                pass

    @staticmethod
    def _run_group_cleanup(group: _Group):
        """
        :param group:
        :return:
        """
        groupcleanupfunc = framework.PyUtils.get_group_cleanup('tests.' + group.name)
        group.group_cleanup = groupcleanupfunc
        # handle call
        try:
            if groupcleanupfunc is not None:
                flogger.info('running groupCleanup for group "' + group.name + '" ...')
                groupcleanupfunc.__call__()
                flogger.info('groupCleanup for group "' + group.name + '" Completed.')
        except Exception as ee:
            flogger.error('something went wrong in the groupInit function.')
            flogger.error(str(ee) + '\n')

        group.end_time = datetime.datetime.now()


class TestSuiteBuilder:
    filename = ''
    filepath = ''
    count_of_tests = 0
    list_of_tests_to_execute = []
    test_case_level_elapsed_time = []
    db_logger = None
    result = []

    @staticmethod
    def buildtestsuite(module=None) -> _TestSuite:
        TestSuiteBuilder.filename = PropertyFileParser.get_value('Test.SuiteFile')
        TestSuiteBuilder.filepath = os.path.join(fpaths.test_suites_dir, TestSuiteBuilder.filename)

        if not os.path.isfile(TestSuiteBuilder.filepath):
            flogger.error('The suite file "' + os.path.join(fpaths.test_suites_dir, TestSuiteBuilder.filename)
                          + '" does not exist. RUNNER will now quit.')
            sys.exit(3)

        list_tests_to_execute = []
        f = None
        try:
            f = open(TestSuiteBuilder.filepath, 'rt')

            readerh = csv.DictReader(f)
            if module is None:
                for row in readerh:
                    if row.get('EXECUTE').upper() == 'Y':
                        testdict = {'sr': row.get('SR'), 'groupname': row.get('GROUPNAME'),
                                    'testcase': row.get('TESTCASE'), 'execute': row.get('EXECUTE'),
                                    'status': Status.PENDING}
                        list_tests_to_execute.append(testdict)
            else:
                for row in readerh:
                    if row.get('EXECUTE').upper() == 'Y' and row.get('GROUPNAME') == module:
                        testdict = {'sr': row.get('SR'), 'groupname': row.get('GROUPNAME'),
                                    'testcase': row.get('TESTCASE'), 'execute': row.get('EXECUTE'),
                                    'status': Status.PENDING}
                        list_tests_to_execute.append(testdict)
        finally:
            f.close()

        if not list_tests_to_execute:
            flogger.warning('List of tests to execute is Empty. Quiting!')
            sys.exit(3)

        TestSuiteBuilder.list_of_tests_to_execute = list_tests_to_execute
        TestSuiteBuilder.count_of_tests = len(list_tests_to_execute)

        test_suite = _TestSuite(list_tests_to_execute)
        return test_suite


class ThreadRunner(Thread):
    groups = None

    def __init__(self, groups):
        super().__init__()
        self.groups = groups

    def run(self):

        for group in self.groups:
            # handle group_init()
            _TestSuite._run_group_init(group)

            for test in group.tests:
                test.start_time = datetime.datetime.now()
                if test.status == Status.SKIP:
                    # status was set in __run_group_setup()
                    flogger.error('Skipping test ' + test.name)
                    test.end_time = datetime.datetime.now()
                    # __tc_over__() log skip result

                elif test.status == Status.PENDING:
                    testobj = None
                    testinstance = None
                    try:
                        testobj = framework.PyUtils.import_class("tests." + group.name + "." + test.name)
                    except AttributeError as ae:
                        flogger.info('skipping TestCase : ' + test.name)
                        test.set_status(Status.ERROR, [str(ae)])
                        test.end_time = datetime.datetime.now()
                        flogger(str(ae))
                        # __tc_over__() log skip result
                        continue
                    except Exception as e:
                        flogger.info('skipping TestCase : ' + test.name)
                        test.set_status(Status.ERROR, [str(e)])
                        test.end_time = datetime.datetime.now()
                        flogger(str(e))
                        # __tc_over__() log skip result
                        continue
                    else:
                        flogger.info('running TestCase : ' + test.name)
                        testobj.name = test.name
                        testobj.group_name = group.name
                        testobj.group_data_setup = group.group_data_setup
                        test.set_status(Status.EXECUTING)
                        test.set_info(testobj)
                        # following will execute the case. Try to remove it from __init__()
                        testinstance = testobj()
                        test.end_time = datetime.datetime.now()
                        test.set_status(testinstance.status, testinstance.step_results)
                        print('--' * 40)
                        framework.colors.print_yellow('TestCase : ' + testobj.name + ' run completed...')
                        logging.info('TestCase : ' + testobj.name + ' run completed...')

                    finally:
                        testinstance.__tc_over__()  # change the result logging mechanism
                        TestSuiteBuilder.result.append(testinstance)

            # handle group_cleanup()
            _TestSuite._run_group_cleanup(group)
            group.set_status()
