from django.urls import path
from apps.products import views
urlpatterns = [
    path("products/", views.get_all_product),
    path("add-product", views.add_product,)
]
