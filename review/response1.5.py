__author__ = "Henry Rosales Méndez" 

"""
This script re-annotates the sentences of VoxEL, KORE50 and ACE04-first20 with some EL-systems, in order to response to the reviewer question: Does the system take into account predictions whose span does not correspond to any gold mention?
"""

#from entitylinkingwrapper import Aida, Freme_NER, Babelfy, Tagme, DBpediaSpotlight
from nifwrapper import *
import sys



fout = open("Spans.csv", "w")
foutsysthe = open("Spans_sys_the.csv", "w")
foutgoldthe = open("Spans_gold_the.csv", "w")

fout.write("Gold label; Gold Positions; Gold liks; System Label; System Positions; Syste, links; System; URI Sent\n")
foutsysthe.write("Gold label; Gold Positions; Gold liks; System Label; System Positions; Syste, links; System; URI Sent\n")
foutgoldthe.write("Gold label; Gold Positions; Gold liks; System Label; System Positions; Syste, links; System; URI Sent\n")

#parser = NIFParser()
#parser.showWarnings = False


def overlaps(ag_, as_):
    """
    overlaps but not equal
    """
    if not (ag_["ini"] == as_["ini"] and ag_["fin"] == as_["fin"]):
        if (ag_["ini"]<=as_["ini"] and as_["ini"]<=ag_["fin"]) or (as_["ini"]<=ag_["ini"] and ag_["ini"]<=as_["fin"]):
            return len(ag_["set_url"].intersection(as_["set_url"])) != 0
            
            
    return False
            
            
        


def writeDownOverlapping(urisent_, ann_gold_, ann_sys_, elsys_):
    """
    Whis this function I'm going to 
    """
    global fout
    global foutsysthe
    global foutgoldthe
    
    for agold in ann_gold_:
        for asys in ann_sys_:
            #print("-----------------> ",agold,asys,overlaps(agold, asys))
            if overlaps(agold, asys):
                fout.write(f"{agold['label']};{agold['ini']}-{agold['fin']}; {', '.join(list(agold['set_url']))} ;{asys['label']};{asys['ini']}-{asys['fin']}; {', '.join(list(asys['set_url']))}; {elsys_}; {urisent_}\n")
                
                if asys["label"][:3] == "the"  or asys["label"][:3] == "The":
                    foutsysthe.write(f"{agold['label']};{agold['ini']}-{agold['fin']}; {', '.join(list(agold['set_url']))} ;{asys['label']};{asys['ini']}-{asys['fin']}; {', '.join(list(asys['set_url']))}; {elsys_}; {urisent_}\n")

                if agold["label"][:3] == "the"  or agold["label"][:3] == "The":
                    foutgoldthe.write(f"{agold['label']};{agold['ini']}-{agold['fin']}; {', '.join(list(agold['set_url']))} ;{asys['label']};{asys['ini']}-{asys['fin']}; {', '.join(list(asys['set_url']))}; {elsys_}; {urisent_}\n")


if __name__ == "__main__":

    ###
    ###   Searching for partial matches between gold and systems that are not already in the gold 
    ###   (because our gold is overlaped). También busco menciones annotadas que empiecen con "the"
    ###

    db2filename_systems = {
        "VoxEL" : [("AIDA", "../SystemsResults/AIDA_VoxEL.ttl"), ("Babelfyr","../SystemsResults/BABELFYr_VoxEL.ttl"), ("Babelfys", "../SystemsResults/BABELFYs_VoxEL.ttl"), ("DBps","../SystemsResults/DBpediaSpotlight_VoxEL.ttl"), ("FREMENER", "../SystemsResults/FREMENER_VoxEL.ttl"), ("TAGME","../SystemsResults/TAGME_VoxEL.ttl")],
        
        "KORE50": [("AIDA", "../SystemsResults/AIDA_KORE50.ttl"), ("Babelfyr","../SystemsResults/BABELFYr_KORE50.ttl"), ("Babelfys", "../SystemsResults/BABELFYs_KORE50.ttl"), ("DBps","../SystemsResults/DBpediaSpotlight_KORE50.ttl"), ("FREMENER", "../SystemsResults/FREMENER_KORE50.ttl"), ("TAGME","../SystemsResults/TAGME_KORE50.ttl")],
        
        
        "ACE": [("AIDA", "../SystemsResults/AIDA_ACE.ttl"), ("Babelfyr","../SystemsResults/BABELFYr_ACE.ttl"), ("Babelfys", "../SystemsResults/BABELFYs_ACE.ttl"), ("DBps","../SystemsResults/DBpediaSpotlight_ACE.ttl"), ("FREMENER", "../SystemsResults/FREMENER_ACE.ttl"), ("TAGME","../SystemsResults/TAGME_ACE.ttl")],

     }
    
    db2gold = {
        "VoxEL": "../Gold/2019_05_19_VoxEL.ttl",
        "KORE50": "../Gold/2019_05_19_KORE50.ttl",
        "ACE": "../Gold/2019_05_21_ACE04.ttl",
        }
    
    
    for db_key in db2filename_systems:
        print(db_key)
        Systems = db2filename_systems[db_key]
            
        sys2wrp = {}
        for s, filename in Systems:
            parser = NIFParser()
            parser.showWarnings = False
            sys2wrp[s] = parser.parser_turtle("\n".join(open(filename,"r").readlines()))

        nif_text = "".join(open(db2gold[db_key],"r").readlines())
        parser = NIFParser()
        parser.showWarnings = False
        wrp_gold = parser.parser_turtle(nif_text)
        
        for doc in wrp_gold.documents:
            uridoc = doc.uri
            for sent in doc.sentences:
                urisent = sent.uri
                
                ann_gold = [{
                    "label": a.getAttribute("nif:anchorOf"),
                    "ini": int(a.getAttribute("nif:beginIndex")),
                    "fin": int(a.getAttribute("nif:endIndex")),
                    "set_url": set(a.getUrlList())
                } for a in sent.annotations]

                sgold = set([])
                Dgold = {}
                for x in ann_gold:
                    tup = (x["ini"], x["fin"], x["label"])
                    sgold.update([tup])
                    Dgold[tup] = x

                for elsys in sys2wrp:
                    wrp_sys = sys2wrp[elsys]
                    if uridoc in wrp_sys.dictD:
                        idxdoc = wrp_sys.dictD[uridoc]
                        
                        S = wrp_sys.documents[idxdoc].dictS
                        if urisent in S:
                            idxsent = wrp_sys.documents[idxdoc].dictS[urisent]
                            syssent = wrp_sys.documents[idxdoc].sentences[idxsent]
                            
                            ann_sys = [{
                                "label": a.getAttribute("nif:anchorOf"),
                                "ini": int(a.getAttribute("nif:beginIndex")),
                                "fin": int(a.getAttribute("nif:endIndex")),
                                "set_url": set(a.getUrlList())
                            } for a in syssent.annotations]
                            
                            
                            ssys = set([])
                            Dsys = {}
                            for x in ann_sys:
                                tup = (x["ini"], x["fin"], x["label"])
                                ssys.update([tup])
                                Dsys[tup] = x
                            
                            difsys = ssys.difference(sgold)
                            writeDownOverlapping(urisent, [Dgold[x] for x in sgold],[Dsys[x] for x in difsys], elsys)

                        else:
                            print(f"[Warning] sentence <{uridoc}> does not apear in the {elsys} solution in document <{uridoc}>.")
                            sys.exit()
                    else:
                        print(f"[Warning] document <{uridoc}> does not apear in the {elsys} solution.")
                        sys.exit()

fout.close()
foutsysthe.close()
foutgoldthe.close()
