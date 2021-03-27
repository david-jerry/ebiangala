from django.urls import path

from .views import (
    PostList,
    PostDetail,
    TagDetail
)

app_name = "blog"
urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('<slug>/', PostDetail, name='detail'),
    path('tag/<slug>/', TagDetail.as_view(), name='tag'),
]
