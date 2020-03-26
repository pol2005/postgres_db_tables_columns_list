from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from .models import DatabaseList, TableList, ColumnList


class DatabaseListListView(ListView):
    model = DatabaseList
    context_object_name = 'visitors_list'
    template_name = 'crud/database-list.html'


class DatabaseListDetailView(DetailView):
    model = DatabaseList
    context_object_name = 'db_detail'
    template_name = 'crud/database-detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DatabaseListDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['table_list'] = TableList.objects.filter(db=self.object)
        return context


class DatabaseListUpdateView(UpdateView):
    model = DatabaseList
    fields = ['name', 'author', 'subject', 'keywords', 'description', 'full_desription',]
    template_name = 'crud/database_update_form.html'

    def get_success_url(self):
        return reverse('db-detail', kwargs={'pk': self.object.id})


class ColumnListUpdateView(UpdateView):
    model = ColumnList
    fields = ['description']
    # if you want more fields, just add  'name' and/or 'column_type' like below and restart the server
    # fields = ['name', 'column_type', 'description']
    template_name = 'crud/column_update_form.html'

    def get_success_url(self):
        c_id = self.object.id
        t_id = ColumnList.objects.get(pk=c_id)
        d_id = TableList.objects.get(pk=t_id.table_id)
        return reverse('db-detail', kwargs={'pk': d_id.db_id})


