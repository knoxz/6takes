from models import *

cards = []
players = []

table = Table(4)


def create_player(player_number):
    for i in range(player_number):
        players.append(Player(i))


def reset_playing_cards():
    from game import debug_print
    cards.clear()
    for i in range(104):
        cards.append(Card(i + 1))
    if debug_print:
        print(f"Playing Cards: {cards}")
    random.shuffle(cards)


def reset_game():
    reset_playing_cards()
    for player in players:
        for _ in range(10):
            player.hand_cards.append(cards.pop())
    table.reset_table(cards)


def play_round():
    for i in range(10):
        from game import debug_print
        if debug_print:
            print(f"Round {i + 1}")
        for player in players:
            # This is random for now.
            player.select_playing_card()
        sorted_player_list = sorted(players, key=lambda player_sort: player_sort.played.number, reverse=True)
        if debug_print:
            print(f"Sorted Player List: {sorted_player_list}")
            table.print_table()
        for _ in range(len(players)):
            playing_player = sorted_player_list.pop()
            if debug_print:
                print(f"Player {playing_player.id} will play Card {playing_player.played} will be played!")
            penalty = table.play_card_onto_table(playing_player.played)
            for player in players:
                if player.id == playing_player.id:
                    player.played = None
                    player.penalty_sum = player.penalty_sum + penalty
            if debug_print:
                table.print_table()


def start_game():
    for _ in range(10):
        play_round()
