from django.db import models

class Storage(models.Model):
    address = models.CharField(max_length=255, verbose_name='Адрес склада')
    company = models.OneToOneField(
        'authenticate.Company',
        on_delete=models.SET_NULL,
        null=True,
        related_name='storage',
        verbose_name='Компания',
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name='Склад'
        verbose_name_plural='Склады'

