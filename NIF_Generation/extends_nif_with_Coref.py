#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  This Script is used  for the extension of the EMNLP paper. Here I merge each result
#  of the systems with the output of coreference systems. 
#


from wrapperCoreference import WrapperCoreference
from nifwrapper import *
import pickle


SystemsEL = {
    "Babelfyr": {
       "VoxEL":"SystemsResults/BABELFYr_VoxEL.ttl",
       "KORE50":"SystemsResults/BABELFYr_KORE50.ttl",
       "ACE04":"SystemsResults/BABELFYr_ACE.ttl"},
    "Babelfys": {
       "VoxEL":"SystemsResults/BABELFYs_VoxEL.ttl",
       "KORE50":"SystemsResults/BABELFYs_KORE50.ttl",
       "ACE04":"SystemsResults/BABELFYs_ACE.ttl"},
    "TagME": {
       "VoxEL":"SystemsResults/TAGME_VoxEL.ttl",
       "KORE50":"SystemsResults/TAGME_KORE50.ttl",
       "ACE04":"SystemsResults/TAGME_ACE.ttl"},
    "DBpSpotlight": {
       "VoxEL":"SystemsResults/DBpediaSpotlight_VoxEL.ttl",
       "KORE50":"SystemsResults/DBpediaSpotlight_KORE50.ttl",
       "ACE04":"SystemsResults/DBpediaSpotlight_ACE.ttl"},
    "AIDA": {
       "VoxEL":"SystemsResults/AIDA_VoxEL.ttl",
       "KORE50":"SystemsResults/AIDA_KORE50.ttl",
       "ACE04":"SystemsResults/AIDA_ACE.ttl"},
    "FREMENER": {
       "VoxEL":"SystemsResults/FREMENER_VoxEL.ttl",
       "KORE50":"SystemsResults/FREMENER_KORE50.ttl",
       "ACE04":"SystemsResults/FREMENER_ACE.ttl"},
}

New_Systems_folder = "SystemsResults_with_Coref/"
wc = WrapperCoreference()
wc.setCoreNLP('/home/henry/Bin/stanford-corenlp-full-2018-10-05')
CoRerefenceSys = {}
CoRerefenceSys["CoreNLPCoref"] = wc.CoreNLPCoref
CoRerefenceSys["NeuralCoref"] = wc.NeuralCoref

Results = {}
for sysCoref_key in CoRerefenceSys:
    print("===============",sysCoref_key,"======================")
    sysCoref = CoRerefenceSys[sysCoref_key]
    
    for el in SystemsEL:
        for db in SystemsEL[el]:
            Results[el] = []
            print("____________\n",db,"\n--------")
            file_db = open(SystemsEL[el][db], "r")
            db_t = "".join(file_db.readlines())
            file_db.close()
            
            #-------
            parser = NIFParser()
            parser.showWarnings = False
            wrp_db = parser.parser_turtle(db_t)
            wrp_db.beSureOnlyOneAnnotation()
            wrp_db.addAlwaysPositionsToUriInSentence = False
            
            pos_doc = 0
            for doc in wrp_db.documents:
                pos_doc = pos_doc + 1
                txt = ""
                for sent in doc.sentences:
                    if len(sent.getText().strip(" \n"))>0:
                        if txt != "": txt = txt + " "
                        txt = txt + sent.getText()
                print(txt)
                print("---")
                corefList = sysCoref(txt)
                #print(corefList)
                wrp_db.extendsDocWithCoref(corefList, doc.uri)
                
            file_db_w = open(SystemsEL[el][db].replace("SystemsResults","SystemsResults_with_Coref").replace(".ttl","_"+sysCoref_key+".ttl"), "w")
            file_db_w.write(wrp_db.toString())
            file_db_w.close()
