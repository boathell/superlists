
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	# 启动时执行
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

	# 测试完毕后执行，自动关闭浏览器
    def tearDown(self):
        self.browser.quit()

    # 功能测试主题部分。函数以test开头，表示测试所用。
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header_text)
        # print(header_text)

        inputbox = self.browser.find_element_by_id('id_item')
        self.assertEqual(
        	inputbox.getattribute('placeholder'), 'Enter a to-do item'
        	)

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
        	any(row.text == '1: Buy peacock feathers' for row in rows))

        # 作为一个标记，每次都执行
        self.fail('Finish the test!')

# 当在命令行执行时执行
if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()
