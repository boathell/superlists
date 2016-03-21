from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List
# Create your views here.


def home_page(request):
	return render(request, 'home.html')

	# 正确的
	# return render(request, 'home.html', { 'new_item_text': request.POST.get('item_text', '')})
	# 错误的
	# return render(request, 'home.html', { 'new_item_text': request.POST['item_text']})

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	items = Item.objects.filter(id=list_)
	return render(request, 'list.html', {'items': items})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.object.get(id=list_id)
	Item.object.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id, ))