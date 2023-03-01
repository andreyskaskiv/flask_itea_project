import datetime
import json
import random
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from definitions import PATH_TO_CREDENTIALS, PATH_TO_TESTS_INTEGRATION_IMG


class TestGenerateDB(unittest.TestCase):
    self = None
    name_function = None
    now_date = None
    service = None
    chrome_options = None
    browser: webdriver.chrome = None
    base_url: str = None
    random_user: dict[str, str] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome_options = Options()
        # cls.chrome_options.add_argument("--headless")  # without GUI
        # cls.service = Service(executable_path=r"tests_integration/chromedriver.exe")

        cls.browser = webdriver.Chrome(options=cls.chrome_options)
        cls.base_url = 'http://127.0.0.1:5000/'

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.browser.quit()

    @classmethod
    def create_screenshot(cls, filename) -> None:
        cls.now_date = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")
        cls.browser.save_screenshot(f"{PATH_TO_TESTS_INTEGRATION_IMG}\\{filename}_{cls.now_date}.png")

    def test_aa_generate_database(self):
        self.browser.get(self.base_url)
        self.assertEqual(self.browser.title, 'Home')
        generate_db_link = self.browser.find_element(By.XPATH, '//input[@id="submit"]')
        generate_db_link.click()

        alert_text = self.browser.find_element(By.XPATH, '//*[@id="alert_block"]').text
        self.assertIn('Database filled with test data', alert_text)

    def test_ab_login_with_new_credentials(self):
        with open(PATH_TO_CREDENTIALS) as file:
            credentials = json.load(file)

        type(self).random_user = random.choice(credentials)
        self.browser.find_element(By.XPATH, '//span[@id="login_menu_icon_color"]').click()
        self.assertEqual(self.browser.title, 'Login')

        self.browser.find_element(By.ID, 'email').send_keys(self.random_user['email'])
        self.browser.find_element(By.ID, 'password').send_keys(self.random_user['password'])
        self.browser.find_element(By.ID, 'submit').click()
        self.create_screenshot(self._testMethodName)
        hello_message = self.browser.find_element(By.TAG_NAME, 'h2').text
        self.assertIn(f'Hello, {self.random_user["username"]}', hello_message)
        self.assertEqual(self.browser.current_url, self.base_url)

    def test_ac_account_page(self):
        self.browser.find_element(By.XPATH, '//img[@alt="avatar"]').click()
        self.create_screenshot(self._testMethodName)
        self.assertEqual(self.browser.title, 'Account')

    def test_ad_search_city(self):
        self.browser.find_element(By.XPATH, '//a[@class="dropdown-toggle"]').click()
        self.browser.find_element(By.XPATH, '//a[@id="search_city"]').click()
        self.create_screenshot(self._testMethodName)
        self.assertEqual(self.browser.title, 'Get city')

    def test_ae_input_cities(self):
        cities = ['Barcelona', 'Tokyo', 'New York', 'Las Vegas', 'London']
        for city in cities:
            self.browser.find_element(By.XPATH, '//input[@id="city_name"]').send_keys(city)
            self.browser.implicitly_wait(1)
            self.browser.find_element(By.XPATH, '//input[@id="Show"]').click()
            time.sleep(3)
            self.create_screenshot(self._testMethodName)
            self.browser.find_element(By.XPATH, '//button[@id="addCity"]').click()
            self.browser.implicitly_wait(1)
            self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//a[@class="dropdown-toggle"]').click()
        self.browser.find_element(By.XPATH, '//a[@id="monitor_weather"]').click()

        self.create_screenshot(self._testMethodName)
        self.assertEqual(self.browser.title, f'Cities of {self.random_user["username"]}')

    def test_af_show_city_detail(self):
        self.browser.find_element(By.XPATH, '//input[@value="1"]').click()
        delete_city_name = self.browser.find_element(By.XPATH, '//*[@id="citiesTable"]/tbody/tr/td[3]/a').text
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//button[@id="selectButtonDelete"]').click()

        alert_text = self.browser.find_element(By.XPATH, '//div[@id="alert_block"]').text
        self.browser.implicitly_wait(1)
        self.create_screenshot(self._testMethodName)
        self.assertIn(f'Deleted: {delete_city_name}', alert_text)

    def test_ag_blog_title(self):
        """Blog page"""
        blog_url = 'http://127.0.0.1:5000/posts/'
        self.browser.get(blog_url)
        self.create_screenshot(self._testMethodName)
        self.assertEqual(self.browser.title, 'Blog')

    def test_ah_blog_user_post(self):
        """User blog page"""

        user_name_post = self.browser.find_element(By.XPATH,
                                                   '//*[@id="content"]/div/div/div/div/table/tbody/tr[1]/td/div/div/a').text
        self.browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/table/tbody/tr[1]/td/div/div/a').click()

        self.assertEqual(self.browser.title, 'Title author')

        user_name_posts = self.browser.find_element(By.XPATH,
                                                   '//*[@id="content"]/div/div/article/div/div/a').text
        self.create_screenshot(self._testMethodName)
        self.assertIn(user_name_post.split(',')[0], user_name_posts.split(',')[0])


if __name__ == '__main__':
    unittest.main()


