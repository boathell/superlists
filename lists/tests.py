from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
	# 测试“/”能否正确解析到home_page
	def test_root_url_resolves_to_home_page_view(self):
		# 解析"/"
		found = resolve('/')

		# 验证解析"/"的函数名，是否为home_page
		self.assertEqual(found.func, home_page)

	# 测试请求的home_page是否正确
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
		# print(expected_code)
		self.assertEqual(response.content.decode(), expected_code)

	# 测试POST请求能否被正确保存
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

		# self.assertIn('A new list item', response.content.decode())
		# expected_code = render_to_string('home.html', {'new_item_text': 'A new list item'})
		# self.assertEqual(response.content.decode(), expected_code)
	# 测试是否只保存POST请求
	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)

	# 测试POST请求提交后是否重新定向
	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
 
	# 检查模板是否能显示多个待办事项
	# 在Page82删除，不再需要
	# def test_home_page_displays_all_list_items(self):
	# 	Item.objects.create(text='itemey 1')
	# 	Item.objects.create(text='itemey 2')

	# 	request = HttpRequest()
	# 	response = home_page(request)

	# 	self.assertIn('itemey 1', response.content.decode())
	# 	self.assertIn('itemey 2', response.content.decode())

class ItemModelTest(TestCase):

	# 测试是否能正确保存ITEM
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')