import json

from pathlib import Path
from string import Template
from typing import Optional, Tuple

from bot.types.Localization.pluralize import pluralize
from bot.types.Localization import utils
from bot.data.config import I18nConfig


class I18nJSON:

    def __init__(self, config: I18nConfig):
        self.file_extension                  = 'json'
        self.encoding                        = 'utf-8'
        self.locales_path: Path              = config.locales_path
        self.default_language                = config.default_language
        self.use_default_language_on_missing = config.use_default_language_on_missing
        self.allow_missing_translation       = config.allow_missing_translation
        self.allow_missing_placeholder       = config.allow_missing_placeholder
        self.allow_missing_plural            = config.allow_missing_plural

        self.locales = {}
        self.load_locales()


    def load_locales(self) -> None:
        locale_files = self.locales_path.glob(f'*.{self.file_extension}')
        for file in locale_files:
            if file.stat().st_size == 0: 
                continue

            with open(file, 'r', encoding=self.encoding) as locale:
                self.locales.update({file.stem: json.load(locale)})

    def get_locales(self) -> dict:
        return self.locales


    def set_language(self, language_key: str) -> None:
        if language_key in self.locales:
            self.language_key = language_key
            return
        if self.allow_missing_translation:
            self.language_key = self.default_language
            return 
        raise ValueError(f"No such language: {repr(language_key)}")


    def get_language(self) -> str:
        return self.language_key


    def pluralize(self, keys: str, amount, resources: Optional[dict]) -> Tuple[Optional[str], str]:
        plural_form = ''
        template: Optional[str] = None

        forms = utils.get(f"{keys}.forms", resources)

        if not forms and self.use_default_language_on_missing:
            resources = self.locales.get(self.default_language)
            forms = utils.get(f"{keys}.forms", resources)
            self.language_key = self.default_language
        
        if not forms and self.allow_missing_plural:
            template = f"{self.language_key}.{keys}"
            return template, plural_form

        if not forms and not self.allow_missing_plural:
            raise ValueError(f"Incorrect filling of pluralization forms for {self.language_key}.{keys}")

        plural_form = pluralize(self.language_key, amount, forms)
        template: Optional[str] = utils.get(f"{keys}.template", resources)

        return template, plural_form


    def t(self, keys: str, template_data: dict = None, **kwargs):
        resources: Optional[dict] = self.locales.get(self.language_key)

        if template_data is None:
            template_data = {}

        template: Optional[str] = utils.get(keys, resources)   
        if "amount" in kwargs:
            template, form = self.pluralize(keys, kwargs.get('amount'), resources)
            template_data['form'] = form
            if not template_data.get('amount'):
                template_data['amount'] = kwargs.get('amount')

        if not template and self.use_default_language_on_missing:
            resources = self.locales.get(self.default_language)
            template = utils.get(keys, resources)  

        if not template and self.allow_missing_translation:
            template = f"{self.language_key}.{keys}"

        if not template and not self.allow_missing_translation:
            raise KeyError(f'{self.language_key}.{keys} not found')

        if type(template) is list:
            template = ''.join(template)

        formatter = TranslationFormatter(template, {  # type: ignore
            "allow_missing_placeholder": self.allow_missing_placeholder
        })
        return formatter.format(**template_data)


class TranslationFormatter(Template):

    def __init__(self, template: str, config):
        self.allow_missing_placeholder = config.get('allow_missing_placeholder')
        super(TranslationFormatter, self).__init__(template)

    def format(self, **kwargs) -> str:
        if self.allow_missing_placeholder:
            return self.safe_substitute(**kwargs)
            
        return self.substitute(**kwargs)
