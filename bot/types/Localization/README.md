# Localization rules
- For default forms use template:
```json
{
    "<your command>": "<your template>"
}
```
- For plural forms use template: 
```json 
{ 
    "<your command>": {
        "template": "<your template>",
        "forms": [<your forms>]
    }
}
```
- For multiline forms use template: 
```json 
{ 
    "<your command>": [
        "<your\n",
        "template>"
    ]
}
```
- Order is important.
[one, many, ...]

## Example
en.json
```json
{
    "greeting": "Hello ${name}!",
    "basket": {
        "template": "You have ${amount} ${form} in your basket",
        "forms": ["apple", "apples"]
    },
    "present": [
        "You have resieved\n",
        "COOL PRESENT"
    ]
}
```
```python
from bot.types.Localization import I18nJSON
from bot.data.config import I18nConfig

i18n = I18nJSON(config: I18nConfig)

async def main():
    print(i18n.t('greeting', {name="User"}))
    print(i18n.t('basket', {amount=2}))
    print(i18n.t('present'))
```
```bash
Output: Hello User!
Output: You have 2 apples in yor basket
Output: You have resieved
...     COOL PRESENT
```
