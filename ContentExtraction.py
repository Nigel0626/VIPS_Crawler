# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 12:06:37 2021

@author: nigel
"""
from DomNodeBox import DomNodeBox
import csv
import os

class ContentExtraction:

    maxweight = 0
    
    
    def start(self, separatorList,blocks,foldername):
        text = ""
        count = 0
        textList = []
        if len(separatorList)>0:
            textList = []
            lastBox = None
            for separator in separatorList:
                if separator.oneSide != None and separator.otherSide != None:
                    count += 1
                    firstBlock = separator.oneSide
                    secondBlock = separator.otherSide
                    weight = separator.weight
                    text1 = firstBlock.visual_cues['text']
                    text2 = secondBlock.visual_cues['text']
                    if separator.type == 1 :
                        if weight < self.maxweight:
                            if count == 1:
                                text = text1
                                #text = text1 + "\n" + text2
                                #print(text)
                            else:
                                text = text + "\n" + text2
                                #print(text)
                            #lastBox = text2    
                        else:
                            if count == 1:
                                textList.append(text1)
                                text = text2
                            else:
                                if text != "":
                                    textList.append(text)
                                    text = ""
                                    text =  text2
                                    
                                    #lastBox = text2
                                else:
                                    textList.append(text1)
                                    #textList.append(text2)
                    else:
                        nearestX = 0
                        nearestY = 0
                        for block in blocks:
                            bx = block.visual_cues["bounds"]["x"]
                            by = block.visual_cues["bounds"]["y"]
                            bh = block.visual_cues["bounds"]["height"]
                            bw = block.visual_cues["bounds"]["width"]
                            if by == separator.y:
                                if bx > separator.x and separator.weight <= 0:
                                    if lastBox != text2:
                                        text2 = block.visual_cues['text']
                                        text += text2
                                        lastBox = block.visual_cues['text']
                                        break
                                
                            
            if(text!=textList[len(textList)-1]):
                textList.append(text)
                    
        for textBox in textList:
            print(textBox)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("===================================================================")

        os.chdir(foldername)  
        with open('blog.csv', 'a+',newline='',encoding="utf-8") as file:
            w = csv.writer(file)
            w.writerow(textList)
                    
                    
    