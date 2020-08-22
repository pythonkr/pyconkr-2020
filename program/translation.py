from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import (
    ProgramCategory, ProgramTime,
)


class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ProgramCategory, ProgramCategoryTranslationOptions)


class ProgramTimeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ProgramTime, ProgramTimeTranslationOptions)

