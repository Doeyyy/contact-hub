from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_contacts, name='search'),
    path('create/', views.create_contact, name='create'),
    path('contact/<int:pk>/delete/', views.deletecontact, name='delete-contact'),
    # Note: the URL name must match exactly what you're using in your template
    # path("delete/<int:contact_id>/", views.delete_contact, name="delete_contact")
]
