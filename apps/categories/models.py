from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name_plural = 'categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'],
                name='unique_category_name_per_user'
            )
        ]

    def __str__(self):
        return self.name
    
    @property
    def is_system(self):
        return self.user is None
        

