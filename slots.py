import random

symbols = {
    '🐷': 1.2,
    '🦆': 1.5,
    '🐙': 1.8,
    '🐕': 2,
    '🐈': 2.2,
    '🐯': 2.5
}


def spin_slots():
    return [[random.choice(list(symbols.keys())) for _ in range(3)] for _ in range(3)]


def check_adjacent(slots, line, column, symbol):
    adjacentes = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]
    sum_adjacent = 0
    for dx, dy in adjacentes:
        new_line, new_column = line + dx, column + dy
        if 0 <= new_line < 3 and 0 <= new_column < 3 and slots[new_line][new_column] == symbol:
            sum_adjacent += symbols[symbol]
    return sum_adjacent


def check_combinations(slots):
    total_prize = 0
    winner_symbol = None

    for i in range(3):
        if slots[i][0] == slots[i][1] == slots[i][2]:
            winner_symbol = slots[i][0]
            total_prize += symbols[winner_symbol]
            total_prize += check_adjacent(slots, i, 0, winner_symbol)
            total_prize += check_adjacent(slots, i, 1, winner_symbol)
            total_prize += check_adjacent(slots, i, 2, winner_symbol)

    for i in range(3):
        if slots[0][i] == slots[1][i] == slots[2][i]:
            winner_symbol = slots[0][i]
            total_prize += symbols[winner_symbol]
            total_prize += check_adjacent(slots, 0, i, winner_symbol)
            total_prize += check_adjacent(slots, 1, i, winner_symbol)
            total_prize += check_adjacent(slots, 2, i, winner_symbol)

    if slots[0][0] == slots[1][1] == slots[2][2]:
        winner_symbol = slots[0][0]
        total_prize += symbols[winner_symbol]
        total_prize += check_adjacent(slots, 0, 0, winner_symbol)
        total_prize += check_adjacent(slots, 1, 1, winner_symbol)
        total_prize += check_adjacent(slots, 2, 2, winner_symbol)

    if slots[0][2] == slots[1][1] == slots[2][0]:
        winner_symbol = slots[0][2]
        total_prize += symbols[winner_symbol]
        total_prize += check_adjacent(slots, 0, 2, winner_symbol)
        total_prize += check_adjacent(slots, 1, 1, winner_symbol)
        total_prize += check_adjacent(slots, 2, 0, winner_symbol)

    return total_prize


def play_slots(bet, balance):
    if bet > balance:
        return "Saldo insuficiente"

    slots = spin_slots()

    prize = check_combinations(slots) * bet
    if prize > 0:
        balance += prize

    else:
        balance -= bet

    return balance, round(prize, 2), slots