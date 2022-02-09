from typing import Optional
from functools import lru_cache


def english(n: int) -> int:
    return 1 if n != 1 else 0

def french(n: int) -> int:
    return 1 if n > 1 else 0

def russian(n: int) -> int:
    if n % 10 == 1 and n % 100 != 11:
        return 0
    return 1 if (n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20)) else 2

def czech(n: int) -> int:
    if n == 1:
        return 0
    return 1 if (n >= 2 and n <= 4) else 2

def polish(n: int) -> int:
    if n == 1:
        return 0
    return 1 if (n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20)) else 2

def icelandic(n: int) -> int:
    return 1 if (n % 10 != 1 or n % 100 == 11) else 0

def chinese(n: int) -> int:
    return 0

def arabic(n: int) -> int:
    if n >= 0 and n < 3:
      return int(n)
    if n % 100 <= 10:
      return 3
    if n >= 11 and n % 100 <= 99:
      return 4
    return 5

pluralRules = {
  'english': english,
  'french': french,
  'russian': russian,
  'czech': czech,
  'polish': polish,
  'icelandic': icelandic,
  'chinese': chinese,
  'arabic': arabic
}


mapping = {
  'english': ('da', 'de', 'en', 'es', 'fi', 'el', 'he', 'hu', 'it', 'nl', 'no', 'pt', 'sv', 'br'),
  'russian': ('hr', 'ru', 'uk', 'uz'),
  'chinese': ('fa', 'id', 'ja', 'ko', 'lo', 'ms', 'th', 'tr', 'zh', 'jp'),
  'french': ('fr', 'tl', 'pt-br'),
  'czech': ('cs', 'sk'),
  'icelandic': ('is'),
  'polish': ('pl'),
  'arabic': ('ar')
}

@lru_cache(maxsize=5)
def get_lang(code: str) -> Optional[str]:
    for key, values in mapping.items():
        if code in values:
            return(key)

    return None


def pluralize(code: str, number: int, forms) -> str:
    key = get_lang(code)

    if not key:
        raise ValueError(f'Unsupported language {code}')

    try:
        form = forms[pluralRules[key](number)]
    except (IndexError, TypeError):
        raise ValueError("Incorrect filling of pluralization forms")
        
    return form
