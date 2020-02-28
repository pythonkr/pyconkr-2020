from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import Banner


class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(FlatPage, FlatPageTranslationOptions)


class BannerTranslationOptions(TranslationOptions):
    fields = ('desc',)


translator.register(Banner, BannerTranslationOptions)
