from django.urls import path
from .views import DatabaseListDetailView, DatabaseListListView, DatabaseListUpdateView, ColumnListUpdateView

urlpatterns = [
    path('', DatabaseListListView.as_view(), name='db-list'),
    path('database/<int:pk>/', DatabaseListDetailView.as_view(), name='db-detail'),
    path('column/<int:pk>/edit', ColumnListUpdateView.as_view(), name='column-update'),
    path('database/<int:pk>/edit', DatabaseListUpdateView.as_view(), name='db-update'),
]
