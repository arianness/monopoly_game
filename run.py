# -*- coding: utf-8 -*-
#############################################
# description: simulates a monopoly game
# author: Arianne S. Silva
# create: 11/03/2021
#############################################

import json
import random
import numpy as np
import sys


class Players(object):
    def __init__(self, id, posture):
        self.id = id
        self.position = 0
        self.posture = posture
        self.balance = 0
        self.properties = []

    def pay(self, value):
        self.balance = self.balance - value

    def get(self, value):
        self.balance = self.balance + value


class Properties(object):
    def __init__(self, id, sale, rent, position):
        self.id = id
        self.sale = int(sale)
        self.rent = int(rent)
        self.owner = None
        self.position = int(position)


class Board(object):
    def __init__(self, players, properties):
        self.players = players
        self.properties = properties
        self.players_off = []

    def start_play(self):
        random.shuffle(self.players)
        self.pay_players()
        cont = 0
        get_out = 0
        while cont < 1000 and get_out == 0:
            for player in self.players:
                # check if just have one player
                if len(self.players_off) == len(self.players) - 1:
                    get_out = 1
                    cont -= 1
                    break
                # check if player is off
                if player in self.players_off:
                    continue
                # check if balance player is negative
                if player.balance < 0:
                    self.remove_player(player)
                    continue
                position = self.play_dice(player)
                property = self.check_position(position)
                self.check_property(property, player)
            cont += 1
        return cont

    def pay_players(self):
        for player in self.players:
            player.get(300)

    def play_dice(self, player):
        position = random.randint(1, 6)
        if (player.position + position) > 20:
            player.position = (player.position + position) - 20
            player.get(100)
        else:
            player.position += position
        return player.position

    def remove_player(self, player):
        if len(player.properties) > 0:
            for property in player.properties:
                property.owner = None
            player.properties = []
        self.players_off.append(player)

    def check_position(self, position):
        for property in self.properties:
            if property.position == position:
                return property

    def check_balance(self, sale, balance):
        if (balance - sale) >= 0:
            return 0
        return 1

    def check_property(self, property, player):
        if property.owner is None:
            if self.check_balance(property.sale, player.balance) == 0:
                if self.check_posture(property.rent, property.sale, player) == 0:
                    self.buy_property(player, property)
        else:
            self.pay_rent(player, property)

    def check_posture(self, rent, sale, player):
        if player.posture == 'i':
            return 0
        if player.posture == 'e':
            if rent > 50:
                return 0
            return 1
        if player.posture == 'c':
            if (player.balance - sale) >= 80:
                return 0
            return 1
        if player.posture == 'a':
            x = random.randint(0, 1)
            return x

    def buy_property(self, player, property):
        sale = property.sale
        player.pay(sale)
        player.properties.append(property)
        property.owner = player

    def pay_rent(self, player, property):
        owner = property.owner
        rent = property.rent
        player.pay(rent)
        owner.get(rent)

    def get_winner(self):
        balances = []
        for player in self.players:
            balances.append(player.balance)
        balances_order = sorted(balances, reverse=True)
        for player in self.players:
            if balances_order[0] == player.balance:
                winner = player
                break
        return winner.posture


def insert_players(players, data):
    for element in data:
        player = Players(element['id'], element['posture'])
        players.append(player)
    return players


def insert_properties(properties, data):
    for element in data:
        propertie = Properties(element['id'], element['sale'], element['rent'], element['position'])
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
        board = Board(players, properties)
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
