#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import json
import random

class Format:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ColorTree:

    def __init__(self, id, seed):

        self._build_atributes(id)
        
        self.choose_color_8bit(seed)

    def _build_atributes(self, id):

        with open(('res/t_full_' + id), 'r') as file:
            self.full = file.read().splitlines()
            self.full.reverse()
            self.full.pop(0)
            self.full.pop(0)
            self.full.reverse()

            self.x_offset = len(max(self.full, key=len))


            self.height = len(self.full)

            for i in range(len(self.full)):
                self.full[i] = list(self.full[i])


        with open(('res/t_sap_' + id), 'r') as file:
           
            self.sap = file.read().splitlines()
            self.sap.reverse()

            self.color_list = json.loads(self.sap[0])
            self.sap.pop(0)

            self.root = self.sap[0].find('$')

            self.sap.pop(0)
            self.sap.reverse()

            self.sap_height = len(self.sap)

            for i in range(self.sap_height):
                self.sap[i] = list(self.sap[i])
            
    def choose_color(self, seed):
        color_list_caule =  [Format.RED,    Format.DARKCYAN]
        color_list_extras = [Format.BLUE,   Format.CYAN,   Format.PURPLE]
        color_list_leafs =  [Format.YELLOW, Format.GREEN]
        
        random.seed(seed)
        self.color_list_all = [color_list_caule[random.randint(0, 1)],
                          color_list_extras[random.randint(0, 2)],
                          color_list_leafs[random.randint(0, 1)]]

    def choose_color_8bit(self, seed):
        #COLOR STUFF
        self.CSI = '\033[38:5:'
        self.COMP = 'm'
        self.END = '\033[0m'

        self.LEAFS = [22, 23, 28, 29, 34, 35, 36, 40, 41, 42, 43,
                46, 47, 48, 49, 70, 76, 77, 82, 83, 84, 118,
                154, 10, 2, 11, 13, 225, 131, 238, 16, 1, 3, 9]
        self.leafs_len = len(self.LEAFS) -1

        self.CAULES = [52, 88, 124, 196, 58, 94, 130, 166, 202, 203,
                167, 131, 238, 16, 1, 3, 9, 42, 43, 46, 47, 48, 49]
        self.caules_len = len(self.CAULES) -1

        self.EXTRAS = [126, 127, 128, 1290, 161, 162, 163, 164, 165, 199, 200, 201, 27, 63, 399,
                135, 4514, 13, 13, 14, 12, 9, 51, 111, 226, 192, 193, 154, 10, 2, 11, 13, 225]
        self.extras_len = len(self.EXTRAS) -1

        self.color_list_all = [
            self.CSI + str(self.CAULES[random.randint(0,self.caules_len)]) + self.COMP,
            self.CSI + str(self.EXTRAS[random.randint(0,self.extras_len)]) + self.COMP,
            self.CSI + str(self.LEAFS[random.randint(0,self.leafs_len)]) + self.COMP,
        ]

    def buffer(self, y, x, buffer, flag, switch):

        if switch == "sap":

            for i in range(self.sap_height):

                for j in range(len(self.sap[i])):

                    if self.sap[i][j] == ' ': pass

                    # CAULES
                    elif (self.sap[i][j] in self.color_list[0]):
                        
                        buffer[y+i-self.sap_height+1][x+j-self.root] = (self.color_list_all[0] 
                                                                + self.sap[i][j]
                                                                + Format.END)
                    # EXTRAS
                    elif (self.sap[i][j] in self.color_list[1]):
                        flag[y+i-self.sap_height+1][x+j-self.root] = True
                        buffer[y+i-self.sap_height+1][x+j-self.root] = (self.color_list_all[1]
                                                                + self.sap[i][j]
                                                                + Format.END)
                    # LEAFS
                    else:
                        flag[y+i-self.sap_height+1][x+j-self.root] = True
                        buffer[y+i-self.sap_height+1][x+j-self.root] = (self.color_list_all[2]
                                                                + self.sap[i][j]
                                                                + Format.END)

        if switch == "full":
            
            for i in range(self.height):

                for j in range(len(self.full[i])):

                    if self.full[i][j] == ' ': pass

                    # CAULES
                    elif (self.full[i][j] in self.color_list[0]):
                        flag[y+i-self.height+1][x+j-self.root] = True
                        buffer[y+i-self.height+1][x+j-self.root] = (self.color_list_all[0] 
                                                                + self.full[i][j]
                                                                + Format.END)
                    # EXTRAS
                    elif (self.full[i][j] in self.color_list[1]):
                        flag[y+i-self.height+1][x+j-self.root] = True
                        buffer[y+i-self.height+1][x+j-self.root] = (self.color_list_all[1]
                                                                + self.full[i][j]
                                                                + Format.END)
                    # LEAFS
                    else:
                        flag[y+i-self.height+1][x+j-self.root] = True
                        buffer[y+i-self.height+1][x+j-self.root] = (self.color_list_all[2]
                                                                + self.full[i][j]
                                                                + Format.END)

