from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import ProgramCategory


class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ProgramCategory, ProgramCategoryTranslationOptions)
