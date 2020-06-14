#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  This script take the nif generated with the systems, and include both, the anotation of coref and WSD. Here is not include 'disambiguate'
#


from wrapperWSD import WrapperWSD
from wrapperCoreference import WrapperCoreference
from nifwrapper import *
import pickle




wsd = WrapperWSD()
wsd.gKey = "807038db-4b34-4656-b1f0-54b1792d7dee"
WSDSys = {}
WSDSys["wsdNLTK"] = wsd.wsdNLTK_links
#WSDSys["wsdBabelfy"] = wsd.wsdBabelfy



wc = WrapperCoreference()
wc.setCoreNLP('/home/henry/Bin/stanford-corenlp-full-2018-10-05')
CoRerefenceSys = {}


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




New_Systems_folder = "SystemsResults_with_Corr_WSD/"


Results = {}
#for sys_key in WSDSys:
#    print("===============",sys_key,"======================")
#    sys = WSDSys[sys_key]
    
for el in SystemsEL:
    print("el:",el)
    
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

            wsd_ = wsd.wsdNLTK_links(txt)
            wrp_db.extendsDocWithWSD(wsd_, doc.uri)
            
            corefList = wc.CoreNLPCoref(txt)
            wrp_db.extendsDocWithCoref(corefList, doc.uri)
            
            corefList = wc.NeuralCoref(txt)
            wrp_db.extendsDocWithCoref(corefList, doc.uri)
            
            
        newName = SystemsEL[el][db].replace("SystemsResults","SystemsResults_with_WSD").replace(".ttl","_corr_wsd.ttl")
        file_db_w = open(newName, "w")
        file_db_w.write(wrp_db.toString())
        file_db_w.close()
