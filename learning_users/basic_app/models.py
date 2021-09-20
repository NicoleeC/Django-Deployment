from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfoModel(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # each user has different name/email...
    #additinoal
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    # import pillow to handle pictures 
    def __str__(self):
        return self.user.username
