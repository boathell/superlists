from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		# 解析"/"
		found = resolve('/')

		# 验证解析"/"的函数名，是否为home_page
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)

		# 测试方法一：对比字节
		# self.assertTrue(response.content.startswith(b'<html>'))
		# self.assertIn(b'<title>To-Do lists</title>', response.content)
		# print (response.content)
		# self.assertTrue(response.content.strip().endswith(b'</html>'))

		# 测试方法二：对比unicode字符串
		expected_code = render_to_string('home.html')
		print(expected_code)
		self.assertEqual(response.content.decode(), expected_code)