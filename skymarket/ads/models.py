from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from users.models import User


class Ad(models.Model):
    image = models.ImageField(default=None, null=True, blank=True, upload_to='media/')
    title = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5)])
    price = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
