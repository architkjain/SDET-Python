import datetime
import framework
from components.driver_managers.driver_manager import Driver
from components.driver_managers import driver_manager
from framework.input_file_manager import PropertyFileParser
import logging


def get_snapshots():
    if PropertyFileParser.get_value('EnableScreenshot').upper() != "TRUE":
        return

    paths_string = []

    dt = datetime.datetime.now()
    ts = dt.strftime('%Y_%m_%d_%H_%M_%S')
    try:
        appium_snapshot_name = ts + '_device.png'
        appium_snapshotpath = framework.Paths.snapshots_dir + '/' + appium_snapshot_name
        appium_screenshottaken = Driver.appiumdriver.save_screenshot(appium_snapshotpath)
        if appium_screenshottaken:
            paths_string.append(appium_snapshotpath)
    except:
        pass

    try:
        selenium_snapshot_name = ts + '_web.png'
        selenium_snapshotpath = framework.Paths.snapshots_dir + '/' + selenium_snapshot_name
        selenium_screenshottaken = Driver.seleniumdriver.save_screenshot(selenium_snapshotpath)
        if selenium_screenshottaken:
            paths_string.append(selenium_snapshotpath)
    except Exception as e:
        pass

    return paths_string


def image_to_binary(snapshotlinks, n):
    """
    :param snapshotlinks: list of string paths
    :param n: index of image path to convert into binary
    :return:
    """
    li = snapshotlinks
    dev_image_data = bytearray()
    dev_image_binary = None
    try:
        if li:
            link = li[n - 1]
            fl = open(link, "rb")
            bin_data = fl.read()
            fl.close()
            for byte in bin_data:
                dev_image_data.append(byte)

            if len(dev_image_data) > 0:
                dev_image_binary = dev_image_data
    except Exception as e:
        print(e)

    return dev_image_binary
