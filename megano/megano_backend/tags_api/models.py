from django.db import models

class Tags(models.Model):
    name = models.CharField(max_length=128)
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        
    def __str__(self):
        return self.name