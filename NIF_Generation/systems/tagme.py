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


class Tagme:
    url  = "https://tagme.d4science.org/tagme/tag"
    number_of_request = 5
    key = "YOUR_KEY_HERE"
    lang = "EN"

    def __init__(self, l = "EN"):
        if not l.lower() in ["en","it","de"]:
            print("ERROR--> TAGME does not support this language")
        self.lang = l

    def request_curl(self,text):
        query_post = "text=" + urllib.parse.quote(text)+ "&lang="+self.lang.lower()+"&gcube-token="+self.key+"&include_categories=true"
        for i in range(self.number_of_request):
            try:
                p = subprocess.Popen(['curl', '--data', query_post, self.url],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    self.raw_output = stdout
                    return stdout
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

    # the input "text" is a string variable with the text in plain format to annotate
    def annotate(self,text,iniPosSent,urisent,uriDocFull):
        if not text:
            print("Error: the text entered is empty!")
            return None

        dict_response = eval(self.request_curl(text))
        
        idsent = urisent
        [ini,fin] = self.getIniFin(urisent)
        
        nifText = '''<%s>
        a nif:String , nif:Context , nif:RFC5147String ;
        nif:isString """%s"""^^xsd:string ;
        nif:beginIndex "%d"^^xsd:nonNegativeInteger ;
        nif:endIndex "%d"^^xsd:nonNegativeInteger ;
        nif:broaderContext <%s> .\n
'''%(idsent,text,ini,fin,uriDocFull)
        
        
        
        for entity in dict_response["annotations"]:
            if "title" in entity:
                link = "https://en.wikipedia.org/wiki/" + entity["title"].replace(" ","_")
                ini = entity["start"]
                fin = entity["end"]
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
