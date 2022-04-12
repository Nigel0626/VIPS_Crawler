# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 01:46:24 2021

@author: nigel
"""


from DomNodeBox import DomNodeBox
from Separator import Separator
import json
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont
import csv
import calendar
import re
from SeparatorDetectionFinal import SeparatorDetectionFinal
from SeparatorWeightRule import SeparatorWeightRule
from ContentExtraction import ContentExtraction
import os
import functools
from datetime import datetime

class Vips:
    
    url_link = None
    title = None
    nodeList = []
    
    def __init__(self,url_link,title):
        self.url_link = url_link
        self.title = title


    
    inlineNodeTag = ['a','abbr','acronym','b','bdo','bdi','bdo','big','big','br',
                    'button','canvas','cite','code','data','datalist','del','dfn',
                    'em','embed','i','iframe','img','input','ins','kdb','label','map',
                    'mark','meter','noscript','object','output','picture','progress',
                    'q','ruby','s','samp','script','select','slot','small','span','strong',
                    'sub','sup','svg','template','textarea','time','u','tt','var','video','wbr','h1','h2']
    
    home_directory = "C:/Users/nigel/Desktop/Nigel's Works/RDS FYP/Coding/FinalVersion"
    folder_directory = ""
    blockList = []
    
    sizeThreshold = 40000
    
    def screenshot(self,driver, url,screenshot_path):
            print('-----------------------------Getting Screenshot------------------------------------')
            default_width=1920
            default_height=1080
            driver.set_window_size(default_width, default_height)
            driver.get(self.url_link)
            total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            print("Width:",default_width, ' Height:', total_height)
            #driver.close()
            driver.set_window_size(default_width, total_height)
            #driver.get(url)
            string = str(self.url_link) + ".png"
            print(string)
            print(screenshot_path)
            driver.save_screenshot(screenshot_path+'.png')
            print('-------------------------------Done Screenshot-----------------------------------------')
            
    def setDriver(self,url):
            CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # chrome path
            CHROMEDRIVER_PATH = r"C:\Program Files (x86)\chromedriver4.exe" # driver path  
            chrome_options = Options()
            chrome_options.add_argument("--headless") #full screen screenshot 
            chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = CHROME_PATH        
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
            default_width=1920
            default_height=1080
            driver.set_window_size(default_width, default_height)
            driver.get(url)
            total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            #print("Width:",default_width, ' Height:', total_height)
            driver.set_window_size(default_width, total_height)
            return driver
        
    def createDom(self,driver):
        file = open("dom.js", 'r')
        jscript = file.read()
        jscript += '\nreturn JSON.stringify(toJSON(document.getElementsByTagName("BODY")[0]));'
        print("Create Dom")
        print(driver.current_url)
        x = driver.execute_script(jscript)
        #print(x)
        return x 
    
    def toDOM2(self,obj,parentNode=None):
            if (isinstance(obj,str)):
                json_obj = json.loads(obj)  #use json lib to load our json string
            else:
                json_obj = obj
            nodeType = json_obj['nodeType'] ## create node object
            node = DomNodeBox(nodeType)
            if nodeType == 1: #ELEMENT NODE
                if json_obj['tagName'] != 'script':
                    node.createElement(json_obj['tagName'],)
                    attributes = json_obj['attributes']
                    if attributes != None:
                        node.setAttributes(attributes)
                    visual_cues = json_obj['visual_cues']
                    if visual_cues != None:
                        node.setVisual_cues(visual_cues)
                else:
                    return node
            elif nodeType == 3:
                node.createTextNode(json_obj['nodeValue'], parentNode)
                if node.parentNode != None:
                    visual_cues = node.parentNode.visual_cues
                    if visual_cues != None:
                        node.setVisual_cues(visual_cues)    
            else:
                return node
    
            self.nodeList.append(node)
            if nodeType == 1 :
                childNodes = json_obj['childNodes']
                for child in childNodes:
                    if(child['nodeType'] == 1):
                        if(child['tagName'] != 'script'): # remove script tag and do not append child
                            node.appendChild(self.toDOM2(child,node))
                    if (child['nodeType'] == 3):
                        try:
                            if not child['nodeValue'].isspace():
                                node.appendChild(self.toDOM2(child,node))
                        except KeyError:
                            print("error")
                        
            return node
        
        
    def drawBlock(self,fileName,blockList,i=0):
        count = 1
        img = Image.open(fileName+'.png')
        print("--------------------------------Drawing Block-----------------------------------")
        for block in blockList:
            x = block.visual_cues['bounds']['x']
            y = block.visual_cues['bounds']['y']
            height = block.visual_cues['bounds']['height']
            width = block.visual_cues['bounds']['width']
            dr = ImageDraw.Draw(img)              
                    ################ Rectangle ###################
            cor = (x,y, x+width, y+height)
            line = (cor[0],cor[1],cor[0],cor[3])
            dr.line(line, fill="red", width=1)
            line = (cor[0],cor[1],cor[2],cor[1])
            dr.line(line, fill="red", width=1)
            line = (cor[0],cor[3],cor[2],cor[3])
            dr.line(line, fill="red", width=1)
            line = (cor[2],cor[1],cor[2],cor[3])
            dr.line(line, fill="red", width=1)
            print("Drawing Block ",count, " X:", x, ' Y:',y, ' height:', height, ' width:',width )
            count +=1
                    ###############                ####################
        print("--------------------------------Done Drawing Block-----------------------------------")
        fileName = re.sub(r".png", "", fileName)
        saved_path = fileName + '_Block_' + str(i) + '.png'
        img.save(saved_path)
         
            
    def drawSeperator(self,fileName,seperatorList,type):
        count = 1
        img = Image.open(fileName+'.png')
        dr = ImageDraw.Draw(img) 
        print("--------------------------------Drawing Separator-----------------------------------")
        for seperator in seperatorList:
            x = seperator.x
            y = seperator.y
            height =seperator.height
            width = seperator.width
            print("Drawing Seperator ",count, " X:", x, ' Y:',y, ' height:', height, ' width:',width )
            dr.rectangle(((x,y),(x + width, y + height)),fill = "yellow")
            count +=1
            
        print("--------------------------------Done Drawing Seperator-----------------------------------")
        fileName = re.sub(r".png", "", fileName)
        if type == 1:
            Type = "Horizontal"
        elif type == 2:
            Type =  "Vertical"
        else:
            Type = "Final"
        saved_path = fileName + '_Seperator_' + Type + '.png'
        print("Save Path: ", saved_path)
        img.save(saved_path)
        
        

    ## rule 0
    ##If the DOM Node type is a text node and the parent node tag is A tag return divide this node, 
    ##do not divide this node
    
    
    def rule0(self,node):
        if(node.nodeType == 3):
            parent = node.parentNode
            if parent.nodeName == 'a':
                return True
            return False
        return True
    
    #rule 1
    #If the DOM node is not a text node and it has no valid children, 
    #then this node cannot be divided and will be cut.
    
    def rule1(self,node):
        if(node.nodeType != 3 and len(node.childNodes) == 0):
            return True
        else:
            return False
    
    #rule 2
    #If the DOM node has only one valid child and the child is not a text node, 
    #then divide this node
    def rule2(self,node):
        if (len(node.childNodes) == 1):
            if(self.validChild(node) == 1 and node.childNodes[0].nodeType != 3):
                return True
            else:
                return False
        else:
            return False
        
    
    #rule 3
    #If the DOM node is the root node of the sub-DOM tree 
    #(corresponding to the block), and there is only one sub DOM tree 
    #corresponding to this block, divide this node.
    def rule3(self,node):
        i = 0
        result = True
        children = node.childNodes
        for child in children:
            if child.nodeName == node.nodeName:
                result = True
                self.isOnlyOneDomSubTree(node, child,result)
                if result:
                    i+=1
        if i == 0:
            return True
        return False
    
    #rule 4
    #if all of the child nodes of the DOM node are text nodes or 
    #virtual text nodes, do not divide the node. If the font size and font weight of all these child nodes 
    #are same, set the DoC of the extracted block to 10.
    #Otherwise, set the DoC of this extracted block to 9.
    def rule4(self,node):
        i = 0
        children = node.childNodes
        fontsize = children[0].visual_cues['font-size']
        fontweight = children[0].visual_cues['font-weight']
        for child in children:
            if(child.nodeType != 3):
                return True
            if(child.visual_cues['font-size'] == fontsize and child.visual_cues['font-weight'] == fontweight):
                i+=1
        if(i == len(children)):
            node.doc==10
        else:
            node.doc == 9  
        return False
    
    
    #rule 5
    #If one of the child nodes of the DOM node is line-break node, 
    #then divide this DOM node.
    def rule5(self,node):
        children = node.childNodes
        for child in children:
            if child.nodeName in self.inlineNodeTag:
                return True
        return False
    
    #rule 6
    #If one of the child nodes of the DOM node has HTML tag <HR>, 
    #then divide this DOM node
    def rule6(node):
        children = node.childNodes
        for child in children:
            if child.nodeName == 'hr':
                return True
        return False
    
    
    #rule 7
    #If the sum of all the child nodes’ size is greater 
    #than this DOM node’s size, then divide this node.
    def rule7(self,node):
        childsize = 0;
        children =  node.childNodes
        for child in children:
            width = child.visual_cues['bounds']['width']
            height = child.visual_cues['bounds']['height']
            childsize += width*height
        nodeWidth = node.visual_cues['bounds']['width']
        nodeHeight = node.visual_cues['bounds']['height']
        nodeSize = nodeWidth * nodeHeight
        if childsize > nodeSize:
            return True
        else:
            return False
    
    #rule 8
    #If the background color of this node is different from one of its children’s, 
    #divide this node and at the same time, the child node with different background 
    #color will not be divided in this round. ? Set the DoC value (6-8) for the child 
    #node based on the html tag of the child node and the size of the child node
    def rule8(self,node):
        backgroundColour = node.visual_cues['background-color']
        children = node.childNodes
        for child in children:
            childColour = child.visual_cues['background-color']
            if childColour != backgroundColour:
                child.isDivide = False
                child.Doc = 7
                return True
        else:
            return False
    
    
    #rule 9
    #If the node has at least one text node child or at least one virtual text node child, 
    #and the node's relative size is smaller than a threshold, then the node cannot be divided
    #Set the DoC value (from 5-8) based on the html tag of the node
    def rule9(self,node):
        children = node.childNodes
        for child in children:
            if(child.nodeName == "text" or self.virtualTextNode(child)):
                nodeSize =  node.visual_cues['bounds']['width'] * node.visual_cues['bounds']['height']
                if nodeSize < self.sizeThreshold:
                    return False
            return True
        return True
            
    
    #rule 10
    #If the child of the node with maximum size are small than a threshold (relative size), do not divide this node. 
    #Set the DoC based on the html tag and size of this node
    def rule10(self,node):
        children = node.childNodes
        for child in children:
            size = 0
            width = child.visual_cues['bounds']['width']
            height = child.visual_cues['bounds']['height']
            size = width*height
            if size < self.sizeThreshold:
                return False
        return True
    
    #rule 11
    #If previous sibling node has not been divided, do not divide this node
    def rule11(self,node):
        parentNode = node.parentNode
        siblings = parentNode.childNodes
        for sibling in siblings:
            if sibling.isDivide == False:
                return False
        return True
                
    #rule 12
    #divide this node
    def rule12(node):
        return True
    
    #rule 13
    #Do not divide this node. Set the DoC value based on the html tag and size of this node.
    def rule13(node):
        node.doc = 6
        return False
    
    #def rule14(node):
    #    if(node.nodeName == 'text'):
    #        if(len(node.childNodes) == 0):
    #            return False
        
    ## can be seen and width and height not equal to 0
    def validNode(self,node):
        height = node.visual_cues['bounds']['height']
        width = node.visual_cues['bounds']['width']
        visibility = node.visual_cues['visibility']
        if(height != 0 and width != 0 and visibility != "hidden"):
            return True
        else:
            return False
        
    def validChild(self,node):
        i = 0
        children = node.childNodes
        for child in children:
            if(self.validNode(child)):
                i+=1
        return i
    
    def virtualTextNode(self,node):
        if node.nodeName in self.inlineNodeTag:
            children = node.childNodes
            for child in children:
                if child.nodeName != "text" or self.virtualTextNode(child):
                    return False
            return True
        return False  
    
    def isOnlyOneDomSubTree(self,pattern, node, result):
            if pattern.nodeName != node.nodeName:
                result = False
            pattern_child = pattern.childNodes
            node_child = node.childNodes
            if len(pattern_child) != len(node_child):
                result = False
            if not result:
                return 
            for i in range(0,len(pattern_child)):
                self.isOnlyOneDomSubTree(pattern_child[i],node_child[i],result)
    def divideable(self,node):
        tag = node.nodeName
        if(tag == "text"):
            if(node.parentNode.nodeName in self.inlineNodeTag):
                if self.rule0(node) == False:
                    return False
                if self.rule1(node):
                    return True
                if self.rule2(node):
                    return True
                if self.rule3(node):
                    return True
                if self.rule4(node):
                    return True
                if self.rule5(node):
                    return True
                if self.rule6(node):
                    return True
                if self.rule7(node):
                    return True
                if self.rule9(node):
                    return True
                if self.rule10(node):
                    return True
                if self.rule12(node):
                    return True
            return False
                
        if(tag == 'table'):
            if self.rule1(node):
                return True
            if self.rule2(node):
                return True
            if self.rule3(node):
                return True
            if self.rule8(node):
                return True
            if self.rule10(node):
                return True
            if self.rule13(node):
                return True
            return False
        
        elif(tag == 'tr'):
            if self.rule1(node):
                return True
            if self.rule2(node):
                return True
            if self.rule3(node):
                return True
            if self.rule7(node):
                return True
            if self.rule8(node):
                return True
            if self.rule10(node):
                return True
            if self.rule11(node):
                return True
            if self.rule13(node):
                return True
            return False
            
        elif(tag == 'td'):
            if self.rule1(node):
                return True
            if self.rule2(node):
                return True
            if self.rule3(node):
                return True
            if self.rule4(node):
                return True
            if self.rule4(node):
                return True
            if self.rule9(node):
                return True
            if self.rule10(node):
                return True
            if self.rule11(node):
                return True
            if self.rule13(node):
                return True
            return False
        elif(tag == 'p'):
            if self.rule1(node):
                return True
            if self.rule2(node):
                return True
            if self.rule3(node):
                return True
            if self.rule4(node):
                return True
            if self.rule5(node):
                return True
            if self.rule6(node):
                return True
            if self.rule7(node):
                return True
            if self.rule9(node):
                return True
            if self.rule10(node):
                return True
            if self.rule12(node):
                return True
            return False
        elif(tag == 'h1'): #do not divide
            return False
        elif(tag == 'h2'): #do not divide
            return False
        elif(tag == 'b'): #do not divide
            return False
        #elif(tag == 'i'):
        #    return False
        else:
            if self.rule1(node):
                return True
            if self.rule2(node):
                return True
            if self.rule3(node):
                return True
            if self.rule4(node):
                return True
            if self.rule6(node):
                return True
            if self.rule7(node):
                return True
            if self.rule9(node):
                return True
            if self.rule10(node):
                return True
            if self.rule12(node):
                return True
            return False
            
        
    def divideDomTree(self,node):
        if(self.divideable(node) and node.isDivide):
            children = node.childNodes
            for child in children:
                self.divideDomTree(child)
        else:
            self.blockList.append(node)
            node.isDivide = False
            
    def sepCompare(self,sep1, sep2):
        if sep1.compare2(sep2) < 0:
            return -1
        else:
            return 1
        #else: return 0
        
    def makdir(self):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        os.chdir(self.home_directory+"/ScreenShot")
        title = self.title
        title.replace('.', '')
        try:
            os.mkdir(title+"_"+dt_string)
        except OSError:
            title = "Blog"
            os.mkdir(title+"_"+dt_string)
        self.folder_directory = self.home_directory+"/ScreenShot" + "/" + title +"_"+dt_string
    
    def start(self):
        self.nodeList = []
        self.blockList = []
        self.latestList = []
        self.tempBlockList = []
        print(self.url_link)
        driver = self.setDriver(self.url_link)
        self.makdir()
        
        path = 'ScreenShot'
        os.chdir(self.folder_directory)
        self.screenshot(driver,self.url_link,"screenshot.png")
        os.chdir(self.home_directory)
        print(driver.current_url)
        dom = self.createDom(driver)
        #height = driver.get_window_size()['height']
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.quit()
        self.toDOM2(dom)
        #print(self.nodeList)
        self.divideDomTree(self.nodeList[0])
        os.chdir(self.folder_directory)
        
        latestList = []
        driver.quit()
        ## remove duplicate block
        for node in self.blockList:
            similar = False
            text = node.visual_cues['text']
            for node2 in latestList:
                if node2.visual_cues['text'] == text:
                    similar = True
            if similar == False:
                latestList.append(node)
         
                
        tempBlockList = latestList
        latestList = []
        
        
        #remove block when the height = 0, width = 0, x and y lesser or equal zero
        for node1 in tempBlockList:
            height = node1.visual_cues['bounds']['height']
            width = node1.visual_cues['bounds']['width']
            x = node1.visual_cues['bounds']['x']
            y = node1.visual_cues['bounds']['y']
            if height != 0 and width != 0 and x>= 0 and y>=0:
                latestList.append(node1)
                
        tempBlockList = latestList
        latestList = []        
        #newBlockList2 = []
        
        #remove block that is contains inside another node
        count = 1
        inside = False
        for node1 in tempBlockList:  
            inside = False
            x1 = node1.visual_cues['bounds']['x']
            y1 = node1.visual_cues['bounds']['y']
            height1 = node1.visual_cues['bounds']['height']
            width1 = node1.visual_cues['bounds']['width']
            for node2 in self.blockList:
                x2 = node2.visual_cues['bounds']['x']
                y2 = node2.visual_cues['bounds']['y']
                height2 = node2.visual_cues['bounds']['height']
                width2 = node2.visual_cues['bounds']['width']
                if node1 != node2:
                    count+=1
                    if((x2<=x1<x2+width2) and (x2<x1+width1<=x2+width2) and (y2<y1<y2+height2) and (y2<y1+height1<y2+height2)):
                        inside = True
                    if((x2<x1<x2+width2) and (x2<x1+width1<x2+width2) and (y2<=y1<y2+height2) and (y2<y1+height1<=y2+height2)):
                        inside = True
            if inside == False:
                latestList.append(node1)
        
        
        tempBlockList = latestList
        latestList = []         
        #newBlockList3 =[]
        
        # remove navigation bar block (remove block that the x location is more half of the total width)
        for node1 in tempBlockList:  
            inside = False
            x1 = node1.visual_cues['bounds']['x']
            if(x1<(1920/2)):
                latestList.append(node1)
        
        
        tempBlockList = latestList
        latestList = []         
        #newBlockList4 = []
        
        #combine block that the distance between is zero
        deleteList = []
        for i in range (len(tempBlockList)):
            #print(i)
            node1 = tempBlockList[i]
            y1 = node1.visual_cues['bounds']['y']
            x1 = node1.visual_cues['bounds']['x']
            h1 = node1.visual_cues['bounds']['height']
            w1 = node1.visual_cues['bounds']['width']
            addedWidth = 0
            addedHeight = 0
            for a in range (len(tempBlockList)):
                node2 = tempBlockList[a]
                y2 = node2.visual_cues['bounds']['y']
                x2 = node2.visual_cues['bounds']['x']
                h2 = node2.visual_cues['bounds']['height']
                w2 = node2.visual_cues['bounds']['width'] 
                if node1 != node2:
                    if(x1==x2) and (y1+h1+addedHeight == y2):
                        node1.visual_cues['bounds']['height'] += h2
                        node1.visual_cues['text'] +=  node2.visual_cues['text']
                        addedHeight += h2
                        deleteList.append(node2)
                        #print("Triggered")
                    if(y1==y2) and (x1+w1 == x2):
                        node1.visual_cues['bounds']['width'] += w2
                        node1.visual_cues['text'] +=  node2.visual_cues['text']
                        deleteList.append(node2)
                        #print("Triggered")
            if node1 not in deleteList:
                latestList.append(node1)
                
        self.drawBlock('screenshot.png', latestList)
        
        #driver.quit()
        #driver = self.setDriver(self.url_link)
        #width = driver.get_window_size()['width']
        #height = driver.get_window_size()['height']
        #total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        width = 1920
        SD = SeparatorDetectionFinal(width,total_height)
        print(SD.width, SD.height)
        horizontalSeparator = []
        horizontalSeparator.extend(SD.service(latestList, 1))
        self.drawSeperator('screenshot_Block_0',horizontalSeparator,1)
        #driver.quit()
        
        SD = SeparatorDetectionFinal(width,total_height)
        print(SD.width, SD.height)
        verticalSeparator = []
        verticalSeparator.extend(SD.service(latestList, 2))
        self.drawSeperator('screenshot_Block_0_Seperator_Horizontal',verticalSeparator,2)
        
        sw = SeparatorWeightRule()
        newHorizontalSeparator = []
        newVerticalSeparator = []
        newHorizontalSeparator = sw.start(horizontalSeparator, 1)
        newVerticalSeparator = sw.start(verticalSeparator, 2)
        
        finalSeparatorList = []
        finalSeparatorList.extend(newHorizontalSeparator)
        finalSeparatorList.extend(newVerticalSeparator)
        

        finalSeparatorList.sort(key=functools.cmp_to_key(self.sepCompare))
        
        
        extraction = ContentExtraction()
        extraction.start(finalSeparatorList, latestList,self.home_directory)
        print(self.url_link)

        
        #for sep in horizontalSeparator:
        #    if(sep.oneSide != None):
        #        firstBox = sep.oneSide
        #        text1 = firstBox.visual_cues["text"]
        #        print(text1)
        #    if(sep.otherSide != None):
        #        firstBox = sep.otherSide
        #        text2 = firstBox.visual_cues["text"]
        #        print(text2)
        #    print("===========================================")