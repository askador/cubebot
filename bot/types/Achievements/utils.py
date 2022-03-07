import sys
sys.path.append("D:/Programming/TelegramBots/CubeBot")

from itertools import chain
from typing import Callable, Optional
from loguru import logger

from bot.db.models import Player

from Achievements import Achievement
from all_achievements import all_achievements



def parse_achievements_by_section(keys: str, resources: dict) -> "list[Achievement]":
    
    _keys = keys.split('.')

    def recursion(keys: list, resources):
        if not resources or not len(keys):
            return []
        if len(keys) == 1:
            return resources.get(keys[0], [])
        return recursion(keys[1:], resources.get(keys[0]))

    return recursion(_keys, resources)


def parse_achievements_by_sections(keys_list: "list[str]", resources: dict) -> "list[Achievement]":
    
    _keys = [keys.split('.') for keys in keys_list]

    def recursion(keys: list, resources):
        if not resources or not len(keys):
            return []
        if len(keys) == 1:
            return resources.get(keys[0], [])
        return recursion(keys[1:], resources.get(keys[0]))

    res = [recursion(keys, resources) for keys in _keys]
    return(list(chain.from_iterable(res)))


def get_achievement_by_section_and_id(section: str, id: int) -> Optional[Achievement]:
    d = parse_achievements_by_section(section, all_achievements)

    if not d:
        return None

    for achievement in d:
        if achievement.id == id:
            return achievement
    
    return None
 

def check_achievements_by_sections(sections: "list[str]", Player: Player, notify: Callable) -> None:
    """
    one level up parent of sections should be the same
    e.g. '`game.plays`' and '`game.won`' have same parent '`game`'
    """
    achievements = parse_achievements_by_sections(sections, all_achievements)
    process_check_achievements(sections, achievements, Player, notify)


def check_achievements_by_section(section: str, Player: Player, notify: Callable) -> None:
    """
    :param section: achievements section. 
    Leveled sections use with delimeter '`.`', e.g. '`achievement.section.name`'

    :param Player: Player Model object
    """
    achievements = parse_achievements_by_section(section, all_achievements)
    process_check_achievements(list(section), achievements, Player, notify)
    

def process_check_achievements(
    sections: "list[str]",
    achievements: Optional[list],
    Player: Player, 
    notify: Callable
) -> None:
    achieved_achievements = Player.get_achievements(sections)
    if not achievements:
        return 
    achieved_achievements_ids = [achievement.split('.')[-1] for achievement in achieved_achievements]

    # symetric difference
    not_achieved_achievements_ids = set(achievements) ^ set(achieved_achievements_ids)

    for achievement_id in not_achieved_achievements_ids:
        achievement = achievements[achievement_id]
        unlock = achievement.check(Player, achieved_achievements_ids) 
        if unlock:
            achievement.on_unlock()
            notify(achievement.unlock_message)


def check_if_all_ids_are_unique() -> None:
    logger.info("Checking ids of achievements")

    indexes = {}
    
    def recursion(recources) -> None:
        if type(recources) is list:
            for ach in recources:
                ach_id = ach.id
                ach_name = ach.__class__.__name__
                if ach_id in indexes:
                    logger.error(f"object {repr(ach_name)} duplicates id {ach_id}")
                indexes.setdefault(ach_id, []).append(ach_name)
            return 
        for section in recources:
            recursion(recources.get(section))

    recursion(all_achievements)

