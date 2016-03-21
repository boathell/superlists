from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

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




		# self.assertIn('A new list item', response.content.decode())
		# expected_code = render_to_string('home.html', {'new_item_text': 'A new list item'})
		# self.assertEqual(response.content.decode(), expected_code)

	# 测试是否只保存POST请求
	## 重构时，这个测试已经不再需要了
	# def test_home_page_only_saves_items_when_necessary(self):
	# 	request = HttpRequest()
	# 	home_page(request)
	# 	self.assertEqual(Item.objects.count(), 0)


	# 检查模板是否能显示多个待办事项
	# 在Page82删除，不再需要
	# def test_home_page_displays_all_list_items(self):
	# 	Item.objects.create(text='itemey 1')
	# 	Item.objects.create(text='itemey 2')

	# 	request = HttpRequest()
	# 	response = home_page(request)

	# 	self.assertIn('itemey 1', response.content.decode())
	# 	self.assertIn('itemey 2', response.content.decode())
	
class NewListTest(TestCase):
	# 测试POST请求能否被正确保存
	def test_saving_a_POST_request(self):
		# 使用self.client.POST重写下面四行语句
		# request = HttpRequest()
		# request.method = 'POST'
		# request.POST['item_text'] = 'A new list item'
		# response = home_page(request)
		self.client.post('/lists/new', data={'item_text' : 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	# 测试POST请求提交后是否重新定向
	def test_redirects_after_POST(self):
		# 使用self.client.POST重写下面四行语句，注意数据库操作，末尾不加斜线
		# request = HttpRequest()
		# request.method = 'POST'
		# request.POST['item_text'] = 'A new list item'
		# response = home_page(request)
		response = self.client.post('/lists/new', data={'item_text' : 'A new list item'})

		# self.assertEqual(response.status_code, 302)
		# 使用assertRedirectst替代assertEqual
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

# class ItemModelTest(TestCase):
class ListAndItemModelsTest(TestCase):
	"""Test the Model of ITEM and LIST"""
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_only_items_for_that_list(self):
		currect_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=currect_list)
		Item.objects.create(text='itemey 2', list=currect_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = self.client.get('/lists/%d/' % (currect_list.id,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')


class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text' : 'A new item for an existing list'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post('/lists/%d/add_item' % (correct_list.id,), {'item_text':'A new item for an existing list'})
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id, ))
