#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  This script take the nif with the annotations from NCR + SCR + WSD-NLTK and include the annotations of the 'disambiguate' system
#


from wrapperWSD import WrapperWSD
from nifwrapper import *
import pickle




wsd = WrapperWSD()
WSDSys = {}
#WSDSys["wsdNLTK"] = wsd.wsdNLTK_links
WSDSys["wsdNWSDT"] = wsd.wsdNWSDT_links
wsd.value["source_NWSDT"] = "/home/henry/bin/disambiguate"


SystemsEL = {
    "Babelfyr": {
       "VoxEL":"Systems_ALL/BABELFYr_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/BABELFYr_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/BABELFYr_ACE_ALL.ttl"},
    "Babelfys": {
       "VoxEL":"Systems_ALL/BABELFYs_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/BABELFYs_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/BABELFYs_ACE_ALL.ttl"},
    "TagME": {
       "VoxEL":"Systems_ALL/TAGME_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/TAGME_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/TAGME_ACE_ALL.ttl"},
    "DBpSpotlight": {
       "VoxEL":"Systems_ALL/DBpediaSpotlight_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/DBpediaSpotlight_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/DBpediaSpotlight_ACE_ALL.ttl"},
    "AIDA": {
       "VoxEL":"Systems_ALL/AIDA_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/AIDA_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/AIDA_ACE_ALL.ttl"},
    "FREMENER": {
       "VoxEL":"Systems_ALL/FREMENER_VoxEL_ALL.ttl",
       "KORE50":"Systems_ALL/FREMENER_KORE50_ALL.ttl",
       "ACE04":"Systems_ALL/FREMENER_ACE_ALL.ttl"},
}



Results = {}
for sys_key in WSDSys:
    print("===============",sys_key,"======================")
    sys = WSDSys[sys_key]
    
    for el in SystemsEL:
        print("el:",el)
        
        for db in SystemsEL[el]:
            Results[el] = []
            print("____________\n",db,"\n--------")
            
            #------ All
            file_all = open(SystemsEL[el][db], "r")
            all_t = "".join(file_all.readlines())
            file_all.close()
            
            parser = NIFParser()
            parser.showWarnings = False
            wrp_all = parser.parser_turtle(all_t)
            wrp_all.beSureOnlyOneAnnotation()
            wrp_all.addAlwaysPositionsToUriInSentence = False
            
            
            #======= NWSDT
            fn = SystemsEL[el][db].replace("Systems_ALL", "SystemsResults_with_WSD").replace("_ALL", "_wsdNWSDT")
            file_db = open(fn, "r")
            db_t = "".join(file_db.readlines())
            file_db.close()
            
            parser = NIFParser()
            parser.showWarnings = False
            wrp_db = parser.parser_turtle(db_t)
            wrp_db.beSureOnlyOneAnnotation()
            wrp_db.addAlwaysPositionsToUriInSentence = False
            
            

            wrp_all.mergeWrapper(wrp_db)
            print("All + NWSDT:", fn, "-->", wrp_all.getCantAnnotations())
                
            newName = SystemsEL[el][db].replace("Systems_ALL","Systems_ALL_with_NWSDT")
            file_db_w = open(newName, "w")
            file_db_w.write(wrp_all.toString())
            file_db_w.close()
