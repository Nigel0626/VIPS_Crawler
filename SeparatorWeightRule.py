# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 01:52:22 2021

@author: nigel
"""

from Separator import Separator

class SeparatorWeightRule:
    distance = 50
    nodeList = []
    separatorList = []
    
    #def __init__(self, nodeList):
    #    self.nodeList = nodeList
        
    def rule1(self,sep):
        if sep.type == 1:
            sep = (sep.weight+(sep.height/self.distance))
        else:
            sep = (sep.weight+(sep.width/self.distance))
            
     
    def rule2(self,sep):
       firstBox = sep.oneSide
       secondBox = sep.otherSide
       
       firstColour = firstBox.visual_cues['background-color']
       secondColour = secondBox.visual_cues['background-color']
       if firstColour != secondColour:
           sep.weight += 1
       
       return sep
    
    def rule3(self,sep):
        if sep.type == 1:
            firstBox = sep.oneSide
            secondBox = sep.otherSide
            
            firstFontSize = firstBox.visual_cues['font-size']
            secondFontSize = secondBox.visual_cues['font-size']
            
            if firstFontSize != secondFontSize:
                sep.weight += 1
            if secondFontSize > firstFontSize:
                sep.weight += 1
        return sep

                
    def rule4(self,sep):
        if sep.type == 1:
            firstBox = sep.oneSide
            secondBox = sep.otherSide
            
            firstNodeName = firstBox.nodeName
            secondNodeName = secondBox.nodeName
            
            if firstNodeName == secondNodeName:
                sep.weight -= 1 
        return sep
    
                    
    #def rule6(sep):
    #    if sep.type == 1:
    #        firstBox = sep.oneSide
    #        secondBox = sep.otherSide
            
    #        firstFontType = firstBox.visual_cues['font-type']
    #        secondFontType = secondBox.visual_cues['font-type']
            
    #        if firstFontSize != secondFontSize:
    #            sep.weight += 1
    #        if secondFontSize > firstFontSize:
    #            sep.weight += 1
    
    def start(self, separatorList, separatorType):
        newSeparatorList = []
        for sep in separatorList:
            if sep.oneSide != None and sep.otherSide != None:
                self.rule1(sep)
                if separatorType == 1:
                    self.rule2(sep)
                    self.rule3(sep)
                    self.rule4(sep)
                newSeparatorList.append(sep)
        return newSeparatorList

    
   