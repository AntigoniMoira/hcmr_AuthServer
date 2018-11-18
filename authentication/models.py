"""
All user's models.
"""
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    User's profile model.
    Otan diagrafei enas Auth User diagrafetai to UserProfile alla oxi to antistrofo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userPhone = models.CharField(max_length=30, default='None')
    birthDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    country = models.CharField(max_length=50, default='None')
    institution = models.CharField(max_length=100, default='None')
    description = models.CharField(max_length=500, default='None')
    PERMISSION_CHOICES = (
        ('U', 'User'),
        ('S', 'Staff'),
        ('A', 'Admin'),
    )
    permission = models.CharField(max_length=1, choices=PERMISSION_CHOICES, default='U')

    class Meta:
        verbose_name_plural = 'UserProfiles'
        ordering = ('country', )
        db_table = 'django\".\"userprofile'


    def __str__(self):
        return self.userPhone
