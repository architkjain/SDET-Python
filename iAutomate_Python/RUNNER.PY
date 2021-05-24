import argparse
import framework
from framework.AutoExceptions import ValidationFailedException
import sys
import time
import os
from components.mobile.agents import Device
from components.web.agents import Browser
import datetime


def __get_cli_args():
    """ registers all CLI arguments
    :return: arguments
    """
    parser = argparse.ArgumentParser()
    o = parser.add_mutually_exclusive_group()
    o.add_argument('-a', action='store_true')
    o.add_argument('-b', action='store_true')
    parser.add_argument('-suite', help='suite file name for execution')
    parser.add_argument('-log', help='LOG level for the execution', default='INFO',
                        choices=['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'])
    args = parser.parse_args()
    return args


def __input_validations(args):
    """
    :param args:
    :return:
    """
    if args.suite:
        suite_file = args.suite
    else:
        suite_file = ''
    # else:
    #     suite_file = framework.PropertyFileParser.get_value('Test.SuiteFile').strip() == ''
    #     if suite_file == '':
    #         print('Suite file name is not provided in properties file. test run will quit.')
    #         raise ValidationFailedException('Suite file name is not provided in properties file. test run will quit.')
    return suite_file, args.log.upper()


if __name__ == '__main__':
    arguments = __get_cli_args()
    try:
        suite_file, log_level = __input_validations(arguments)
    except ValidationFailedException as VFE:
        print(VFE)
        sys.exit(2)

    framework.Paths.buildpaths(allpaths=True)
    framework.utils.LogUtils.backup_logs()
    logging_mode = framework.PropertyFileParser.get_value('Logging.Mode')
    framework.Logging.initialize(log_level, logging_mode)
    server_config = framework.PropertyFileParser.get_value('ServerConfig')
    framework.Server.build('Servers.ini', server_config)
    Device.appium_build(os.path.join(framework.Paths.agent_cap_dir,
                                     framework.PropertyFileParser.get_value(
                                         'Device.Properties') + '.properties'))

    Browser.selenium_build(os.path.join(framework.Paths.agent_cap_dir,
                                        framework.PropertyFileParser.get_value(
                                            'Browser.Properties') + '.properties'))

    suite = framework.TestSuiteBuilder.buildtestsuite()
    suite.run()

    sys.exit()
