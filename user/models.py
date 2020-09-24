from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from sorl.thumbnail import ImageField as SorlImageField
from django.utils.translation import ugettext as _

User = get_user_model()


def profile_image(instance, filename):
    return f'profile/{instance.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True, help_text=_(
        '여기에 기입한 조직 이름이 행사 당일 이름표에 표시됩니다.'))
    image_ori = SorlImageField(upload_to=profile_image, null=True, blank=True,
                               help_text=_('사용자 사진 원본'))
    image_small = SorlImageField(upload_to=profile_image, null=True, blank=True,
                                 help_text=_('사용자 사진 축소본'))
    bio = models.TextField(max_length=4000, null=True, blank=True,
                           help_text=_('이 내용이 개인 후원자 목록에 노출됩니다. 변경 사항은 최대 60분 이내에 적용됩니다.'))
    user_code = models.CharField(max_length=20, null=True, blank=True)
    agreement_receive_advertising_info = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('profile')

    @property
    def is_empty(self):
        return self.name == '' or self.phone is None or self.organization is None or self.bio is None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Staff(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    phrase = models.TextField(max_length=1000, null=True, blank=True)
    image = SorlImageField(upload_to=profile_image, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
