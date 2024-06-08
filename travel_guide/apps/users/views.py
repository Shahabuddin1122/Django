import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, ProfileImage


# Create your views here.
def user(request):
    obj = User.objects.values()
    data = list(obj)
    return JsonResponse({'users': data})


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            img_data = data.get("img")

            # If `img` is provided, find or create the ProfileImage
            if img_data:
                profile_image, created = ProfileImage.objects.get_or_create(image=img_data)
            else:
                # If no `img` is provided, you can create a default one or handle as needed
                profile_image = ProfileImage.objects.create(image="NO IMAGE")

            # Create the User instance
            new_user = User.objects.create(
                name=name,
                email=email,
                password=password,
                img=profile_image
            )

            return JsonResponse({'success': True,
                                 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email,
                                          'img': new_user.img.image}}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)


def get_individual_user(request, name):
    one_user = User.objects.get(name__endswith=name)
    data = {
        'id': one_user.id,
        'name': one_user.name,
        'email': one_user.email,
        'password': one_user.password,
        'img': one_user.img.image
    }
    return JsonResponse({'user': data})
