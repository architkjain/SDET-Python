import datetime
import os
import framework


class DirPaths:
    suite = None
    log_level = None
    log_file_path = None

    root_dir = None
    framework_dir = None
    tests_dir = None
    test_suites_dir = None
    test_data_dir = None
    logs_dir = None
    snapshots_dir = None
    agent_cap_dir = None
    logfilepath = None
    suitefile = None
    suitefileabsolutepath = None
    stepresultsfilepath = None
    testresultsfilepath = None
    logs_backup_dir = None
    htmlreportfilepath = None
    clear_cache_file_path = None
    device_locator_file_path = None

    @staticmethod
    def buildpaths(allpaths=True):
        DirPaths.__built__ = True
        dt = datetime.datetime.now()

        framework.Run.id = dt.strftime('%Y_%m_%d_%H_%M_%S')
        DirPaths.framework_dir = os.path.dirname(os.path.abspath(__file__))

        DirPaths.root_dir = os.path.dirname(DirPaths.framework_dir)

        DirPaths.logs_dir = os.path.join(DirPaths.root_dir, 'logs')
        DirPaths.snapshots_dir = os.path.join(DirPaths.logs_dir, 'snapshots')
        DirPaths.logs_backup_dir = os.path.join(DirPaths.logs_dir, 'backup')

        DirPaths.tests_dir = os.path.join(DirPaths.root_dir, 'tests')
        DirPaths.test_suites_dir = os.path.join(DirPaths.root_dir, 'suites')
        DirPaths.test_data_dir = os.path.join(DirPaths.root_dir, 'testdata')

        DirPaths.agent_cap_dir = os.path.join(DirPaths.root_dir, 'agent_capabilities')

        DirPaths.clear_cache_file_path = os.path.join(DirPaths.root_dir, 'clear_cache')
        DirPaths.device_locator_file_path = os.path.join(DirPaths.root_dir,
                                                         'testreusables\\MobilePageObjects', 'device_locators.ini')

        if allpaths:
            DirPaths.log_file_path = os.path.join(DirPaths.logs_dir, framework.Run.id) + '.log'
            DirPaths.stepresultsfilepath = os.path.join(DirPaths.logs_dir, "STEP_RESULTS_" + framework.Run.id) + '.csv'
            DirPaths.testresultsfilepath = os.path.join(DirPaths.logs_dir, "TEST_RESULTS_" + framework.Run.id) + '.csv'
            DirPaths.htmlreportfilepath = os.path.join(DirPaths.logs_dir, "HTML_REPORT_" + framework.Run.id) + '.html'

            print('\nFRAMEWORK PATHS : ')
            print('root_dir : ' + DirPaths.root_dir)
            print('framework_dir : ' + DirPaths.framework_dir)
            print('logs_dir : ' + DirPaths.logs_dir)
            print('logs_backup_dir : ' + DirPaths.logs_backup_dir)
            print('snapshots_dir : ' + DirPaths.snapshots_dir)
            print('tests_dir : ' + DirPaths.tests_dir)
            print('test_suites_dir : ' + DirPaths.test_suites_dir)
            print('test_data_dir : ' + DirPaths.test_data_dir)
            print('agent_caps_dir : ' + DirPaths.agent_cap_dir)
            print('logfilepath : ' + DirPaths.log_file_path)
            print('stepresultsfilepath : ' + DirPaths.stepresultsfilepath)
            print('testresultsfilepath : ' + DirPaths.testresultsfilepath)
            print('htmlreportfilepath : ' + DirPaths.htmlreportfilepath)
            # print('clear_cache_file_path : ' + DirPaths.clear_cache_file_path)
            # print('device_locator_file_path : ' + DirPaths.device_locator_file_path)

            print('\n')
