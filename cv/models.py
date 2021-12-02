from django.core.validators import FileExtensionValidator
from django.db import models

class Image(models.Model):
    img = models.ImageField(
        upload_to='image/',
        verbose_name='画像',
        validators=[FileExtensionValidator(['jpg', 'jpeg'])],
    )
