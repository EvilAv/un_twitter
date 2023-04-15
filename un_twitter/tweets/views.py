from django.shortcuts import render
from django.http import JsonResponse
from .models import Test
from .forms import TestForm


# Create your views here.
def home_page(request):
    return render(request, 'tweets/index.html')


def test_view(request, start):
    # maybe it should be prohibited to enter json part but i am not sure
    if start >= len(Test.objects.all()):
        return JsonResponse({})
    elif start + 40 >= len(Test.objects.all()):
        end = len(Test.objects.all())
    else:
        end = start + 40
    test_list = Test.objects.all()[start:end]
    json_list = [i.serialize() for i in test_list]
    data = {
        'name': 'aaaa',
        'data': json_list,
    }
    return JsonResponse(data)


def test_list_view(request):
    return render(request, 'tweets/test.html')


def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if form.is_valid():
            test_tweet = form.save()
            test_tweet.save()
            if is_ajax:
                return JsonResponse(test_tweet.serialize(), status=201)
        if form.errors:
            if is_ajax:
                return JsonResponse(form.errors, status=400)

    else:
        form = TestForm()

    return render(request, 'tweets/tweet-create.html', {'form': form})