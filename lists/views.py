from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home_page(request):
	# 正确的
	return render(request, 'home.html', { 'new_item_text': request.POST.get('item_text', '')})
	# 错误的
	# return render(request, 'home.html', { 'new_item_text': request.POST['item_text']})