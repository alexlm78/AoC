"""
This is the solution for the first part problem of Advent of Code 2023 day 7.
author: Tim Eismar
github: https://github.com/teismar
date: 2023-12-07
"""


def file_to_list(filename: str) -> list:
    """
    Read the file and return a list of the strings of each line.
    :param filename:
    :return content:
    """
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def grade_hand(hand: str) -> int:
    """
    Grade the hand and return the value.
    1 = high card
    2 = one pair
    3 = two pairs
    4 = three of a kind
    5 = Full House
    6 = four of a kind
    7 = Five of a kind
    :param hand:
    :return value:
    """
    split_hand = [*hand]
    split_hand_set = list(set(split_hand))

    # Five of a kind
    if len(split_hand_set) == 1:
        return 7

    # Four of a kind or Full House
    if len(split_hand_set) == 2:
        if hand.count(split_hand_set[0]) == 3 or hand.count(split_hand_set[0]) == 2:
            return 5
        else:
            return 6

    # Three of a kind or two pairs
    if len(split_hand_set) == 3:
        if hand.count(split_hand_set[0]) == 3 or hand.count(split_hand_set[1]) == 3 or hand.count(split_hand_set[2]) == 3:
            return 4
        else:
            return 3

    # One pair or high card
    if len(split_hand_set) == 4:
        if hand.count(split_hand_set[0]) == 2 or hand.count(split_hand_set[1]) == 2 or hand.count(split_hand_set[2]) == 2 or hand.count(split_hand_set[3]) == 2:
            return 2
        else:
            return 1

    # High card
    return 1

def list_to_hands(content: list) -> list:
    """
    Convert the list of strings to a list of lists of hands.
    :param content:
    :return hands:
    """
    hands = []
    for line in content:
        temp = line.split(" ")
        hands.append((grade_hand(temp[0]),temp[0], temp[1]))
    return hands

def get_higher_card(card1: str, card2: str, card_values: dict) -> str:
    """
    Compare two cards and return the higher one.
    :param card1:
    :param card2:
    :param card_values:
    :return:
    """
    if card1[0] in card_values:
        card1_value = card_values[card1[0]]
    else:
        card1_value = int(card1[0])

    if card2[0] in card_values:
        card2_value = card_values[card2[0]]
    else:
        card2_value = int(card2[0])

    if card1_value > card2_value:
        return card1
    elif card1_value < card2_value:
        return card2
    else:
        return "equal"

def compare_hands(hand1: tuple, hand2: tuple) -> tuple:
    """
    Compare two hands and return the winner.
    :param hand1:
    :param hand2:
    :return winner:
    """
    for i in range(len(hand1[1])):
        higher = get_higher_card(hand1[1][i], hand2[1][i], {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14})
        if not higher == "equal":
            if higher == hand1[1][i]:
                return hand1
            else:
                return hand2
    return hand1

def get_total_winnings(hands: list) -> int:
    """
    Get the total winnings of the player.
    :param hands:
    :return total_winnings:
    """
    total_winnings = 0

    # Sort the hands after the function compare_hands which returns the winner
    for i in range(len(hands)):
        for j in range(i+1, len(hands)):
            if hands[i][0] == hands[j][0]:
                winner = compare_hands(hands[i], hands[j])
                if winner == hands[j]:
                    hands[i], hands[j] = hands[j], hands[i]

    # Reverse the list
    hands.reverse()

    for i in range(len(hands)):
        total_winnings += (i+1) * int(hands[i][2])

    return total_winnings
def main():
    """
    Main function
    """
    content = file_to_list("AoC_day07.input.txt")
    hands = list_to_hands(content)

    # Sort the hands after the grade
    hands.sort(key=lambda x: x[0], reverse=True)

    # Get the total winnings
    total_winnings = get_total_winnings(hands)

    print(f"The total winnings are: {total_winnings}")

if __name__ == "__main__":
    main()