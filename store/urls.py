
from django.urls.conf import path
from . import views

urlpatterns = [


    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update-item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

]
