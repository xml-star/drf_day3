from django.urls import path
from api import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("v2/books/", views.BookAPIViewV2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIViewV2.as_view()),

    path("gen/", views.BookGenericAPIView.as_view()),
    path("gen/<str:id>/", views.BookGenericAPIView.as_view()),

    path("v3/gen/", views.BookGenericAPIViewV3.as_view()),
    path("v3/gen/<str:id>/", views.BookGenericAPIViewV3.as_view()),

    path("register/", views.UserViewSetView.as_view({"post": "user_register"})),
    path("login/", views.UserViewSetView.as_view({"post": "user_login"})),


]