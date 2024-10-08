from django.db import models

class Profile(models.Model):
    ''' encapsulates the idea of a user profile '''

    # data attributes
    first_name = models.TextField(blank = False)
    last_name = models.TextField(blank = False)
    city = models.TextField(blank = False)
    email_address = models.TextField(blank = False)
    profile_img_url = models.TextField(blank = False)


