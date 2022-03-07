from __future__ import annotations
from typing import Callable
from abc import abstractmethod, ABC

import sys

sys.path.append("D:/Programming/TelegramBots/CubeBot")
from bot.db.models import Player

class Achievement(ABC):
    id: int
    title: str
    description: str = ''
    award: int = 0

    @abstractmethod
    def __init__(self, on_unlock: Callable[[Player], None]) -> None:
        self.dependencies: list = []
        self.on_unlock: Callable[[Player], None] = on_unlock

        if not hasattr(self, 'id'):
            raise AttributeError(f"type '{self.__class__.__name__}' has no attribute 'id'")
        if not hasattr(self, 'title'):
            raise AttributeError(f"type '{self.__class__.__name__}' has no attribute 'title'")

    @property
    def unlock_message(self) -> str:
        return f'Achievement Unlocked: {self.title}'

    @abstractmethod
    def _check_condition(self, user: Player, achieved_achievements_ids: list[str]) -> bool:
        """ 
        When implemented, specifies whether or not this Achievement
        should be unlocked based on the given achieved achievements id. Must be
        implemented for every subclass of Achievement.
        
        :param user: Player Model object
        :param achieved_achievements_ids: list of achievements ids

        :return bool: True if this Achievement can be unlocked

        :raises NotImplementedError: If not implemented in subclasses
        """
        raise NotImplementedError(
             'Must implement _check_condition method for '
            f'class {self.__class__.__name__}')

    def check(self, user: Player, achieved_achievements_ids: list[str]):
        return self._check_condition(user, achieved_achievements_ids)


class PlayFirstGame(Achievement):
    id = 1
    title = "Новобранец"
    description = "Сыграйте одну игру"
    award = 1000

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def _check_condition(self, user: Player, achieved_achievements_ids: list[str]=None):
        if user.plays == 0:
            return True
        return False


class Play10TimesAchievement(Achievement):
    id = 2
    title = "Исследователь"
    description = "Сыграйте 10 раз"
    award = 1500

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dependencies = [PlayFirstGame]

    def _check_condition(self, user: Player, achieved_achievements_ids: list[str]):
        # check if all dependent achievements is achieved
        is_dependencies_satisfied = all(
            ach.id in achieved_achievements_ids for ach in self.dependencies)

        if is_dependencies_satisfied and user.plays < 5:
            return True
        
        return False


class Play100TimesAchievement(Achievement):
    id = 3
    title = "Исследователь"
    description = "Сыграйте 100 раз"
    award = 12000

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dependencies = [PlayFirstGame, Play10TimesAchievement]

    def _check_condition(self, user: Player, achieved_achievements_ids: list[str]):
        # check if all dependent achievements is achieved
        is_dependencies_satisfied = all(
            ach.id in achieved_achievements_ids for ach in self.dependencies)

        if is_dependencies_satisfied and user.plays < 100:
            return True
        
        return False