# -*- coding: utf-8 -*-
#############################################
# description: define players class of the
#              monopoly game simulator
# author: Arianne S. Silva
# create: 11/03/2021
#############################################

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
