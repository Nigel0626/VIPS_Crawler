# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 21:00:05 2021

@author: nigel
"""
import sys
from Separator import Separator


class SeparatorDetectionFinal:
    width = 0
    height = 0
    separatorType = 0
    separatorList = None
    count = 0
    
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.separatorList = []
        
    #rule 1 If the block is contained in the separator, split the separator
    #rule 2 If the block crosses with the separator, update the separator’s parameters
    #rule 3 If the block covers the separator, remove the separator
        
    def HorizontalRule1(self,block, separator):
        y = block.visual_cues['bounds']['y']
        height = block.visual_cues['bounds']['height']
        if y > separator.y and (height + y) < (separator.height + separator.y):
            return True
        return False
    
    def HorizontalRule2(self,block, separator):
        y = block.visual_cues['bounds']['y']
        height = block.visual_cues['bounds']['height']
        if (y < separator.y and ((height+y)>(separator.height + separator.y))) :
            return True
        else:
            return False

    def HorizontalRule3(self,block, separator):
        y = block.visual_cues['bounds']['y']
        height = block.visual_cues['bounds']['height']
        LBY = y + height
        SLBY = separator.y + separator.height
        if (y < separator.y and LBY > separator.y  and LBY < SLBY):
            return True
        else:
            return False

    def HorizontalRule4(self,block, seperator):
        y = block.visual_cues['bounds']['y']
        LBY = y + block.visual_cues['bounds']['height']
        SLBY = seperator.y + seperator.height
        if y > seperator.y and y < SLBY and LBY > SLBY:
            return True
        return False

    def VerticalRule1(self,block, separator):
        x = block.visual_cues['bounds']['x']
        width = block.visual_cues['bounds']['width']
        if x > separator.x and (width + x) < (separator.width + separator.x):
            return True
        return False
    
    def VerticalRule2(self,block, separator):
        x = block.visual_cues['bounds']['x']
        width = block.visual_cues['bounds']['width']
        if (x < separator.x and ((width+x)>(separator.width + separator.x))) :
            return True
        else:
            return False

    def VerticalRule3(self,block, separator):
        x = block.visual_cues['bounds']['x']
        width = block.visual_cues['bounds']['width']
        LX = x + width
        SLX = separator.x + separator.width
        if (x < separator.x and LX > separator.x  and LX < SLX):
            return True
        else:
            return False

    def VerticalRule4(self,block, seperator):
        x = block.visual_cues['bounds']['x']
        width = block.visual_cues['bounds']['width']
        LBX = x + width
        sepLBX = seperator.y + seperator.height
        if x > seperator.x and x < sepLBX and LBX > sepLBX:
            return True
        return False

    def service(self, blocks, separatorType):
        self.separatorType = separatorType
        self.firstStep()
        self.secondStep(blocks)
        self.thirdStep()
        #print (str(self.separatorType) + "-SeparatorVo.list.size::"+ str(len(self.separatorList)))
        return self.separatorList
    
    def firstStep(self):
        separator = Separator(0,0,self.width,self.height,self.separatorType)
        #print(separator.height, separator.width)
        self.separatorList.append(separator)

            ## 1.Initialize the separator list. The list starts with only one separator 
            ##(Pbe, Pee) whose start pixel and end pixel are corresponding to the borders 
            ##of the pool.

    def secondStep(self,blocks):
        if(self.separatorType == 1):
            self.DetectionHorizontal(blocks)
        else:
            self.DetectionVertical2(blocks)

    def thirdStep(self):
        tempList = []
        tempList.extend(self.separatorList)
        if (self.separatorType == 1):
            for sep in tempList:
                if sep.x == 0 and (sep.y == 0 or (sep.y + sep.height) == self.height):
                    self.separatorList.remove(sep)
        elif (self.separatorType == 2):
            for sep in tempList:
                if sep.y == 0 and (sep.x == 0 or (sep.x + sep.width) == self.width):
                    self.separatorList.remove(sep)
        else:
            return

    def DetectionHorizontal(self,blocks):
        for block in blocks:
            tempList = []
            tempList.extend(self.separatorList)
            #print("separator 1st len",len(tempList))
            for sep in tempList:
                #print(sep.height, sep.y)
                if(self.HorizontalRule1(block,sep)):
                    #print("Rule 1")
                    y = block.visual_cues['bounds']['y']
                    height = block.visual_cues['bounds']['height']
                    newY = y + height
                    newSeparator = Separator(0,newY,self.width,(sep.y+sep.height)-y, self.separatorType)
                    if newSeparator.height != 0:
                        newSeparator.oneSide = block
                        self.separatorList.append(newSeparator)
                    
                    separator = sep
                    separator.height = y - separator.y
                    #if y < separator.y:
                        #print("Y :" , y , separator.y)
                    if separator.height == 0:
                        self.separatorList.remove(separator)
                    else:
                        separator.otherSide = block
                elif(self.HorizontalRule2(block,sep)):
                    #print("Rule 2")
                    self.separatorList.remove(sep)
                elif(self.HorizontalRule3(block,sep)):
                    #print("Rule 3")
                    y = block.visual_cues['bounds']['y']
                    height = block.visual_cues['bounds']['height'] 
                    originalY = sep.y
                    sep.y = y + height
                    sep.height = sep.height + originalY - sep.y
                    sep.oneSide = block
                elif(self.HorizontalRule4(block,sep)):
                    #print("Rule 4")
                    sep.height = block.visual_cues['bounds']['y'] - sep.y
                    sep.otherSide = block
                else:
                    #print("Rule 5")
                    continue
                
                
#    def DetectionVertical(self,blocks):
#            for block in blocks:
#                tempList = []
#                tempList.extend(self.separatorList)
#                #print("separator 1st len",len(tempList))
#                for sep in tempList:
#                    #print(sep.height, sep.y)
#                    if(self.VerticalRule1(block,sep)):
#                        #print("Rule 1")
#                        x = block.visual_cues['bounds']['x']
##                        width = block.visual_cues['bounds']['width']
#                        newX = x + width
#                        newSeparator = Separator(newX,0,(sep.x+sep.width)-x,self.height, self.separatorType)
#                        if newSeparator.width != 0:
#                            newSeparator.oneSide = block
#                            self.separatorList.append(newSeparator)
#                        
#                        separator = sep
#                        separator.width = x - separator.x
#                        if separator.width == 0:
#                            self.separatorList.remove(separator)
#                        else:
#                            separator.otherSide = block
#                    elif(self.VerticalRule2(block,sep)):
#                        #print("Rule 2")
#                        self.separatorList.remove(sep)
#                    elif(self.VerticalRule3(block,sep)):
#                        #print("Rule 3")
#                        x = block.visual_cues['bounds']['x']
#                        width = block.visual_cues['bounds']['width'] 
#                        originalX = sep.x
#                        sep.x = x + width
#                        sep.width = sep.width + originalX - sep.x
#                        sep.oneSide = block
#                    elif(self.VerticalRule4(block,sep)):
#                        #print("Rule 4")
#                        sep.width = block.visual_cues['bounds']['x'] - sep.x
#                        sep.otherSide = block
#                    else:
#                        #print("Rule 5")
 #                       continue
                    
                    
    def DetectionVertical2(self,blocks):
        for block1 in blocks:
            block1X = block1.visual_cues['bounds']['x']
            block1Y = block1.visual_cues['bounds']['y']
            block1W = block1.visual_cues['bounds']['width']
            block1H = block1.visual_cues['bounds']['height']
            
            leftMinW = sys.maxsize
            leftX = 0
            leftY = 0
            leftW = 0
            leftH = 0
            
            rightMinW = sys.maxsize
            rightX = 0
            rightY = 0
            rightW = 0
            rightH = 0
            
            for block2 in blocks:
                if block1 == block2:
                    continue
                block2X = block2.visual_cues['bounds']['x']
                block2Y = block2.visual_cues['bounds']['y']
                block2W = block2.visual_cues['bounds']['width']
                block2H = block2.visual_cues['bounds']['height']
                
                RBX1 = block1X + block1W
                RBX2 = block2X + block2W
                RBY1 = block1Y + block1H
                RBY2 = block2Y + block2H
                
                if RBX2<block1X:
                    X = block2X + block2W
                    W = block1X - X
                    
                    sep = Separator(0,0,block1X,block1H,2)
                    if W < leftMinW:
                        if self.VerticalRule1(block2, sep):
                            if W < leftMinW:
                                leftMinW = W
                                leftX = X
                                leftY = block1Y
                                leftW = W
                                leftH = block1H
                                otherSide = block2
                        elif self.VerticalRule2(block2, sep):
                            if W < leftMinW:
                                leftMinW = W
                                leftX = X
                                leftY = block2Y
                                leftW = W
                                leftH = block2H
                                otherSide = block2
                        elif self.VerticalRule3(block2, sep):
                            if W < leftMinW:
                                leftMinW = W
                                leftX = X
                                leftY = block2Y
                                leftW = W
                                leftH = RBY1 - block2Y
                                otherSide = block2
                        elif self.VerticalRule4(block2, sep):
                            if W < leftMinW:
                                leftMinW = W
                                leftX = X
                                leftY = block1Y
                                leftW = W
                                leftH = RBY2 - block1Y
                                otherSide = block2
                elif block2X > RBX1:
                    X = block1X + block1W
                    W = block2X -X
                    sep = Separator(block1X, block1Y, self.width, self.height, 2)
                    if W < rightMinW:
                        if self.VerticalRule1(block2, sep):
                                rightMinW = W
                                rightX = X
                                rightY = block1Y
                                rightW = W
                                rightH = block1H
                                otherSide = block2
                        elif self.VerticalRule2(block2, sep):
                                rightMinW = W
                                rightX = X
                                rightY = block2Y
                                rightW = W
                                rightH = block2H
                                otherSide = block2
                        elif self.VerticalRule3(block2, sep):
                                rightMinW = W
                                rightX = X
                                rightY = block2Y
                                rightW = W
                                rightH = RBY2-block2Y
                                otherSide = block2
                        elif self.VerticalRule4(block2, sep):
                                rightMinW = W
                                rightX = X
                                rightY = block1Y
                                rightW = W
                                rightH = RBY2-block1Y
                                otherSide = block2
            if leftMinW < sys.maxsize:
                separator = Separator(leftX,leftY,leftW,leftH,2)
                separator.oneSide = block1
                separator.otherSide = otherSide
                self.separatorList.append(separator)
            if rightMinW < sys.maxsize:
                separator = Separator(rightX,rightY,rightW,rightH,2)
                separator.oneSide = block1
                separator.otherSide = block2
                self.separatorList.append(separator)
                
        self.combineSeparator()
        tempSeparator = self.separatorList
        finalSeparatorList = []
        
        for sep in tempSeparator:
            w1 = sep.width
            h1 = sep.height
            x1 = sep.x
            y1 = sep.y
            
            repeat = False
            for finalSep in finalSeparatorList:
                w2 = finalSep.width
                h2 = finalSep.height
                x2 = finalSep.x
                y2 = finalSep.y
                if sep == finalSep:
                    repeat = True
                if w1 == w2 and h1 == h2 and x1 == x2 and y1 == y2:
                    repeat = True
            if repeat == False:
                finalSeparatorList.append(sep)
                
        #finalSeparatorList2 = []        
        #for sep1 in finalSeparatorList:
        #    inside = False
        #    for sep2 in finalSeparatorList:
        #        if sep1 != sep2 and self.insideSep(sep1, sep2):
        #            inside = True
        #    if inside == False:
        #        finalSeparatorList2.append(sep)
        self.separatorList = finalSeparatorList;
        
        
    def insideSep(self,sep1,sep2):
        x1 = sep1.x
        y1 = sep1.y
        height1 = sep1.height
        width1 = sep1.width

        x2 = sep2.x
        y2 = sep2.y
        height2 = sep2.height
        width2 = sep2.width
        if sep1 != sep2 or (width1 != width2 and height1 != height2 and x1 != x2 and y1 != y2):
            if((x2<=x1<x2+width2) and (x2<x1+width1<=x2+width2) and (y2<y1<y2+height2) and (y2<y1+height1<y2+height2)):
                return True
            if((x2<x1<x2+width2) and (x2<x1+width1<x2+width2) and (y2<=y1<y2+height2) and (y2<y1+height1<=y2+height2)):
                return False
        return False
                    
        
    def combineSeparator(self):
        count1 = 0
        removed_list = []
        removed_index = []
        temp1 = []
        temp1.extend(self.separatorList)
        for i in temp1:
            sep1 = i
            count1 += 1
            for j in range(count1+1, len(temp1)):
                sep2 = temp1[j]
                if sep1.equals(sep2) and (abs(sep1.y-sep2.y) < 100):
                    removed_index.append(j)
                    if sep2.y > sep1.y:
                        #question
                        sep1.y = sep1.y
                        sep1.height = abs(sep1.y - sep2.y) + sep2.height
                    elif sep2.y < sep1.y:
                        sep1.y = sep2.y
                        sep1.height = abs(sep1.y - sep2.y) + sep1.height  
        for index in removed_index:
            removed_list.append(self.separatorList[index])
        
        for sep in removed_list:
            removed_list.remove(sep)
                            
                            

    

    