# -*- coding: utf-8 -*-
#############################################
# description: simulates a monopoly game
# author: Arianne S. Silva
# create: 11/03/2021
#############################################

import json
import sys
from methods import *
import board as bd


def main():
    rotation = []
    time_out = 0
    winners = []
    turn = 0
    #open data file
    try:
        with open('data.json', 'r') as dataFile:
            data = json.load(dataFile)
    except FileNotFoundError:
        print("Could not found the file 'data.json'. ")
        return
    except:
        print("Error in the format json file.")
        print("\t", sys.exc_info()[1])
        return
    data_players = data['players']
    data_properties = data['properties']
    while turn < 300:
        players = []
        properties = []
        # create list players
        players = insert_players(players, data_players)
        # create list properties
        properties = insert_properties(properties, data_properties)
        # create board and insert lists
        board = bd.Board(players, properties)
        cont = board.start_play()
        if cont == 1000:
            time_out += 1
        rotation.append(cont)
        winners.append(board.get_winner())
        del players
        del properties
        del board
        turn += 1
    mean_rotation, percent_winners, winner = calculate_result(rotation, winners)
    show_result(time_out, mean_rotation, percent_winners, winner)


if __name__ == '__main__':
    main()
