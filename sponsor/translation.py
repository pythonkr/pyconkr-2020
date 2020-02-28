from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import (
    Sponsor, SponsorLevel,
)


class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


translator.register(Sponsor, SponsorTranslationOptions)


class SponsorLevelTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


translator.register(SponsorLevel, SponsorLevelTranslationOptions)
