from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from sorl.thumbnail import ImageField as SorlImageField
User = get_user_model()


def profile_image(instance, filename):
    return f'profile/{instance.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    image = SorlImageField(upload_to=profile_image, null=True, blank=True)
    bio = models.TextField(max_length=4000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    @property
    def is_empty(self):
        return self.name == '' or self.phone is None or self.organization is None or self.bio is None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
