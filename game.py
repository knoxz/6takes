# Settings
from game_functions import *

player_number = 6

create_player(player_number)
reset_game()
play_round()

# print(f"Players: {players}")
for player in players:
    print(f"Player {player.id + 1} has {player.penalty_sum}")

print(f"Cards({len(cards)}) not used: {cards}")
