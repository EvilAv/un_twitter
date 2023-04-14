from django.shortcuts import render
from django.http import JsonResponse
from .models import Test


# Create your views here.
def home_page(request):
    return render(request, 'tweets/index.html')


def test_view(request, start):
    if start >= len(Test.objects.all()):
        return JsonResponse({})
    elif start + 40 >= len(Test.objects.all()):
        end = len(Test.objects.all()) - 1
    else:
        end = start + 40
    test_list = Test.objects.all()[start:end]
    json_list = [{'text': i.text} for i in test_list]
    data = {
        'name': 'aaaa',
        'data': json_list,
    }
    return JsonResponse(data)


def test_list_view(request):
    return render(request, 'tweets/test.html')