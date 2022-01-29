# -*- encoding: utf-8 -*-
import sys

from pathlib import Path
from unittest import IsolatedAsyncioTestCase

sys.path.append("D:/Programming/TelegramBots/CubeBot")
from bot.types.Localization.I18nJSON import I18nJSON
from bot.data.config import I18nConfig


class TestTranslationFormat(IsolatedAsyncioTestCase):
    def setUp(self):
        i18n_config = I18nConfig(
            default_language='ru',
            locales_path=Path.joinpath(Path(__file__).parent, 'locales'),
            allow_missing_translation=True,
            allow_missing_placeholder=True,
            allow_missing_plural=True
        )

        self.i18n = I18nJSON(i18n_config)


    async def test_basic_translation(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('simple'), 'простой перевод')

    async def test_missing_translation(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('inexistent'), 'ru.inexistent')

    async def test_missing_translation_error(self):
        self.i18n.allow_missing_translation = False # type: ignore
        self.i18n.set_language('ru')
        with self.assertRaises(KeyError):
            await self.i18n.t('inexistent')

    async def test_locale_change(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('en')
        self.assertEqual(await self.i18n.t('simple'), 'simple translation')

    async def test_default_language(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('asd')
        self.assertEqual(await self.i18n.t('simple'), 'простой перевод')

    async def test_language_value_error(self):
        self.i18n.allow_missing_translation = False # type: ignore
        with self.assertRaises(ValueError):
            self.i18n.set_language('asd')

    async def test_basic_placeholder(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('hi', {"name": "User"}), 'Привет User!')

    async def test_missing_placehoder(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('hi'), 'Привет ${name}!')

    async def test_missing_placeholder_error(self):
        self.i18n.allow_missing_placeholder = False # type: ignore
        self.i18n.set_language('ru')
        with self.assertRaises(KeyError):
            await self.i18n.t('hi')

    async def test_pluralization(self):
        self.i18n.allow_missing_placeholder = True # type: ignore
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('plural', {"amount": 1}), 'У вас 1 яблоко')
        self.assertEqual(await self.i18n.t('plural', {"amount": 2}), 'У вас 2 яблока')
        self.assertEqual(await self.i18n.t('plural', {"amount": 0}), 'У вас 0 яблок')

    async def test_incorrect_key_for_pluralization(self):
        self.i18n.allow_missing_plural = True
        self.assertEqual(await self.i18n.t('simple', {"amount": 1}), 'ru.simple')

    async def test_incorrect_key_for_pluralization_error(self):
        self.i18n.allow_missing_plural = False
        with self.assertRaises(KeyError):
            await self.i18n.t('simple', {"amount": 1})

    async def test_incorrect_pluralization_filling(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.allow_missing_placeholder = True # type: ignore
        self.i18n.allow_missing_plural = False
        with self.assertRaises(ValueError):
            await self.i18n.t('incorrect_plural', {"amount": 0})

    async def test_multiline_string(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.allow_missing_placeholder = True # type: ignore
        self.i18n.allow_missing_plural = False
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('multiline_string'), "multiline\nstring")

    async def test_multiline_string_plural(self):
        self.i18n.allow_missing_translation = True # type: ignore
        self.i18n.allow_missing_placeholder = True # type: ignore
        self.i18n.allow_missing_plural = False
        self.i18n.set_language('ru')
        self.assertEqual(await self.i18n.t('multiline_string_plural', {"amount": 0}), "У вас\n0 мячей")