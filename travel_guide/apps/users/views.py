import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, ProfileImage, Car


# Create your views here.
def user(request):
    users = User.objects.raw("SELECT * FROM users_user")

    # usrs = User.objects.values()
    # data = list(usrs)

    # Convert the queryset to a list of dictionaries
    data = []
    for u in users:
        data.append({
            'id': u.id,
            'name': u.name,
            'email': u.email,
        })

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
            cars_data = data.get("cars", [])  # Expecting a list of car models

            # Handle single car model input
            if not cars_data:
                single_car = data.get("car")
                if single_car:
                    cars_data = [single_car]

            if img_data:
                profile_image, created = ProfileImage.objects.get_or_create(image=img_data)
            else:
                profile_image = ProfileImage.objects.create(image="NO IMAGE")

            # Create the User instance
            new_user = User.objects.create(
                name=name,
                email=email,
                password=password,
                img=profile_image
            )

            # Associate Car instances with the user
            car_objects = []
            for car_model in cars_data:
                car, created = Car.objects.get_or_create(model=car_model)
                car_objects.append(car)

            # Associate Car instances with the user using set()
            new_user.cars.set(car_objects)

            return JsonResponse({
                'success': True,
                'user': {
                    'id': new_user.id,
                    'name': new_user.name,
                    'email': new_user.email,
                    'img': new_user.img.image,
                    'cars': [car.model for car in new_user.cars.all()]
                }
            }, status=201)
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
