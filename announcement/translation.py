from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Announcement
)


class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Announcement, AnnouncementTranslationOptions)
