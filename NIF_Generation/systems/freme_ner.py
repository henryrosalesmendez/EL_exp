#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'henry'

import subprocess
import urllib.parse
import xmltodict
import pickle
import os

try:
    from systems.utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass

try:
    from utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass


class Freme_NER:
    url  = "https://api.freme-project.eu/current/e-entity/freme-ner/documents?"
    number_of_request = 5
    lang = "EN"

    def __init__(self, l = "EN"):
        if not l.lower() in ["en","de","fr","es","it"]:
            print("ERROR--> FREME-NER does not support this language")
        self.lang = l

    def request_curl(self,text):
        for i in range(self.number_of_request):
            try:
                text = text.replace("'"," ")
                command = "curl -X POST --header 'Content-Type: text/plain' --header 'Accept: text/turtle' -d '"+text+"' 'https://api.freme-project.eu/current/e-entity/freme-ner/documents?language=%s&dataset=dbpedia&mode=all'"%(self.lang.lower())
                print(command)
                p = os.popen(command,"r")
                output = ""
                while True:
                    line = p.readline()
                    if not line: break
                    output += line
                return output
            except Exception as err:
                print(unicode(err))
                continue
        return None
    
    
    def untilGato(self,uri):
        return uri.split("#")[0]
    
    def toWiki(self,x):
        return "https://en.wikipedia.org/wiki/" + x.split("resource/")[1]
    
    def getIniFin(self,uri):
        LL = uri.split("#")[1]
        if LL.find("=")!=-1:
            LL = LL.split("=")[1]
        return [int(x) for x in LL.split(",")]
    
    
    def getBetween(self,txt,t1,t2):
        p1 = txt.find(t1)
        if (p1 == -1):
            return -1
        
        s = txt[p1+len(t1):]
        p2 = s.find(t2)
        if (p2 == p1-1):
            return -1
        return s[:p2]
        


    # the input "text" is a string variable with the text in plain format to annotate
    def annotate(self,text,iniPosSent,urisent,uriDocFull):
        if not text:
            print("Error: the text entered is empty!")
            return None
        
        idsent = urisent
        [ini,fin] = self.getIniFin(urisent)
        
        nifText = '''<%s>
        a nif:String , nif:Context , nif:RFC5147String ;
        nif:isString """%s"""^^xsd:string ;
        nif:beginIndex "%d"^^xsd:nonNegativeInteger ;
        nif:endIndex "%d"^^xsd:nonNegativeInteger ;
        nif:broaderContext <%s> .\n
'''%(idsent,text,ini,fin,uriDocFull)

        R = []
        response = self.request_curl(text)
        ch = ""
        for l in response.split("\n"):
            line = l.strip(" \n")
            if not line: continue
            if line.find("@prefix")!=-1: continue;
            if line[-1] != ".":
                ch = ch + line;
            else:
                ch = ch + line + "\n";
        
                if ch.find("nif:Phrase") != -1: # annotation
                    p1 = ch.find('itsrdf:taIdentRef')
                    if p1!=-1:
                        
                        link = self.toWiki(self.getBetween(ch[p1:],"<",">"))
                        
                        p1 = ch.find('nif:endIndex')
                        fin = int(self.getBetween(ch[p1:], '"', '"'))
                        
                        
                        p1 = ch.find('nif:beginIndex')
                        ini = int(self.getBetween(ch[p1:], '"', '"'))
                        
                        label = text[ini:fin]            
                        ann = '<%s#char=%d,%d>\n'%(self.untilGato(uriDocFull), ini, fin)
                        ann = ann + '        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;\n'
                        ann = ann + '        nif:referenceContext <%s> ;\n'%(idsent)
                        ann = ann + '        nif:context <%s> ;\n'%(uriDocFull)
                        ann = ann + '        nif:anchorOf """%s"""^^xsd:string ;\n'%(label)
                        ann = ann + '        nif:beginIndex "%d"^^xsd:nonNegativeInteger ;\n'%(ini)
                        ann = ann + '        nif:endIndex "%d"^^xsd:nonNegativeInteger ;\n'%(fin)
                        ann = ann + '        itsrdf:taIdentRef <%s> .\n\n'%(link)

                        nifText = nifText + ann
                        

                elif ch.find("nif:sourceUrl") != -1: # documents
                    pass
                
                elif ch.find("nif:broaderContext") != -1: # sentence
                    pass
                ch = ""
        return nifText
