from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage
from .models import (
    Room,
    ProgramCategory, ProgramTime,
    Speaker, Program,
)


class RoomTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


translator.register(Room, RoomTranslationOptions)


class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ProgramCategory, ProgramCategoryTranslationOptions)


class ProgramTimeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ProgramTime, ProgramTimeTranslationOptions)


class SpeakerTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


translator.register(Speaker, SpeakerTranslationOptions)


class ProgramTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


translator.register(Program, ProgramTranslationOptions)
