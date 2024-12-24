from django.db import models


class Theme(models.Model):
    category = models.TextField(max_length=20)
    start = models.TextField(max_length=100)
    final = models.TextField(max_length=100)

    class Meta:
        db_table = 'theme'

    def __str__(self):
        return f"{self.start}\t{self.final}"
