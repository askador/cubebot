from Achievements import PlayFirstGame, Play10TimesAchievement

all_achievements = {
    "game": {
        'plays': [
            PlayFirstGame(on_unlock=""),
            Play10TimesAchievement(on_unlock="")
        ],
        'won': []
    },
    "transfer": []
}
