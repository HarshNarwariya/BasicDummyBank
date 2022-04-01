from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('index/', view=views.index, name="index"),
    path('make_transaction/', view=views.MakeTransaction.as_view(), name="make_transaction"),
    path('transactions/', view=views.RecordList.as_view(), name="transactions"),
    path('record/<int:pk>/update/', view=views.RecordUpdate.as_view(), name='record_update'),
    path('record/<int:pk>/delete/', view=views.RecordDelete.as_view(), name='record_delete'),
]