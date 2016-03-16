
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

	# 断言方法三，测试辅助方法，可以测试多个待办事项，不能以test开头，不会作为测试运行
	# 习惯上，辅助方法放在tearDown后面
    def check_for_row_in_list_table(self, row_text):
    	table = self.browser.find_element_by_id('id_list_table')
    	rows = table.find_elements_by_tag_name('tr')
    	self.assertIn(row_text, [row.text for row in rows])

    # 功能测试主题部分。函数以test开头，表示测试所用。
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # print(header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
        	inputbox.get_attribute('placeholder'), 'Enter a to-do item'
        	)

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
		

        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # import time
        # time.sleep(10)

        # 断言方法一和二需要用到table和rows
        # table = self.browser.find_element_by_id('id_list_table')
        #注意这里是find_elements_by_tag_name，如果写成element会报TypeError: 'WebElement' object is not iterable错误
        # rows = table.find_elements_by_tag_name('tr')

        # 断言方法一，只能测试第一个待办事项
        # self.assertTrue(
        # 	any(row.text == '1: Buy peacock feathers' for row in rows),
        # 	"New to-do list did not appear in table -- its text was :\n %s" % (table.text)
        # 	)

        # 断言方法二，也只能测试第一个待办事项
        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

	    # 作为一个标记，每次都执行
	    # self.fail('Finish the test!')

# 当在命令行执行时执行
if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()
