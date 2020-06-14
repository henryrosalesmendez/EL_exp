#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'henry'

import subprocess
import urllib.parse
import xmltodict
import pickle

try:
    from systems.utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass

try:
    from utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass


class Babelfy:
    url  = "https://babelfy.io/v1/disambiguate"
    number_of_request = 5
    key="YOUR_KEY_HERE"
    lang = "EN"
    todos = True


    def __init__(self, l = "EN", todos_ = True):
        self.lang = l
        self.todos = todos_

    def request_curl(self,text):
        if self.todos:
            query_post = "lang="+self.lang+"&key="+self.key+"&annType=ALL&text="+urllib.parse.quote(text)
        else: query_post = "lang="+self.lang+"&key="+self.key+"&annType=NAMED_ENTITIES&text="+urllib.parse.quote(text)
        
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
    
    def getIniFin(self,uri):
        LL = uri.split("#")[1]
        if LL.find("=")!=-1:
            LL = LL.split("=")[1]
        return [int(x) for x in LL.split(",")]

    # returns a list of stripped uris, e.g., ["Barack_Obama","Michael_Jacson"]
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
        req = self.request_curl(text)
        list_response = eval(req)
        #{'tokenFragment': {'start': 1, 'end': 2}, 'charFragment': {'start': 4, 'end': 16}, 'babelSynsetID': 'bn:00075359n', 'DBpediaURL': 'http://dbpedia.org/resource/Supreme_Court_of_the_United_States', 'BabelNetURL': 'http://babelnet.org/rdf/s00075359n', 'score': 0.0, 'coherenceScore': 0.0, 'globalScore': 0.0, 'source': 'MCS'}
        
        for entity in list_response:
            if "DBpediaURL" in entity and entity["DBpediaURL"]:
                link = self.toWiki(entity["DBpediaURL"])
                ini = int(entity["charFragment"]["start"])
                fin = int(entity["charFragment"]["end"]) + 1
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
