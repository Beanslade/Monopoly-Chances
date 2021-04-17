import time
import os
from Constants import *
from Cards.CommunityChest import CommunityChest
from Cards.Chance import Chance
from GamePieces.Dice import Dice
from GamePieces.Position import Position
from GamePieces.Player import Player

ROLLS = 50
GAMES = 10000
PLAYER_COUNT = 1


def init_board():
    return [Position(pos_id=0),  # Go
            Position(pos_id=1, colour="brown", cost=60, house_price=50, rents=[0, 2, 10, 30, 90, 160, 250]),
            Position(pos_id=2),  # Community Chest
            Position(pos_id=3, colour="brown", cost=60, house_price=50, rents=[0, 4, 20, 60, 180, 320, 450]),
            Position(pos_id=4, rents=[200]),
            Position(pos_id=5, colour="train", cost=200, rents=[0, 25, 50, 100, 200]),
            Position(pos_id=6, colour="blue", cost=100, house_price=50, rents=[0, 6, 30, 90, 270, 400, 550]),
            Position(pos_id=7),  # Chance
            Position(pos_id=8, colour="blue", cost=100, house_price=50, rents=[0, 6, 30, 90, 270, 400, 550]),
            Position(pos_id=9, colour="blue", cost=120, house_price=50, rents=[0, 9, 40, 100, 300, 450, 600]),
            Position(pos_id=10),  # Just Visiting
            Position(pos_id=11, colour="pink", cost=140, house_price=100, rents=[0, 10, 50, 150, 450, 625, 750]),
            Position(pos_id=12, colour="utility", cost=150, rents=[4, 10]),
            Position(pos_id=13, colour="pink", cost=140, house_price=100, rents=[0, 10, 50, 150, 450, 625, 750]),
            Position(pos_id=14, colour="pink", cost=160, house_price=100, rents=[0, 12, 60, 180, 500, 700, 900]),
            Position(pos_id=15, colour="train", cost=200, rents=[0, 25, 50, 100, 200]),
            Position(pos_id=16, colour="orange", cost=180, house_price=100, rents=[0, 14, 70, 200, 550, 750, 950]),
            Position(pos_id=17),  # Community Chest
            Position(pos_id=18, colour="orange", cost=180, house_price=100, rents=[0, 14, 70, 200, 550, 750, 950]),
            Position(pos_id=19, colour="orange", cost=200, house_price=100, rents=[0, 16, 80, 220, 600, 800, 1000]),
            Position(pos_id=20),  # Free Parking
            Position(pos_id=21, colour="red", cost=220, house_price=150, rents=[0, 18, 90, 250, 700, 875, 1050]),
            Position(pos_id=22),  # Chance
            Position(pos_id=23, colour="red", cost=220, house_price=150, rents=[0, 18, 90, 250, 700, 875, 1050]),
            Position(pos_id=24, colour="red", cost=240, house_price=150, rents=[0, 20, 100, 300, 750, 925, 1100]),
            Position(pos_id=25, colour="train", cost=200, rents=[0, 25, 50, 100, 200]),
            Position(pos_id=26, colour="yellow", cost=260, house_price=150, rents=[0, 22, 110, 330, 800, 975, 1150]),
            Position(pos_id=27, colour="yellow", cost=260, house_price=150, rents=[0, 22, 110, 330, 800, 975, 1150]),
            Position(pos_id=28, colour="utility", cost=150, rents=[4, 10]),
            Position(pos_id=29, colour="yellow", cost=280, house_price=150, rents=[0, 24, 120, 360, 850, 1025, 1200]),
            Position(pos_id=30),  # Go To Jail
            Position(pos_id=31, colour="green", cost=300, house_price=200, rents=[0, 26, 130, 390, 900, 1100, 1275]),
            Position(pos_id=32, colour="green", cost=300, house_price=200, rents=[0, 26, 130, 390, 900, 1100, 1275]),
            Position(pos_id=33),  # Community Chest
            Position(pos_id=34, colour="green", cost=320, house_price=200, rents=[0, 28, 150, 450, 1000, 1200, 1400]),
            Position(pos_id=35, colour="train", cost=200, rents=[0, 25, 50, 100, 200]),
            Position(pos_id=36),  # Chance
            Position(pos_id=37, colour="purple", cost=350, house_price=200, rents=[0, 35, 175, 500, 1100, 1300, 1500]),
            Position(pos_id=38, rents=[100]),
            Position(pos_id=39, colour="purple", cost=400, house_price=200, rents=[0, 50, 200, 600, 1400, 1700, 2000]),
            Position(pos_id=40)]


def take_turn(player, board):
    dice1 = Dice().roll()
    dice2 = Dice().roll()

    if dice1 == dice2:
        player.inc_double_count()
        if player.get_double_count() == MAX_DOUBLES:
            player.update_position_jail()
            player.reset_double_count()
    else:
        player.reset_double_count()

    if player.get_position() == IN_JAIL and (player.get_double_count() > 0 or player.get_jail_count() > 3):
        player.update_position(JUST_VISITING)
        player.reset_jail_count()
    else:
        player.inc_jail_count()

    if player.get_position() != IN_JAIL:
        dice_total = dice1 + dice2
        player.update_position(player.get_position() + dice_total)
        if POSITION_NAMES_UK[player.get_position()] == "Community Chest":
            community_chest_card = CommunityChest().pick_up_card()
            if community_chest_card != NO_MOVE:
                board[player.get_position()].new_visit()
                if community_chest_card == IN_JAIL:
                    player.update_position_jail()
                else:
                    player.update_position(community_chest_card)
        elif POSITION_NAMES_UK[player.get_position()] == "Chance":
            chance_card = Chance().pick_up_card()
            if chance_card != NO_MOVE:
                board[player.get_position()].new_visit()
                if chance_card == GO_BACK:
                    player.update_position(player.get_position() - chance_card)
                elif chance_card == IN_JAIL:
                    player.update_position_jail()
                else:
                    player.update_position(chance_card)
        elif POSITION_NAMES_UK[player.get_position()] == "Go To Jail":
            board[player.get_position()].new_visit()
            player.update_position_jail()
        board[player.get_position()].new_visit()


if __name__ == '__main__':
    board = init_board()
    time_start = time.time()
    for game in range(GAMES):
        players = [Player(player_id=p_id, position=GO, double_count=0, jail_count=0) for p_id in range(PLAYER_COUNT)]
        for roll in range(ROLLS):
            for player in players:
                take_turn(player, board)
                while player.get_double_count() != 0:
                    take_turn(player, board)

    output = ""
    colour_average = [0 for colour in range(9)]
    for position in board:
        visit_percentage = position.get_visits() / (ROLLS * GAMES * PLAYER_COUNT) * 100.00
        if position.get_cost() != 0:
            if position.get_house_price() != 0:
                property_value = ((position.get_cost() + position.get_house_price()) / (position.get_rent(-1)))\
                                 * visit_percentage
            else:
                property_value = (position.get_cost() / position.get_rent(-1)) * visit_percentage
            print(f"{POSITION_NAMES_UK[position.pos_id]}: ")  # {visit_percentage}%
            print(f"    Property Value: {property_value}")
            if position.is_colour("brown"):
                colour_average[0] += property_value
            elif position.get_colour() == "blue":
                colour_average[1] += property_value
            elif position.get_colour() == "pink":
                colour_average[2] += property_value
            elif position.get_colour() == "orange":
                colour_average[3] += property_value
            elif position.get_colour() == "red":
                colour_average[4] += property_value
            elif position.get_colour() == "yellow":
                colour_average[5] += property_value
            elif position.get_colour() == "green":
                colour_average[6] += property_value
            elif position.get_colour() == "purple":
                colour_average[7] += property_value
            elif position.get_colour() == "train":
                colour_average[8] += property_value

    if not os.path.exists("monopoly_chances.txt"):
        with open("monopoly_chances.txt", "w") as f:
            f.write(output)

    print(f"\nBrwn average value: {colour_average[0] / 2}")
    print(f"Blue average value: {colour_average[1] / 3}")
    print(f"Pink average value: {colour_average[2] / 3}")
    print(f"Orng average value: {colour_average[3] / 3}")
    print(f"Red  average value: {colour_average[4] / 3}")
    print(f"Yelw average value: {colour_average[5] / 3}")
    print(f"Gren average value: {colour_average[6] / 3}")
    print(f"Purp average value: {colour_average[7] / 2}")
    print(f"Tran average value: {colour_average[8] / 4}")

    print(f"\nComplied in: {time.time() - time_start} seconds")
