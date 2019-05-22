#!/usr/bin/python3
# -*- coding: utf-8 -*-


from nifwrapper import *
import pickle

Datasets = {
    "KORE50":"Gold/2019_05_19_KORE50.ttl", 
    "VoxEL": "Gold/2019_05_19_VoxEL.ttl",
    "ACE04": "Gold/2019_05_21_ACE04.ttl"
}

Systems = {
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

    

#avg
cat2membership = {
"el:Mnt-Full":0.545,
"el:Mnt-Short":0.361,
"el:Mnt-Extended":0.542,
"el:Mnt-Alias":0.293,
"el:Mnt-NumericTemporal":0.047,
"el:Mnt-CommonForm":0.121,
"el:Mnt-ProForm":0.0,
"el:PoS-NounSingular":0.273,
"el:PoS-NounPlural":0.14,
"el:PoS-Adjective":0.132,
"el:PoS-Verb":0.038,
"el:PoS-Adverb":0.069,
"el:Olp-None":0.217,
"el:Olp-Maximal":0.278,
"el:Olp-Intermediate":0.228,
"el:Olp-Minimal":0.148,
"el:Ref-Direct":0.231,
"el:Ref-Anaphoric":0.02,
"el:Ref-Metaphoric":0.119,
"el:Ref-Metonymic":0.0,
"el:Ref-Related":0.105,
"el:Ref-Descriptive":0.152,
}

H = {}
for sys_k in Systems:
    print("------------------------------------------")
    print("sys_k:",sys_k)
    H[sys_k] = {}
    for gold_k in Datasets:
    
        H[sys_k][gold_k] = {}

        ## -- Loading gold standard
        file_gold = open(Datasets[gold_k], "r")
        gold_t = "".join(file_gold.readlines())
        file_gold.close()
        
        parser = NIFParser()
        parser.showWarnings = False
        wrp_gold = parser.parser_turtle(gold_t)
        wrp_gold.beSureOnlyOneAnnotation()
        wrp_gold.setMembershipAttribute(cat2membership)
        
        ## -- Loading system results
        file_system = open(Systems[sys_k][gold_k], "r")
        system_t = "".join(file_system.readlines())
        file_system.close()

        parser_s = NIFParser()
        parser_s.showWarnings = False
        wrp_sys = parser_s.parser_turtle(system_t)
        wrp_sys.beSureOnlyOneAnnotation()
        
        ##-- Benchmark
        bmk = NIFBenchmark(wrp_sys, wrp_gold)
        bmk.showWarnings = False
        scores = bmk.microF()
        H[sys_k][gold_k]["f1"] = scores
        
        ext = bmk.microExtF1()
        H[sys_k][gold_k]["extF1"] = ext


pickle.dump(H, open('TableAster_notIncludedYet.pkl', 'wb') )
H = pickle.load(open('TableAster_notIncludedYet.pkl', 'rb'))

def pr(t):
    return str( round(t["f1"]["f1"],3) ).ljust(7) + "&" + str(round((t["extF1"]["f1"]),3)).ljust(7)

for sys_k in H:
    kore50 =  H[sys_k]["KORE50"]
    voxel =  H[sys_k]["VoxEL"]
    ace04 =  H[sys_k]["ACE04"]
    
    print(sys_k.ljust(20) + " & " + pr(kore50) +" & "+pr(voxel)+" & "+ pr(ace04) + "\\\\")




