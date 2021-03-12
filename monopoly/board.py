# -*- coding: utf-8 -*-
#############################################
# description: define board class of the
#              monopoly game simulator
# author: Arianne S. Silva
# create: 11/03/2021
#############################################

import random


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
