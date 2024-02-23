from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Rating(models.Model):
    score = models.PositiveIntegerField(
        default = 0,
        validators =[MaxValueValidator(5), MinValueValidator(0)]
    )
    comment = models.TextField(blank=True, null= True)  
    
    def __str__(self):
        return "{}: {}".format(self.score, self.comment)
        
    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            score = self.score
            comment = self.comment