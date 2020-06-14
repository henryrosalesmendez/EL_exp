#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'henry'

import subprocess
import urllib.parse
import xmltodict
import pickle

try:
    from systems.utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc, yago2wikiid
except:
    pass

try:
    from utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc, yago2wikiid
except:
    pass

null = None

class Aida:
    url  = "https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate"
    number_of_request = 5
    key = ""
    lang = "EN"
    
    def __init__(self, l = "EN"):
        self.lang = l

    def request_curl(self,text):
        query_post = "text=" + urllib.parse.quote(text)
        for i in range(self.number_of_request):
            try:
                p = subprocess.Popen(['curl', '--data', query_post, self.url],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    self.raw_output = stdout
                    return stdout
            except Exception as err:
                print(err)
                continue
        return None

    def untilGato(self,uri):
        return uri.split("#")[0]
    
    def toWiki(self,x):
        return "https://en.wikipedia.org/wiki/" + x.split("resource/")[1]
    
    # Joe_Jackson_\\u0028manager\\u0029   ----->   Joe_Jackson_(manager)
    def decode(self,x):
        x_ = x.replace("\\u00","%")
        return urllib.parse.unquote(x_)
    
    def Yago2Wiki(self,x):
        return "https://en.wikipedia.org/wiki/" + self.decode(x.split(":")[1])
    
    def getIniFin(self,uri):
        LL = uri.split("#")[1]
        if LL.find("=")!=-1:
            LL = LL.split("=")[1]
        return [int(x) for x in LL.split(",")]
    
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
        dict_response = eval(self.request_curl(text))
        for entity in dict_response["mentions"]:
            #{'allEntities': [{'kbIdentifier': 'YAGO:Joe_Jackson_\\u0028manager\\u0029', 'disambiguationScore': '1'}], 'offset': 0, 'name': 'Joseph Walter Jackson', 'length': 21, 'bestEntity': {'kbIdentifier': 'YAGO:Joe_Jackson_\\u0028manager\\u0029', 'disambiguationScore': '1'}}

            if "bestEntity" in entity:                
                link = self.Yago2Wiki(entity["bestEntity"]["kbIdentifier"])
                ini = int(entity["offset"])
                fin = int(entity["offset"]) + int(entity["length"])
                label = text[ini:fin]            
                ann = '''<%s#char=%d,%d>
        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
        nif:referenceContext <%s> ;
        nif:context <%s> ;
        nif:anchorOf """%s"""^^xsd:string ;
        nif:beginIndex "%d"^^xsd:nonNegativeInteger ;
        nif:endIndex "%d"^^xsd:nonNegativeInteger ;
        itsrdf:taIdentRef <%s> .
        
''' %(self.untilGato(uriDocFull), ini, fin,idsent,uriDocFull,label,ini,fin,link)
                nifText = nifText + ann
                
        return nifText
