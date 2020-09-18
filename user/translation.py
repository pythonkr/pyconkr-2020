from modeltranslation.translator import translator, TranslationOptions
from .models import Profile, Staff


class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'bio',)


translator.register(Profile, ProfileTranslationOptions)


class StaffTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Staff, StaffTranslationOptions)
