import framework
from components.driver_managers import driver_manager
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
from appium.common import exceptions
from selenium.common import exceptions
from framework.paths import DirPaths
from components.mobile.agents import Device
from components.mobile import Platform
import logging
import time
import os
from datetime import datetime, timedelta


class Direction:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


def __get_element(driver, element_dict, timeout=30):
    """
    Function to find an element based on the platform
    :param driver: appium driver
    :param element_dict: element dictionary
    :return: element
    """
    elem = None
    timeout = timeout + 10
    driver.implicitly_wait(timeout)
    logging.info("In get Element")
    try:
        if Device.platform_name == 'Android':
            logging.info("Finding the element for Android")
            logging.info("Element to be found is " + element_dict.get('androidvalue'))
            elem = driver.find_element(element_dict.get('androidby'),
                                       element_dict.get('androidvalue'))
        else:
            logging.info("Finding the element for IOS")
            logging.info("Element to be found is " + element_dict.get('iosvalue'))
            elem = driver.find_element(element_dict.get('iosby'),
                                       element_dict.get('iosvalue'))
    except Exception as E:
        logging.info("Could not Find any element")
        elem = None
    driver.implicitly_wait(180)
    return elem


def __get_elements(driver, element_dict, timeout=30):
    """
    Function to find an multiple elements based on the platform
    :param driver: appium driver
    :param element_dict: element dictionary
    :return: list of elements
    """
    elems = None
    driver.implicitly_wait(timeout)
    logging.info("In get Elements")
    try:
        if Device.platform_name == 'Android':
            logging.info("Finding the element for Android")
            logging.info("Element to be found is " + element_dict.get('androidvalue'))
            elems = driver.find_elements(element_dict.get('androidby'),
                                         element_dict.get('androidvalue'))
        else:
            logging.info("Finding the element for IOS")
            logging.info("Element to be found is " + element_dict.get('iosvalue'))
            elems = driver.find_elements(element_dict.get('iosby'),
                                         element_dict.get('iosvalue'))
    except Exception as E:
        logging.info("Could not Find any element")
        elems = None
    driver.implicitly_wait(150)
    logging.info("Found the element")
    return elems


def find_elements(driver, element_dict, timeout=30):
    """ finds all elements with given criteria
    :param driver: appium driver
    :param element_dict: element dictionary
    :param timeout: time in seconds to search all elements
    :return: list of elements
    """
    logging.info("In find_elements")
    return __get_elements(driver, element_dict, timeout)


def click(driver, element_dict):
    """
    Function to click an element 
    :param driver: appim driver
    :param element_dict: element dictionary 
    :return: 
    """
    try:
        logging.info("In Click")
        elem = __get_element(driver, element_dict)
        elem.click()
        logging.info("Click Performed")
    except exceptions.StaleElementReferenceException:
        try:
            elem = __get_element(driver, element_dict)
            elem.click()
        except exceptions.WebDriverException:
            pass
    except exceptions.WebDriverException:
        pass


def check_exist(driver, element_dict, timeout=30):
    """
    Function 
    :param driver: 
    :param element_dict: 
    :param timeout:
    :return:
    """
    logging.info("In check_exist")
    elem = __get_element(driver, element_dict, timeout)
    try:
        if Device.platform_name == 'Android':
            try:
                if elem.is_displayed():
                    return True
                else:
                    return False
            except exceptions.StaleElementReferenceException:
                elem = find_element(driver, element_dict, timeout)
                if elem.is_displayed():
                    return True
                else:
                    return False

        elif Device.platform_name == 'IOS':
            '''    separate if to check existence of element due to following issues
                    https://github.com/appium/appium/issues/8254
                    https://github.com/facebook/WebDriverAgent/issues/582
                    '''
            if elem is not None:
                return True
            else:
                return False
    except Exception as E:
        return False


def send_keys(driver, element_dict, strvalue):
    """
    :param driver:
    :param element_dict:
    :param strvalue:
    :return:
    """
    try:
        logging.info("In send keys")
        elem = __get_element(driver, element_dict)
        logging.info("enetring value" + strvalue)
        elem.send_keys(strvalue)
    except Exception as E:
        pass


def android_key_press(driver, key_code, metastate=None):
    """Sends a key_code to the device. Android only. Possible key_codes can be
    found in http://developer.android.com/reference/android/view/KeyEvent.html.

    :Args:
     - key_code - the key_code to be sent to the device
     - metastate - meta information about the key_code being sent
    """
    logging.info("in android_key_press")
    driver.press_key_code(key_code, metastate)


def tap(driver, element_dict, x=None, y=None):
    logging.info("In tap")
    try:
        elem = __get_element(driver, element_dict)
        action = TouchAction(driver)
        if x is None and y is None:
            action.tap(elem).perform()
            logging.info("Tapping element")
        else:
            action.tap(elem, x, y).perform()
    except Exception as E:
        pass


def swipe(driver, element_dict, direction, offset, pause_in_ms=3000):
    """
    :param driver:
    :param element_dict:
    :param direction:
    :param offset:
    :param pause_in_ms:
    :return:
    """
    if direction == Direction.LEFT:
        logging.info("swiping left.")
        try:
            elem = __get_element(driver, element_dict)
            action = TouchAction(driver)
            action.press(elem).wait(ms=pause_in_ms)
            action.move_to(x=-offset, y=0).release().perform()
            logging.info("Swipe Action performed - left")
        except Exception as E:
            pass
    elif direction == Direction.RIGHT:
        logging.info("swiping right.")
        try:
            elem = __get_element(driver, element_dict)
            action = TouchAction(driver)
            action.press(elem).wait(ms=pause_in_ms)
            action.move_to(x=offset, y=0).release().perform()
            logging.info("Swipe Action performed - right")
        except Exception as E:
            pass
    elif direction == Direction.DOWN:
        logging.info("scrolling down.")
        try:
            elem = __get_element(driver, element_dict)
            action = TouchAction(driver)
            action.press(elem).wait(ms=pause_in_ms)
            action.move_to(x=0, y=offset).release().perform()
            logging.info("Scroll Action performed - Down")
        except Exception as E:
            pass
    elif direction == Direction.UP:
        logging.info("scrolling up.")
        try:
            elem = __get_element(driver, element_dict)
            action = TouchAction(driver)
            action.press(elem).wait(ms=pause_in_ms)
            action.move_to(x=0, y=-offset).release().perform()
            logging.info("Scroll Action performed - Up")
        except Exception as E:
            pass
    else:
        logging.info("Unknown direction.")


def swipe_on_screen(driver, start_x, start_y, offset_x, offset_y, duration=None):
    """Swipe from one point to another point, for an optional duration.
    - duration - (optional) time to take the swipe, in ms.
    keep offset_x to 0 to swipe UP or DOWN
    keep offset_y to 0 to swipe RIGHT or LEFT
    :Usage: driver.swipe(100, 100, 100, 400)
    """
    try:
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)
        logging.info("swipe on screen.")
        return True
    except Exception as E:
        logging.error("error while swiping on screen.")
        return False


def scroll_element_to_element_on_screen(driver, direction, offset, elements=[], pause_in_ms=3000):
    """ this funtion takes 2 elements from screen and
    :param driver:
    :param direction:
    :param offset:
    :param elements:
    :param pause_in_ms:
    :return:
    """
    if isinstance(elements, list):
        elem_from = elements[0]
        elem_to = elements[1]

        from_x = elem_from.location['x']
        from_y = elem_from.location['y']
        to_x = elem_to.location['x']
        to_y = elem_to.location['y']

        new_offset = to_y - from_y

        if direction == Direction.DOWN:
            logging.info("scrolling down.")
            try:
                action = TouchAction(driver)
                action.press(elem_from).wait(ms=pause_in_ms)
                action.move_to(x=to_x, y=new_offset).release().perform()
                logging.info("Scroll Action performed - Down - scroll_element_to_element_on_screen")
            except Exception as E:
                pass
        elif direction == Direction.UP:
            logging.info("scrolling up.")
            try:
                elem = __get_element(driver, elements)
                action = TouchAction(driver)
                action.press(elem).wait(ms=pause_in_ms)
                action.move_to(x=-offset, y=0).release().perform()
                logging.info("Scroll Action performed - Up - scroll_element_to_element_on_screen")
            except Exception as E:
                pass


def clear_text(driver, element_dict):
    """ Function to clear text from the edit box field
    :param driver:      appium driver
    :param element_dict:    locator
    :returns: None
    """
    try:
        elem = __get_element(driver, element_dict)
        elem.clear()
        logging.info("In clear_text - text cleared")
    except exceptions:
        logging.info("Exception - Could not clear text")
        pass


def close_application(driver):
    """ Function to close an application
    :param driver:      appium driver
    :returns: None
    """
    logging.info("App closed")
    driver.quit()  # close_app()


def get_element_attribute(driver, element_dict, attribute):
    """ This could be a generic function to fetch the attribute if an element.
    for Android it takes an attribute 'text'
    for iOS the attribute is 'value'
    :param driver:  appium driver
    :param element_dict:     locator
    :param attribute:  the assigned value to the locator
    :return attr:   atrribute text/value
    """
    try:
        logging.info("in get element attribute")
        elem = __get_element(driver, element_dict)
        attr = elem.get_attribute(attribute)
        logging.info("Found the desired attribute")
        return attr
    except exceptions:
        logging.info("Could not find the attribute")
        pass


def input_text(driver, element_dict, text):
    """ Function to enter text in to the edit box field
    :param driver:  appium driver
    :param element_dict:     locator
    :param  text:  text to be entered in to the box field
    """
    logging.info("In input text")
    try:
        elem = __get_element(driver, element_dict)
        elem.send_keys(text)
        logging.info("Text entered : " + text)
    except exceptions:
        logging.info("could not enter text" + text)
        pass


def long_press(driver, element_dict):
    """ Function to long press an element on to the screen
    :param driver:  appium driver
    :param element_dict:     locator
    """
    logging.info("In long press")
    try:
        elm = __get_element(driver, element_dict)
        long_press = TouchAction(driver).long_press(elm)
        long_press.perform()
        logging.info("long press performed")
    except exceptions:
        pass


def open_application():
    """ Function to open the application
    :return: 
    """
    driver = driver_manager.instantiate()
    return driver


def go_back(driver):
    """ Function to go back by one level 
    :param driver:     appium driver
    """
    logging.info("in go back")
    try:
        driver.back()
        logging.info("Back action performed")
    except Exception as E:
        logging.info("Back action not performed")
        pass


def wait_until_page_contains_element(driver, element_dict, timeout=5):
    """
    Function to check the presence of an element on the page within the specified time
    :param driver: appium driver
    :param element_dict: locator
    :param timeout: timeout
    :return: result / True
    """
    logging.info('Waiting for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    if check_exist(driver, element_dict, timeout):
        logging.info('Element found on the page!')
        return True
    else:
        logging.warning('Element not found on the page in specified time = ' + str(timeout) + ' seconds')
        return False


def wait_until_page_does_not_contain_element(driver, element_dict, timeout=5):
    """
    Function to confirm the element not present on the page within the specified time
    :param driver: 
    :param element_dict: 
    :param timeout: 
    :return:  true/result 
    """
    logging.info('Looking for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    print('Looking for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    result = False
    num = 1
    while num <= timeout:
        if check_exist(driver, element_dict, 2):
            time.sleep(1)
            num = num + 1
        else:
            logging.info('Element is NOT present on the page!')
            result = True
            break
    return result


def page_should_contain_element(driver, element_dict):
    """ 
    Function to confirm the existance of the locator on the page
    :param driver:  appium driver 
    :param element_dict: locator
    :return: False / Status=True
    """
    status = check_exist(driver, element_dict)
    if not status:
        logging.info('Element present On the page!')
        return status
    else:
        logging.info('Page does not contain element!')
        return False


def page_should_not_contain_element(driver, element_dict):
    """
    Function to confirm the locator absence on the page
    :param driver: appium driver
    :param element_dict: locator
    :return: True/False
    """
    status = check_exist(driver, element_dict)
    if not status:
        print('Page does not Contains required element')
        return True
    else:
        logging.warning('Element present on the page')
        return False


def element_should_be_disabled(driver, element_dict):
    """
    Function to check the element is disabled or not
    :param driver: appium driver
    :param element_dict: locator
    :return: True/False
    """
    logging.info("in element_should_be_disabled ")
    elem = __get_element(driver, element_dict)
    try:
        if elem.is_enabled():
            logging.info("Element still enabled returning false")
            return False
        else:
            logging.info("Element not enabled returning True")
            return True
    except Exception as E:
        return False


def element_should_be_enabled(driver, element_dict):
    """
    Function to check the element is enabled on page
    :param driver: appium driver
    :param element_dict: locator
    :return: True/False
    """
    logging.info("in element_should_be_enabled")
    elem = __get_element(driver, element_dict)
    try:
        if elem.is_enabled():
            logging.info("Element still displayed returning true")
            return True
        else:
            logging.info("Element not displayed returning false")
            return False
    except Exception as E:
        return False


def input_password(driver, element_dict, text):
    """
    Function to enter the text in to the password field
    :param driver: appium driver
    :param element_dict: locator
    :param text: user password 
    :return: None
    """
    logging.info("in input_password")
    try:
        elem = __get_element(driver, element_dict)
        logging.info("sending password" + text)
        elem.send_keys(text)
    except Exception as E:
        pass


def background_app(driver, timeout=5):
    """
    Function to background the application for specified time
    :param driver: appium driver
    :param timeout: time defined for the background activity
    :return: none
    """
    logging.info("In background_app")
    try:
        driver.background_app(timeout)
    except Exception as E:
        pass


def click_a_point(driver, x=0, y=0, duration=100):
    """
    Function to click a specific point on the application on the basis on x and y co-ordinates
    :param driver: appium driver 
    :param x: x co-ordinate
    :param y: y co-ordinatee
    :param duration: default 1 second
    :return: False
    """
    logging.info("Clicking on a point (%s,%s)." % (x, y))
    action = TouchAction(driver)
    try:
        action.press(x=float(x), y=float(y)). \
            wait(float(duration)). \
            release(). \
            perform()
        return True
    except Exception as e:
        print(e)
        logging.warning("'Can\'t click on a point at (%s,%s)' % (x, y)")
        return False


def long_press_key_code(driver, key_code, metastate=None):
    """Sends a long press of key_code to the device.
    Android only.
    See `press key_code` for more details.
    :param driver: appium driver 
    :param key_code: key_code
    :param metastate: meta information about the key_code being sent
    """
    logging.info("In long_press_key_code - key_code:" + str(key_code))
    driver.long_press_key_code(int(key_code), metastate)


def page_should_contain_text(driver, text):
    """
    Function to find text from the page
    :param driver: appium driver
    :param text: text 
    :return: True/False
    """
    logging.info("In page_should_contain_text")
    return text in driver.page_source


def page_should_not_contain_text(driver, text):
    """
    Functioan to confirms the text is not on the page 
    :param driver: appium driver
    :param text: text 
    :return: True/False
    """
    logging.info('Checking if page does not contain text: ' + text)
    if text not in driver.page_source:
        return True
    else:
        return False


def wait_until_page_does_not_contain_text(driver, text, timeout=5):
    """
    Function to confirm the text is not present on the page within the specified time
    :param driver: appium driver
    :param text: text to be searched on the page
    :param timeout: default 5
    :return:  True/False 
    """
    logging.info('Looking for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    print('Looking for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    timeout = time.time() + timeout  # Timer based on wait_time to prevent infinite loops
    while True:
        time.sleep(0.2)  # Prevent CPU slamming with short timeout between loops
        if time.time() > timeout:
            logging.info('Page does not contain text ')
            return False
        if text in driver.page_source:
            return True


def wait_until_page_contain_text(driver, text, timeout=5):
    """
    Function to confirm the text is not present on the page within the specified time
    :param driver: appium driver
    :param text: text to be searched on the page
    :param timeout: default 5 sec
    :return:  True/False
    """
    logging.info('Looking for an element on the screen, max wait = ' + str(timeout) + ' seconds')
    timeout = time.time() + timeout  # Timer based on wait_time to prevent infinite loops
    while True:
        time.sleep(0.2)  # Prevent CPU slamming with short timeout between loops
        if time.time() > timeout:
            logging.info('Page Does Not Contain text on the page ')
            return False
        if text in driver.page_source:
            logging.info('Page Contain text on the page ')
            return True


def capture_screenshot(driver):
    """
    Function to capture page screenshot, saves the screenshot in the to the snapshots folder
    :param driver: appium driver
    :return: None
    """
    directory = '%s\snapshots/' % os.getcwd()
    file_name = 'screenshot.png'
    driver.save_screenshot(directory + file_name)
    logging.info('Screenshot saved at the location:{0}'.format(directory))


def find_element(driver, element_dict, timeout=30):
    return __get_element(driver, element_dict, timeout)


def vertical_scroll_until_presence_of_element(driver, direction=Direction.DOWN, element_dict={}, max_search_time=30,
                                              timeout=1):
    """ function scrolls the screen and tries to search the element within given max time.
    :param driver: appium driver
    :param direction: direction of scrolling (top / bottom)
    :param element_dict: element locator
    :param max_search_time: max time to keep scolling
    :param timeout: timeout to locate element.
    :return: located element else False
    """
    logging.info("In vertical_scroll_until_presence_of_element")
    try:
        if element_dict != {}:
            print('Locating element might take maximum ' + str(max_search_time) + ' seconds')
            end_time = datetime.now() + timedelta(seconds=max_search_time)
            while datetime.now() < end_time:
                if check_exist(driver, element_dict, timeout):
                    return find_element(driver, element_dict)
                if Platform.name == 'Android':
                    if direction == Direction.DOWN:
                        driver.swipe(400, 700, 400, 300)
                    elif direction == Direction.UP:
                        driver.swipe(50, 300, 50, 700)
                elif Platform.name == 'IOS':
                    if direction == Direction.DOWN:
                        swipe_on_screen(driver, 400, 700, 400, 300)
                    elif direction == Direction.UP:
                        swipe_on_screen(driver, 400, 300, 400, 700)
            logging.info('Could not find element after scrolling for ' + str(max_search_time) + ' seconds')
            return False
        else:
            return False
    except Exception as E:
        return False


def check_exist_iOS(driver, element_dict, timeout=30):
    """
    separate function to check existence of element due to following issues
    https://github.com/appium/appium/issues/8254
    https://github.com/facebook/WebDriverAgent/issues/582
    :param driver:
    :param element_dict:
    :param timeout:
    :return:
    """
    elem = __get_element(driver, element_dict, timeout)
    try:
        if elem is not None:
            return True
        else:
            return False
    except Exception as E:
        return False


def tap_element_by_coordinates(driver, element_dict):
    """

    :param driver: appium driver
    :param element_dict: element to tap
    :return:
    """
    elem = __get_element(driver, element_dict)
    try:
        if elem is not None:
            logging.info('element found for tap element by coordinates')
            x = round(elem.rect['x'])
            y = round(elem.rect['y'])
            height = round(elem.rect['height'])
            width = round(elem.rect['width'])
            new_x = x + round(width / 2)
            new_y = y + round(height / 2)

            logging.info('element will be tapped on x:' + str(new_x) + ' and y:' + str(new_y))
            action = TouchAction(driver)
            action.tap(x=new_x, y=new_y)
            action.perform()
            return True
        else:
            return False
    except Exception as E:
        return False


def get_device_locator(locator_key):
    """

    :param locator_key:
    :return: element dict with locator value
    """
    element_dict = {'androidby': MobileBy.XPATH,
                    'androidvalue': '',
                    'iosby': MobileBy.ID, 'iosvalue': ''}
    try:
        logging.info('getting device locator for ' + locator_key)
        locator_value = framework.ConfigFileParser.get_value(DirPaths.device_locator_file_path,
                                                             Platform.device_locator_section_name,
                                                             locator_key)

        logging.info('device locator for ' + locator_key + ' is ' + locator_value)
        element_dict = {'androidby': MobileBy.XPATH,
                        'androidvalue': locator_value,
                        'iosby': MobileBy.ID, 'iosvalue': ''}
        return element_dict
    except Exception as E:
        logging.error(Platform.device_locator_section_name + ' device locator for ' + locator_key +
                      ' could not found')
        return element_dict


def hide_keyboard(driver):
    """ Function to hide keyboard
    :param driver:     appium driver
    """
    logging.info("in hide keyboard")
    try:
        driver.hide_keyboard()
        logging.info("hide keyboard")
    except Exception as E:
        logging.info("not able to hide keyboard")
        pass


def tap_element_by_coordinates_offset(driver, element_dict, off_x=0, off_y=0):
    """
    :param driver: appium driver
    :param element_dict: element to tap
    :param off_x: x co-ordinate
    :param off_y: y co-ordinate
    :return:
    """
    elem = __get_element(driver, element_dict)
    try:
        if elem is not None:
            logging.info('element found for tap element by coordinates')
            x = round(elem.rect['x'])
            y = round(elem.rect['y'])
            height = round(elem.rect['height'])
            width = round(elem.rect['width'])
            new_x = (x + round(width)) - off_x
            new_y = (y + round(height)) - off_y

            logging.info('element will be tapped on x:' + str(new_x) + ' and y:' + str(new_y))
            action = TouchAction(driver)
            action.tap(x=new_x, y=new_y)
            action.perform()
            return True
        else:
            return False
    except Exception as E:
        return False


def is_element_checked(driver, element_dict, timeout=10):
    """ Checks if checkbox is checked or not
    :param driver:
    :param element_dict:
    :param timeout:
    :return:
    """
    if check_exist(driver, element_dict, timeout):
        elem = find_element(driver, element_dict)
        attr = elem.get_attribute('checked')
        if str(attr) == 'true':
            logging.info('Located element is selected')
            return True
        elif str(attr) == 'false':
            logging.error('Located element is NOT selected')
            return False
    else:
        logging.error('Element is NOT displayed on screen')
        return False


def get_device_specific_value(key):
    """
    :param key:
    :return: value
    """
    value = ''
    try:
        logging.info('getting device value for ' + key)
        value = framework.ConfigFileParser.get_value(DirPaths.device_locator_file_path,
                                                     Platform.device_locator_section_name, key)

        logging.info('device value for ' + key + ' is ' + value)

        return value
    except Exception as E:
        logging.error(Platform.device_locator_section_name + ' device specific value for ' + key +
                      ' could not found')
        return value
