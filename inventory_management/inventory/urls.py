from django.urls import path
from .views import create_item, get_item, update_item, delete_item

urlpatterns = [
    path('items/', create_item, name='create_item'),
    path('items/<int:item_id>/', get_item, name='get_item'),
    path('items/<int:item_id>/', update_item, name='update_item'),
    path('items/<int:item_id>/', delete_item, name='delete_item'),
]
