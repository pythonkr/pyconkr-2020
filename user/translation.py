from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Profile
)


class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'bio',)


translator.register(Profile, ProfileTranslationOptions)
