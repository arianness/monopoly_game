# -*- coding: utf-8 -*-
#############################################
# description: define the methods of the
#              monopoly game simulator
# author: Arianne S. Silva
# create: 11/03/2021
#############################################


import numpy as np
import players as pl
import properties as pr


def insert_players(players, data):
    for element in data:
        player = pl.Players(element['id'], element['posture'])
        players.append(player)
    return players


def insert_properties(properties, data):
    for element in data:
        propertie = pr.Properties(element['id'], element['sale'], element['rent'], element['position'])
        properties.append(propertie)
    return properties


def calculate_result(rotation, winners):
    percent_winners = {}
    values = []
    percent_winners['impulsive'] = winners.count('i')
    percent_winners['exigent'] = winners.count('e')
    percent_winners['cautious'] = winners.count('c')
    percent_winners['aleatory'] = winners.count('a')
    percent_winners['total'] = len(winners)
    for key, value in percent_winners.items():
        if key != 'total':
            values.append(value)
    winners = sorted(values, reverse=True)
    larger = winners[0]
    for key, value in percent_winners.items():
        percent = (percent_winners[key] / percent_winners['total']) * 100
        if key != 'total':
            percent_winners[key] = [value, format(percent, '.2f')]
            if larger == value:
                winner = key
    rotation_mean = np.mean(rotation)
    percent_winners.pop('total')
    return rotation_mean, percent_winners, winner


def show_result(time_out, mean_rotation, percent_winners, winner):
    print("\n")
    print("Average of turns: ", format(mean_rotation, '.2f'))
    print("Total of time-out: ", time_out)
    print("Winning percentage per posture: ")
    for key, value in percent_winners.items():
        print('\t', key, str(value[1]) + '%')
    print("Winner posture: ", winner)
    print("\n")
