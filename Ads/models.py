from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import reverse


class Category(models.Model):
    CHOICE_CATEGORY = (
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Traders', 'Торговцы'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potions', 'Зельевары'),
        ('Speell masters', 'Мастера заклинаний'),
    )

    name_category = models.CharField(max_length=16, choices=CHOICE_CATEGORY, default='Questgivers', unique=True)

    def __str__(self):
        return f'{self.name_category}'


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_creation = models.DateTimeField(auto_now_add=True)
    category_ad = models.ManyToManyField(Category, through='AdCategory')
    title_ad = models.CharField(max_length=128)
    content_ad = RichTextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title_ad}'

    def get_absolute_url(self):
        return reverse('ad_details', args=[str(self.id)])


class AdCategory(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text_response = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        slice_response = self.text_response[:60]

        return f'{self.user}: {slice_response}'

