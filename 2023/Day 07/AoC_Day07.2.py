"""
This is the solution for the second part problem of Advent of Code 2023 day 7.
author: Tim Eismar
github: https://github.com/teismar
date: 2023-12-07
"""

from AoC_Day07 import file_to_list, grade_hand, get_higher_card

cache = {}

def list_to_hands(content: list) -> list:
    """
    Convert the list of strings to a list of lists of hands.
    :param content:
    :return hands:
    """
    hands = []
    for line in content:
        temp = line.split(" ")
        if 'J' not in temp[0]:
            hands.append((grade_hand(temp[0]), temp[0], temp[1]))
        else:
            # Start searching for the highest grade by replacing every J with a number
            possible_cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
            j_count = temp[0].count('J')
            possibilities = len(possible_cards) ** j_count
            if temp[0] in cache:
                current_highest_grade = cache[temp[0]]
            else:
                current_highest_grade = grade_hand(temp[0])
                cache[temp[0]] = current_highest_grade
            # Iterate through all possibilities
            for i in range(possibilities):
                temp_hand = temp[0]
                # Maximize the grade of the hand by replacing every J with any number
                for j in range(j_count):
                    # Replace the first J with any number
                    temp_hand = temp_hand.replace('J', possible_cards[i % len(possible_cards)], 1)
                    # Ensure that the i is different for every J
                    i = i // len(possible_cards)
                # Get the grade of the temporary hand
                if temp_hand in cache:
                    temp_hand_grade = cache[temp_hand]
                else:
                    temp_hand_grade = grade_hand(temp_hand)
                    cache[temp_hand] = temp_hand_grade
                # If the grade is higher than the current highest grade, replace it
                if temp_hand_grade > current_highest_grade:
                    current_highest_grade = temp_hand_grade

            hands.append((current_highest_grade, temp[0], temp[1]))

    return hands


def compare_hands(hand1: tuple, hand2: tuple) -> tuple:
    """
    Compare two hands and return the winner.
    :param hand1:
    :param hand2:
    :return winner:
    """
    for i in range(len(hand1[1])):
        higher = get_higher_card(hand1[1][i], hand2[1][i], {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14})
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
        for j in range(i + 1, len(hands)):
            if hands[i][0] == hands[j][0]:
                winner = compare_hands(hands[i], hands[j])
                if winner == hands[j]:
                    hands[i], hands[j] = hands[j], hands[i]

    # Reverse the list
    hands.reverse()

    for i in range(len(hands)):
        total_winnings += (i + 1) * int(hands[i][2])

    return total_winnings


def main():
    """
    Main function
    """
    content = file_to_list("AoC_Day07.input.txt")
    hands = list_to_hands(content)

    # Sort the hands after the grade
    hands.sort(key=lambda x: x[0], reverse=True)

    # Get the total winnings
    total_winnings = get_total_winnings(hands)

    print(f"The total winnings are: {total_winnings}")


if __name__ == "__main__":
    main()