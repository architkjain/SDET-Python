"""Test case implementation"""
import os
import csv
import framework
from framework.resultlogger import log_test_result, log_step_result
import logging
from framework import AutoExceptions
from framework.resultlogger import flogger
from framework import Status
from framework.screenshots import get_snapshots


class AutoTest(object):
    """"""

    group_init_failed = False
    status = 'Pass'
    name = None
    testdata_source = None
    group_name = None
    group_data_setup = None
    step_results = []

    def __init__(self, *args):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        self._test_method_name = 'test'
        self._resultForDoCleanups = None
        self.log_test_result = log_test_result
        self.log_step_result = self.autotestlogstepresult
        try:
            testmethod = getattr(self, self._test_method_name)
        except AttributeError:
            raise ValueError("no such test method in %s: %s" % (self.__class__, self._test_method_name))
        self._test_method_doc = testmethod.__doc__
        self._cleanups = []
        self.name = self.__class__.__name__
        self.get_data()
        self.step_results = list()

        for current_test_data in self.testdata_source:
            self.testdata = current_test_data
            try:
                self.set_up()
            except AutoExceptions.StepFailException as e:
                flogger.error(e)
            except Exception as e:
                flogger.error('Generic Error in setUp(): %s', str(e))
                self.status = Status.ERROR
            else:
                try:
                    if args:
                        testmethod.__call__(args)
                    else:
                        testmethod.__call__()
                except AutoExceptions.StepFailException as e:
                    flogger.error(e)
                except Exception as e:
                    flogger.error('Generic Error in %s(): %s', testmethod.__name__, str(e))
                    self.status = Status.ERROR
            finally:
                try:
                    self.tear_down()
                except AutoExceptions.StepFailException as e:
                    flogger.error(e)
                except Exception as e:
                    flogger.error('Generic Error in tear_down(): %s', str(e))
                    self.status = Status.ERROR

    def __tc_over__(self):
        log_test_result(self.group_name, self.__class__.__name__, self.status)
        self.status = 'Pass'

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def get_data(self, csv_filename=None):
        f = None
        if csv_filename:
            test_data_file = os.path.join(framework.Paths.test_data_dir, csv_filename)
        else:
            test_data_file = os.path.join(framework.Paths.test_data_dir, self.__class__.__name__ + ".csv")

        if not os.path.isfile(test_data_file):
            logging.info('Default test data csv does not exist.')
            self.testdata_source = []
        else:
            try:
                f = open(test_data_file, 'rt')
                readerh = csv.DictReader(f)
                reclist = []
                for row in readerh:
                    if str(row['flag']).upper() == 'Y':
                        reclist.append(row)
                self.testdata_source = reclist
            finally:
                f.close()

    def autotestlogstepresult(self, stepname, stepdescription, expected, actual, status, comment=''):

        snapshot_links = []
        if status in [Status.FAIL, Status.ERROR]:
            snapshot_links = get_snapshots()

        self.step_results.append({'step': actual, 'status': status, 'comment': comment, 'snapshots': snapshot_links})
        if self.status == 'Pass':
            self.status = status

        log_step_result(self.name, stepname, stepdescription, expected, actual, status, comment, snapshot_links)

        if status == 'Fail':
            raise AutoExceptions.StepFailException(
                'Test Step Failed. Name: ' + stepname + '. Description: ' + stepdescription)

