from django.db import models


class DatabaseList(models.Model):
    name = models.CharField(max_length=500)
    author = models.CharField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    full_desription = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class TableList(models.Model):
    name = models.CharField(max_length=500)
    db = models.ForeignKey(DatabaseList, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)


class ColumnList(models.Model):
    name = models.CharField(max_length=500)
    column_type = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    table = models.ForeignKey(TableList, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
