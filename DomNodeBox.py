# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 20:53:18 2021

@author: nigel
"""

class DomNodeBox:
    __slots__ = ('nodeType','tagName', 'nodeName' , 'nodeValue', 'visual_cues', 'attributes', 'childNodes','parentNode','doc','isDivide','box')
    
    def __init__(self, nodeType):
        self.nodeType = nodeType
        self.attributes = dict()
        self.childNodes = []
        self.visual_cues = dict()
        self.doc = 7
        self.isDivide = True
        self.box = []
        
        
    def createElement(self, tagName):
        self.nodeName = tagName
        self.tagName = tagName
             
    def createTextNode(self, nodeValue, parentNode):
        self.nodeName = 'text'
        self.nodeValue = nodeValue
        self.parentNode = parentNode
        
    def createComment(self, nodeValue, parentNode):
        self.nodeName = "comment"
        self.nodeValue = nodeValue
        self.parentNode = parentNode
    
    def setAttributes(self, attribute):
        self.attributes = attribute
        
    def setdoc(self,doc):
        self.doc = doc
     
    def setIsDevide(self,isDevide):
        self.isDevide = isDevide
    
    def setVisual_cues(self, visual_cues):
        self.visual_cues = dict(visual_cues)
    
    def appendChild(self, childNode):
        self.childNodes.append(childNode)