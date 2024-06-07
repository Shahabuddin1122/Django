from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import User


# Create your views here.
def user(request):
    obj = User.objects.values()
    data = list(obj)
    return JsonResponse({'users': data})
