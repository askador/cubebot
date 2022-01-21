import json
import sys

from string import Template
from dataclasses import dataclass
from typing import Dict, Optional, List, Any

from pathlib import Path
from pluralize import pluralize

sys.path.append("D:/Programming/TelegramBots/CubeBot")
from bot.data.config import I18nConfig

# @dataclass
# class I18nConfig:
#     default_language: str
#     locales_path: Path
#     allow_missing_translation: bool
#     allow_missing_placeholder: bool
#     allow_missing_plural: bool

class I18nJSON:

    def __init__(self, config: I18nConfig):
        self.file_extension            = 'json'
        self.locales_path: Path        = config.locales_path
        self.default_language          = config.default_language
        self.language_key              = self.default_language
        self.allow_missing_translation = config.allow_missing_translation,
        self.allow_missing_placeholder = config.allow_missing_placeholder,
        self.allow_missing_plural      = config.allow_missing_plural

        self.locales = {}
        self.load_locales()

    def load_locales(self) -> None:
        locale_files = self.locales_path.glob(f'*.{self.file_extension}')
        for file in locale_files:
            if file.stat().st_size == 0: continue

            with open(file, 'r', encoding='utf-8') as locale:
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

    @staticmethod
    async def get_template(keys: list, resources: Optional[Dict[str, Any]]) -> Optional[str]:
        if not resources or not len(keys) or type(resources) is not dict:
            return
        if len(keys) == 1:
            return resources.get(keys[0])
        return str(await I18nJSON.get_template(keys[1:], resources.get(keys[0], {})))

    @staticmethod
    async def get_plural_forms(keys: list, resources: Optional[Dict[str, Any]]) -> Optional[List[str]]:
        if not resources or not len(keys):
            return
        if len(keys) == 1:
            return resources.get(keys[0])
        return await I18nJSON.get_plural_forms(keys[1:], resources.get(keys[0])) # type: ignore


    async def t(self, keys: str, template_data: dict={}) -> str:
        resources: Optional[Dict[str, Any]] = self.locales.get(self.language_key)

        if not "amount" in template_data:
            template = await self.get_template(keys.split('.'), resources)
        else:    
            try:
                forms = await self.get_plural_forms(f"{keys}.forms".split('.'), resources)
                plural_form = await pluralize(self.language_key, template_data.get("amount"), forms) #type: ignore
                template = await self.get_template(f"{keys}.template".split('.'), resources)
                template_data['form'] = plural_form
            except AttributeError:
                if self.allow_missing_plural:
                    template = f"{self.language_key}.{keys}"
                else:
                    raise KeyError(
                        f"Plural forms not defined for key {self.language_key}.{keys}"
                    )
            except ValueError:
                if self.allow_missing_plural:
                    template = f"{self.language_key}.{keys}"
                else:
                    raise ValueError(
                        f"Incorrect filling of pluralization forms for {self.language_key}.{keys}"
                    )

        if not template and self.allow_missing_translation:
            template = f"{self.language_key}.{keys}"

        if not template and not self.allow_missing_translation:
            raise KeyError(f'{self.language_key}.{keys} not found')
        
        formatter = TranslationFormatter(template, {                    #type: ignore
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
        else:
            return self.substitute(**kwargs)
