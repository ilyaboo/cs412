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
    
    def get_friends(self):
        ''' accessor method that obtains all the friends of the profile '''

        tmp = list(Friend.objects.filter(profile1 = self) | Friend.objects.filter(profile2 = self))
        return [val.profile1 if val.profile1 != self else val.profile2 for val in tmp]

class StatusMessage(models.Model):
    ''' encapsulates the idea of a user's status message '''

    # data attributes
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank = False)
    profile = models.ForeignKey("Profile", on_delete = models.CASCADE)

    def __str__(self):
        ''' returns a string representation of this StatusMessage object '''
        return f' Published at {self.timestamp} by {self.profile}: {self.message}'
    
    def get_images(self):
        ''' accessor method to get all images associated with a status message '''

        return Image.objects.filter(status_message = self)
    
class Image(models.Model):
    ''' encapsulates the idea of an image '''

    # data attributes
    image = models.ImageField(blank = False)
    status_message = models.ForeignKey("StatusMessage", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        ''' returns a string representation of this StatusMessage object '''
        return f' Image for {self.status_message.profile}\'s post posted at {self.timestamp}'
    
class Friend(models.Model):
    ''' encapsulates the idea of a friend relation between two users '''

    profile1 = models.ForeignKey("Profile", on_delete = models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete = models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'