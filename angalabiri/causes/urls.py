from django.urls import path
from angalabiri.causes.views import CauseList, CauseDetail
app_name = "cause"
urlpatterns = [
    path('', CauseList.as_view(), name='list'),
    path('<slug>/', CauseDetail, name='detail'),
]
