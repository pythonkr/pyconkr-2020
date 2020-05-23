from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=500)
    desc = models.TextField(null=True, blank=True)

    announce_after = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def at(self):
        return self.announce_after if self.announce_after else self.created

    def __str__(self):
        return self.title
