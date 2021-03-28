from django.urls import path

from .views import (
    SuggestionList,
    SuggestionDetail,
    SuggestionCreate,
)

app_name = "suggestion"
urlpatterns = [
    path('', SuggestionList.as_view(), name='list'),
    path('create', SuggestionCreate.as_view(), name='create'),
    path('<slug>/', SuggestionDetail.as_view(), name='detail'),
]
