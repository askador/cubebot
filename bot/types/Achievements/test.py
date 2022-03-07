# type: ignore

# class A_SOME_LONG_CLASSNAME:
#     id = 1

# class B_SOME_LONG_CLASSNAME:
#     id = 2

# class C_SOME_LONG_CLASSNAME:
#     id = 2

# class D_SOME_LONG_CLASSNAME:
#     id = 2

# class E_SOME_LONG_CLASSNAME:
#     id = 5

# class F_SOME_LONG_CLASSNAME:
#     id = 6

# class G_SOME_LONG_CLASSNAME:
#     id = 7

# class H_SOME_LONG_CLASSNAME:
#     id = 8


# fake_all_achievements = {
#     'a': {
#         'b': {
#             'c': [A_SOME_LONG_CLASSNAME, B_SOME_LONG_CLASSNAME],
#             'c1': {
#                 'd': [C_SOME_LONG_CLASSNAME] 
#             }  
#         }, 
#         'b1': [D_SOME_LONG_CLASSNAME, E_SOME_LONG_CLASSNAME, F_SOME_LONG_CLASSNAME]
#     },
#     'a1': [G_SOME_LONG_CLASSNAME, H_SOME_LONG_CLASSNAME]
# }

def game_end():

    """ 
    but what if achievement depends on plays amount and money won  
    
    try to implement check achievement by multiple sections
    """
    check_achievements_by_sections(['game.plays', 'game.won'], user, message.answer)
    # check_achievements_by_section('game.plays', user)
    # check_achievements_by_section('game.won', user)
    check_achievements_by_section('game.lost', user)


def transfer_money():

    check_achievements_by_section('transfer.get', user)
    check_achievements_by_section('transfer.given', user)


