
from django.contrib import admin
from django.urls import path,include

app = 'zebrashopapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('zebrashopapp.urls'))
]
