from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item
# Create your views here.


def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')

	items = Item.objects.all()

	return render(request, 'home.html', {'items' : items})

	# 正确的
	# return render(request, 'home.html', { 'new_item_text': request.POST.get('item_text', '')})
	# 错误的
	# return render(request, 'home.html', { 'new_item_text': request.POST['item_text']})

