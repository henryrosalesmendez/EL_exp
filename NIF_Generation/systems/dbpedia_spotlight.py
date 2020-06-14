#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'henry'

import subprocess
import xmltodict
import pickle
import urllib.parse
import os
try:
    from systems.utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass

try:
    from utils.functions import url2id,url2id_wiki_normalized, ExistFile, position2numbertoken, position2numbertoken_doc
except:
    pass

Lang2Port = {
    "EN":2222,
    "ES":2231,
    "DE": 2226,
    "dutch": 2232,
    "hungarian": 2229,
    "FR": 2225,
    "portuguese": 2228,
    "IT": 2230,
    "russian": 2227,
    "turkish": 2235,
    "ES": 2231
}

class DBpediaSpotlight:
    url  = "http://spotlight.sztaki.hu:2222/rest/annotate" #By default for English
    number_of_request = 5
    key = ""
    lang = "EN"
    param_support = 20
    param_confidence = 0.3

    def __init__(self, l = "EN",support=20,confidence=0.3):
        if l == "EN":
            self.url  = "http://model.dbpedia-spotlight.org/en/annotate"
            self.lang = "EN"
        elif not l in Lang2Port:
            print("This language is not supported by DBpedia yet. The languages availables are: " + ",".join(Lang2Port.keys()))
        else:
            self.url  = "http://spotlight.sztaki.hu:%d/rest/annotate" % Lang2Port[l]
            self.lang = l
        self.param_confidence = confidence
        self.param_support = support

    def request_curl(self,text):
        for i in range(self.number_of_request):
            try:
                p = subprocess.Popen(['curl', '-H', 'Accept: application/json', self.url, '--data-urlencode', 'text=%s' % text,
                '--data', 'confidence='+str(self.param_confidence), '--data', 'support='+str(self.param_support)],
                                     stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                                     
                stdout, stderr = p.communicate()
                if stdout:
                    self.raw_output = stdout
                    return stdout
            except Exception as err:
                print(err)
                continue
        return None
    
    #other way to call the API
    def request_curl_1(self,text):
        for i in range(self.number_of_request):
            try:
                command = 'curl -X GET "http://model.dbpedia-spotlight.org/%s/annotate?text=%s" -H "accept: application/json"'%(self.lang.lower(), urllib.parse.quote(text))
                p = os.popen(command,"r")
                output = ""
                while True:
                    line = p.readline()
                    if not line: break
                    output += line
                return output
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

    # the input "text" is a string variable with the text in plain format to annotate
    # API Specification: https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/User%27s-manual
    def annotate(self,text,iniPosSent,urisent,uriDocFull):
        if not text:
            print("Error: the text entered is empty!")
            return None

        self.processed_output = []
        dict_response = None
        try:
            dict_response = eval(self.request_curl_1(text))
        except Exception as err:
            print("--> Error",err)
            return ""
            
        idsent = urisent
        [ini_,fin_] = self.getIniFin(urisent)

        nifText = '''<%s>
        a nif:String , nif:Context , nif:RFC5147String ;
        nif:isString """%s"""^^xsd:string ;
        nif:beginIndex "%d"^^xsd:nonNegativeInteger ;
        nif:endIndex "%d"^^xsd:nonNegativeInteger ;
        nif:broaderContext <%s> .\n
'''%(idsent,text,ini_,fin_,uriDocFull)

        if not 'Resources' in dict_response:
            return nifText
        list_response = dict_response['Resources']

        for entity in list_response:
            link = self.toWiki(entity["@URI"])
            label = entity["@surfaceForm"]  
            ini = int(entity["@offset"])
            fin = ini + len(label)
                      
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

