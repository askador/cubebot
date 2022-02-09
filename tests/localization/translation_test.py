# -*- encoding: utf-8 -*-
import sys

from pathlib import Path
from unittest import TestCase

sys.path.append("D:/Programming/TelegramBots/CubeBot")
from bot.types.Localization import I18nJSON
from bot.data.config import I18nConfig


class TestTranslationFormat(TestCase):
    def setUp(self):
        self.config = I18nConfig(
            default_language='ru',
            locales_path=Path.joinpath(Path(__file__).parent, 'locales'),
            use_default_language_on_missing=True,
            allow_missing_translation=True,
            allow_missing_placeholder=True,
            allow_missing_plural=True
        )


    def test_basic_translation(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('simple'), 'простой перевод')

    def test_missing_translation(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('inexistent'), 'ru.inexistent')

    def test_missing_translation_error(self):
        i18n = I18nJSON(self.config)
        i18n.allow_missing_translation = False
        i18n.set_language('ru')
        with self.assertRaises(KeyError):
            i18n.t('inexistent')

    def test_locale_change(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('en')
        self.assertEqual(i18n.t('simple'), 'simple translation')

    def test_default_language(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('asd')
        self.assertEqual(i18n.t('simple'), 'простой перевод')

    def test_use_default_language_on_missing(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('en')
        self.assertEqual(i18n.t('use_default_language'), 'дефолтный перевод')

    def test_language_value_error(self):
        i18n = I18nJSON(self.config)
        i18n.allow_missing_translation = False
        with self.assertRaises(ValueError):
            i18n.set_language('asd')

    def test_basic_placeholder(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('hi', {"name": "User"}), 'Привет User!')

    def test_missing_placehoder(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('hi'), 'Привет ${name}!')

    def test_missing_placeholder_error(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        i18n.allow_missing_placeholder = False
        with self.assertRaises(KeyError):
            i18n.t('hi')

    def test_pluralization(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('plural', amount=1), 'У вас 1 яблоко')
        self.assertEqual(i18n.t('plural', amount=2), 'У вас 2 яблока')
        self.assertEqual(i18n.t('plural', amount=0), 'У вас 0 яблок')

    def test_incorrect_key_for_pluralization(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        i18n.allow_missing_plural = True
        self.assertEqual(i18n.t('simple', amount=1), 'ru.simple')

    def test_incorrect_pluralization_error(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        i18n.allow_missing_plural = False
        with self.assertRaises(ValueError):
            i18n.t('simple', amount=1)

    def test_plural_use_default_language_on_missing(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('en')
        self.assertEqual(i18n.t('plural_use_default_language', amount=1), 'У вас 1 яблоко')

    def test_multiline_string(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('multiline_string'), "some\n\nmultiline\nstring")

    def test_multiline_string_plural(self):
        i18n = I18nJSON(self.config)
        i18n.set_language('ru')
        self.assertEqual(i18n.t('multiline_string_plural', amount=0), "У вас\n0 мячей")