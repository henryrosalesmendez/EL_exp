#!/usr/bin/python3
# -*- coding: utf-8 -*-

from nifwrapper import *
from systems.babelfy import Babelfy
from systems.dbpedia_spotlight import DBpediaSpotlight
from systems.tagme import Tagme
from systems.fred import Fred
from systems.aida import Aida
from systems.freme_ner import Freme_NER


Gold = {
    "KORE50":"/media/henry/Datos/Datasets/MINE/2019_05_19_KORE50.ttl", 
    "VoxEL": "/media/henry/Datos/Datasets/MINE/2019_05_19_VoxEL.ttl",
    "ACE": "/media/henry/Datos/Datasets/MINE/2019_05_19_ACE2004.ttl"
}

Systems = {
    "BABELFYr": Babelfy("EN", True),
    "BABELFYs": Babelfy("EN", False),
    "TAGME": Tagme("EN"),
    "DBpediaSpotlight": DBpediaSpotlight("EN"),
    "AIDA": Aida("EN"),
    "FREMENER": Freme_NER("EN"),
}

for s in Systems:
    sys = Systems[s]
    print("=============("+s+")===========")
    for gold in Gold:
        print("->",gold)
        file_nif_input = Gold[gold] 
        file_gold = open(file_nif_input, "r")
        gold_t = "".join(file_gold.readlines())
        file_gold.close()

        parser = NIFParser()
        wrp_gold = parser.parser_turtle(gold_t)

        txtNIF = ""
        for doc in wrp_gold.documents:
            uridoc = doc.uri

            ini_d = doc.getAttribute("nif:beginIndex");
            fin_d = doc.getAttribute("nif:endIndex");
            txtNIF = txtNIF + '<'+uridoc+'>\n        a nif:String , nif:Context  , nif:RFC5147String ;\n        nif:beginIndex "'+ini_d+'"^^xsd:nonNegativeInteger ;\n        nif:endIndex "'+fin_d+'"^^xsd:nonNegativeInteger ;\n        nif:sourceUrl <'+uridoc+'> .\n\n'
            
            for sent in doc.sentences:
                sent_text = sent.getText()
                ini = int(sent.getIni())
                ssal = sys.annotate(sent_text,ini,sent.uri,uridoc)
                txtNIF = txtNIF + ssal


        fout = open("SystemsResults/%s_%s.ttl"%(s,gold),"w")
        fout.write(txtNIF)
        fout.close()
