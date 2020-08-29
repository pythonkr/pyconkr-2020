from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=500,
                          help_text="공지 내용을 볼 수 있는 링크입니다. 주로 페이스북 공지 링크가 들어가게 됩니다.")
    active = models.BooleanField(default=True,
                                 help_text='True면 공지사항이 노출됩니다.')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
