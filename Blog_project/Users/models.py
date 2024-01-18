from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()
        """ 
        This method is used to resize the image to 300*300
        """
        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            



    """ Comments """
    """ OneToOneField is a field that links to another model, but only one instance of the other model is linked to each instance of the first model.  """
    """ on_delete=models.CASCADE means that if the User is deleted, then the Profile will also be deleted. """