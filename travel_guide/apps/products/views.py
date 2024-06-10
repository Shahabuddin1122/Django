import json
from datetime import datetime

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.
def get_all_product(request):
    products = product.objects.values()
    return JsonResponse({"data": list(products)})


@csrf_exempt
def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        name = data.get("name")
        price = data.get("price")
        description = data.get("description")
        category = data.get("category")
        subcategory = data.get("subcategory")
        image = data.get("image")
        new_product = product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            subcategory=subcategory,
            image=image
        )
        return JsonResponse({"data": model_to_dict(new_product)})
    else:
        return JsonResponse({"error": "POST method not supported"})
