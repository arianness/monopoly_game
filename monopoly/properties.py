# -*- coding: utf-8 -*-
#############################################
# description: define properties class of the
#              monopoly game simulator
# author: Arianne S. Silva
# create: 11/03/2021
#############################################

class Properties(object):
    def __init__(self, id, sale, rent, position):
        self.id = id
        self.sale = int(sale)
        self.rent = int(rent)
        self.owner = None
        self.position = int(position)


