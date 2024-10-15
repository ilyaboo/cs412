from django.db import models
from django.urls import reverse

class Profile(models.Model):
    ''' encapsulates the idea of a user profile '''

    # data attributes
    first_name = models.TextField(blank = False)
    last_name = models.TextField(blank = False)
    city = models.TextField(blank = False)
    email_address = models.TextField(blank = False)
    profile_img_url = models.TextField(blank = False)

    def __str__(self):
        ''' returns a string representation of this Profile object '''
        return f'{self.first_name} {self.last_name} from {self.city}'

    def get_status_messages(self):
        ''' accessor method that obtains all the status messages of the profile '''

        return StatusMessage.objects.filter(profile = self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    ''' encapsulates the idea of a user's status message '''

    # data attributes
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank = False)
    profile = models.ForeignKey("Profile", on_delete = models.CASCADE)

    def __str__(self):
        ''' returns a string representation of this StatusMessage object '''
        return f' Published at {self.timestamp} by {self.profile}: {self.message}'
