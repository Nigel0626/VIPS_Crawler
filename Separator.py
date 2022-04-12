# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 20:53:18 2021

@author: nigel
"""

class Separator:
    
    ## 1 = horizontal
    ## 2 = vertical
    
    x = 0
    y = 0
    width = 0
    height = 0
    weight = 0
    type = 0
    oneSide = None
    otherSide = None
    
    def __init__(self, x,y,width,height,type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        
    def equals(self, obj):
        if isinstance(obj,Separator):
            if obj.type == 2:
                if obj.x == self.x and obj.width == self.width:
                    return True
        return self == obj
             
 #   def compare(self,obj):
 #       return self.weight - obj.weight
    
    def compare2(self,obj):
        x1 = self.x
        y1 = self.y
        x2 = obj.x
        y2 = obj.y
        if (y1 == y2):
            return x1 - x2
        else:
            return y1 - y2