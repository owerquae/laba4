from django.db import models

class Record(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name