"""
app_driver.py

provides an interface for the lower level appium calls to other systems of supbot
will be reworked to handle more exceptions
"""
import logging
import os
import re
import shlex
import subprocess
import threading
from typing import Tuple, Optional, List
from appium.webdriver.webelement import WebElement
from appium.webdriver import Remote
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from supbot import g, helper
# noinspection PyBroadException
from supbot.exceptions import DeviceNotFound


class AppDriver:
    """
    Abstracts appium calls
    """

    def __init__(self, driver: Remote, implicit_wait: int):
        self.driver = driver
        self.implicit_wait = implicit_wait

    @staticmethod
    def create() -> Optional['AppDriver']:
        global appium_process
        """
        Initializes appium driver
        """
        # region input from kwargs
        run_server = not ("no_server" in g.kwargs and g.kwargs["no_server"])

        if "port" in g.kwargs and g.kwargs["port"] is not None:
            port = g.kwargs["port"]
        elif run_server:
            port = str(helper.get_free_tcp_port())
        else:
            port = "4723"

        g.logger.info("Finding android device")

        if "device_name" in g.kwargs and g.kwargs["device_name"] is not None:
            device_name = g.kwargs["device_name"]
        elif "device" in g.kwargs and g.kwargs["device"] is not None:
            device_name = g.kwargs["device"]
        else:
            if 'ANDROID_HOME' not in os.environ.keys():
                g.logger.error("`ANDROID_HOME` environment variable not found "
                               "(default: %USERPROFILE%\AppData\Local\Android\Sdk)")
                raise
            adb_path = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', "adb")
            ada_output = ""
            try:
                ada_output = subprocess.check_output([adb_path, "devices"]).decode('utf-8')
            except FileNotFoundError:
                g.logger.error("`ANDROID_HOME` environment variable not setup correctly "
                               "(default: %USERPROFILE%\AppData\Local\Android\Sdk)")
                raise
            search = re.search(r'^(.+)\tdevice', ada_output, flags=re.MULTILINE)
            if search is None:
                g.logger.error("No Android Device Found, Either specify using `device` "
                               "or make sure a device is available in adb")
                raise DeviceNotFound
            device_name = search.group(1)

        if "implicit_wait" in g.kwargs and g.kwargs["implicit_wait"] is not None:
            implicit_wait = g.kwargs["implicit_wait"]
        else:
            implicit_wait = 5

        # endregion

        if run_server:
            def appium_logging():
                global appium_process

                g.logger.info("launching appium server on {}".format(port))
                try:
                    appium_process = subprocess.Popen(shlex.split("appium --port {}".format(port)),
                                                      stdout=subprocess.PIPE, shell=True)
                    appium_logs = logging.getLogger('appium')
                    while g.system.status > -1:
                        line = appium_process.stdout.readline().decode('utf-8')
                        appium_logs.debug(line)
                    appium_process.stdout.close()
                    appium_process.kill()
                except FileNotFoundError:
                    g.logger.error("Appium not installed, install node package manager, "
                                  "then use this command to install `npm install -g appium@1.15.1`")
                    raise

            threading.Thread(target=appium_logging).start()

        g.logger.info("Connecting to appium with {}".format(device_name))
        desired_caps = {
            "platformName": "Android",
            "udid": device_name,
            "appPackage": "com.whatsapp",
            "appActivity": "com.whatsapp.HomeActivity",
            "noReset": "true",
            "deviceName": "Android Emulator"
        }
        driver = None
        try:
            driver = Remote('http://localhost:{}/wd/hub'.format(port), desired_caps)
        except WebDriverException as e:
            if "JAVA_HOME is not set currently" in e.msg:
                g.logger.error("`JAVA_HOME` environment variable not setup correctly "
                              "(default C:\PROGRA~1\Java\jdk1.8.0_181)")
                appium_process.stdout.close()
                appium_process.kill()
                raise

        driver.implicitly_wait(1)
        g.logger.info("driver created")
        return AppDriver(driver, implicit_wait)

    def destroy(self):
        """
        Quits appium drivers
        """
        self.driver.quit()

    def click_on_chat(self, chat_name: str) -> bool:
        """
        Clicks on the chat list item in the app
        :param chat_name: name of the contact
        """
        try:
            search = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")
            element = next(x for x in search if helper.contact_number_equal(x.text, chat_name))
            element.click()
            return True
        except Exception:
            return False

    def type_in_search(self, chat_name: str) -> bool:
        try:
            self.driver.find_element_by_id("com.whatsapp:id/search_src_text").send_keys(chat_name)
            return True
        except NoSuchElementException:
            return False

    def click_search(self) -> bool:
        try:
            self.driver.find_element_by_id("com.whatsapp:id/menuitem_search").click()
            return True
        except Exception:
            return False

    def goto_home(self):
        self.driver.start_activity("com.whatsapp", "com.whatsapp.HomeActivity")

    def type_and_send(self, message: str):
        """
        Entered text in chat, and presses the send button
        :param message: message to send
        """
        try:
            element = self.driver.find_element_by_id('com.whatsapp:id/entry')
            element.send_keys(message)

            element = self.driver.find_element_by_id('com.whatsapp:id/send')
            element.click()

            return True
        except Exception:
            return False

    def click_on_last_chat_link(self):
        self.driver.find_elements_by_id("com.whatsapp:id/message_text").pop().click()
        return True

    def click_ok(self):
        try:
            ok = self.driver.find_element_by_id("android:id/button1")
            ok.click()
            return True
        except NoSuchElementException:
            return False

    def press_back(self):
        """
        presses the back button, then waits for animation/load to finish
        """
        time.sleep(0.5)
        self.driver.press_keycode(4)

    def press_chat_back(self):
        try:
            self.driver.find_element_by_id("com.whatsapp:id/back").click()
            return True
        except Exception:
            return False

    def press_search_back(self):
        try:
            self.driver.find_element_by_id("com.whatsapp:id/search_back").click()
            return True
        except Exception:
            return False

    def get_new_chat(self) -> Optional[str]:
        """
        Checks for chat item with new message bubble,
        used by new_chat checker (checker system not made yet)
        :return: chat (contact_name) who sent a new chat
        """
        try:
            self.driver.implicitly_wait(1)
            element = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id='
                                                        '"com.whatsapp:id/conversations_row_message_count"]/../..'
                                                        '//android.widget.TextView[@resource-id="com.whatsapp:id'
                                                        '/conversations_row_contact_name"]')
            return element.text
        except NoSuchElementException:
            return None
        finally:
            self.driver.implicitly_wait(self.implicit_wait)

    def get_new_bubbles(self):
        return self.driver.find_elements_by_xpath('//android.widget.TextView[@resource-id='
                                                             '"com.whatsapp:id/unread_divider_tv"]/../..'
                                                             '//following-sibling::android.view.ViewGroup'
                                                             '//android.widget.LinearLayout[@resource-id='
                                                             '"com.whatsapp:id/main_layout"]')

    def get_new_messages(self) -> Optional[List[str]]:
        """
        checks for all the new messages
        :return: list of messages sent to the bot
        """
        try:
            new_bubbles = self.get_new_bubbles()

            messages = [Bubble(x).get_message() for x in new_bubbles]
            return messages
        except NoSuchElementException:
            return None

    def get_group_messages(self) -> Optional[List[Tuple[str, str]]]:
        try:
            new_bubbles = self.get_new_bubbles()
            messages = []
            for i, bubble in enumerate(new_bubbles):
                b = Bubble(bubble)
                messages.append((b.get_author(new_bubbles), b.get_message()))

            return messages
        except NoSuchElementException:
            return None

    def send_image(self, image_loc: str) -> bool:
        try:
            _, ext = os.path.splitext(image_loc)
            os.utime(image_loc, (time.time(), time.time()))
            self.driver.push_file(destination_path="/storage/emulated/0/Supbot/temp" + ext,
                                  source_path=image_loc)
            self.driver.find_element_by_id("com.whatsapp:id/input_attach_button").click()
            self.driver.find_element_by_id("com.whatsapp:id/pickfiletype_gallery").click()
            self.driver.find_element_by_xpath('//android.widget.TextView[@text="Supbot"]').click()
            self.driver.find_element_by_xpath('//android.widget.ImageView').click()
            self.driver.find_element_by_id("com.whatsapp:id/send").click()
            return True
        except Exception:
            return False

    def scroll_chat(self, reverse=False):
        try:
            elements = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")
            if reverse:
                self.driver.scroll(elements[1], elements[-1], 3000)
            else:
                self.driver.scroll(elements[-1], elements[1], 3000)
            return True
        except Exception:
            return False

    def check(self, _id, slow: bool = False):
        """
        checks if an element is on screen
        :param _id: id of the element
        :param slow: set to true if used for state.check methods
        :return: True if element exists
        """
        try:
            if slow:
                self.driver.implicitly_wait(self.implicit_wait)

            return self.driver.find_element_by_id(_id) is not None
        except Exception:
            return False
        finally:
            if slow:
                self.driver.implicitly_wait(1)

    # todo make better architecture for check
    def check_scroll_end(self):
        return self.check("com.whatsapp:id/conversations_row_tip_tv")

    def check_scroll_top(self):
        """On top check is done by temp group pined on top"""
        try:
            search = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")
            element = next(x for x in search if helper.contact_number_equal(x.text, "!temp"))
            return element is not None
        except Exception:
            return False

    def check_for_below_chat(self):
        return self.check("com.whatsapp:id/badge")

    def check_group(self) -> bool:
        return self.check("com.whatsapp:id/name_in_group_tv")

    def check_fab(self):
        return self.check("com.whatsapp:id/fab", True)

    def check_search_input(self):
        return self.check("com.whatsapp:id/search_src_text", True)

    def check_chat(self, chat_name):
        return self.check("com.whatsapp:id/conversation_contact_name", True)


# noinspection PyBroadException
class Bubble:
    def __init__(self, web_element: WebElement):
        self.bubble = web_element

    def get_message(self) -> str:
        try:
            return self.bubble.find_element_by_id("com.whatsapp:id/message_text").text
        except Exception:
            return ""

    def _get_author_from_me(self) -> Optional[str]:
        try:
            return self.bubble.find_element_by_id("com.whatsapp:id/name_in_group_tv").text
        except Exception:
            return None

    def get_author(self, bubbles: List[WebElement]) -> Optional[str]:
        my_index = -1
        for bubble_i, bubble in enumerate(bubbles):
            if self.bubble == bubble:
                my_index = bubble_i

        checking = my_index
        while checking >= 0:
            author = Bubble(bubbles[checking])._get_author_from_me()
            if author is not None:
                return author
            checking -= 1

        return None


