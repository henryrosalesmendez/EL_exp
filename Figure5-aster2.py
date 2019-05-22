#!/usr/bin/python3
# -*- coding: utf-8 -*-

##
#  Author: Henry Rosales Méndez
#  
#  Description: Here I first concatenate the three datasets in only one.
#      In the validation stage, we keep all the annotations from the systems
#      no matter if they don't have a corresponding annotation in the gold standard.
#      (Not as GERBIL)

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




##--- Unificar Gold Standard

fgoldUnified = open("goldUnified.ttl","w")
for g in Datasets:
    file_gold = open(Datasets[g], "r")
    gold_t = "".join(file_gold.readlines())
    fgoldUnified.write(gold_t)
    
fgoldUnified.close()

Datasets = {"Unified":"goldUnified.ttl"}



###--- Unificar systems
Systemst = {}
for sys in Systems:
    fsysUnified = open(sys+"Unified.ttl","w")
    for g in Systems[sys]:
        file_sys = open(Systems[sys][g], "r")
        sys_t = "".join(file_sys.readlines())
        fsysUnified.write(sys_t)    
    fsysUnified.close()
    
    Systemst[sys] = {"Unified": sys+"Unified.ttl"}
    
Systems = Systemst



H = {}

for alpha in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
    H[alpha] = {}
    print("================================")
    print("alpha:",alpha)
    cat2membership = {
        "el:Mnt-Full":1,
        "el:Mnt-Short":1,
        "el:Mnt-Extended":1,
        "el:Mnt-Alias":1,
        "el:Mnt-NumericTemporal":alpha,
        "el:Mnt-CommonForm":alpha,
        "el:Mnt-ProForm":alpha,
        "el:PoS-NounSingular":1,
        "el:PoS-NounPlural":1,
        "el:PoS-Adjective":alpha,
        "el:PoS-Verb":alpha,
        "el:PoS-Adverb":alpha,
        "el:Olp-None":1,
        "el:Olp-Maximal":1,
        "el:Olp-Intermediate":alpha,
        "el:Olp-Minimal":alpha,
        "el:Ref-Direct":1,
        "el:Ref-Anaphoric":alpha,
        "el:Ref-Metaphoric":alpha,
        "el:Ref-Metonymic":alpha,
        "el:Ref-Related":alpha,
        "el:Ref-Descriptive":alpha
    }
    for sys_k in Systems:
        print("------------------------------------------")
        print("sys_k:",sys_k)
        H[alpha][sys_k] = {}
        for gold_k in Datasets:
        
            H[alpha][sys_k][gold_k] = {}
            #print("...................")
            #print("sys_k:",sys_k)
            
            ## -- Loading gold standard
            file_gold = open(Datasets[gold_k], "r")
            gold_t = "".join(file_gold.readlines())
            file_gold.close()
            
            parser = NIFParser()
            parser.showWarnings = False
            wrp_gold = parser.parser_turtle(gold_t)
            wrp_gold.beSureOnlyOneAnnotation()
            wrp_gold.setMembershipAttribute(cat2membership)
            
            ## -- 
            #wrp_gold.KeepOnlyTag(c)
            
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
            print(sys_k+"|f1:",scores)
            H[alpha][sys_k][gold_k]["f1"] = scores
            
            ext = bmk.microExtF1()
            print(sys_k+"|ext:",ext)
            H[alpha][sys_k][gold_k]["extF1"] = ext
            


#pickle.dump(H, open('Figure5-aster2.pkl', 'wb') )
#H = pickle.load(open('Figure5-aster2.pkl', 'rb'))



sys2color = { 
    "Babelfyr": "black",
    "Babelfys": "green",
    "TagME": "blue",
    "DBpSpotlight": "red",
    "AIDA":"violet",
    "FREMENER": "orange"
}

db2typeline = { "Unified":"solid", "KORE50":"solid", "VoxEL":"solid", "ACE04":"solid", "Unified_g":"solid"}


fout = open("Figure5-aster2.tex","w")
fout.write("""
\\documentclass{article}
\\usepackage[margin=0.5in]{geometry}
\\usepackage[utf8]{inputenc}
\\usepackage{textcomp}
\\usepackage{comment}
\\usepackage{pgfplots}
\\usepackage{booktabs} 
\\usepackage{multirow}

\\pgfplotsset{width=9cm,compat=1.9}

\\begin{document}
""")



fout.write("\\begin{figure}[t]\n")
fout.write("\\label{fig:charts}\n")
fout.write("\\caption{Precision, Recall and $F_1$ of selected EL systems over the unified datasets for each of the non-empty combination of tags.}")
fout.write("\\resizebox{\\textwidth}{!}{\n")
textP = """
\\begin{tikzpicture}
\\begin{axis}[
     title={Chart Aster 2},
     xlabel={$\\alpha$},
     ylabel={$F_1^*$},
     xmin=0, xmax=1,
     ymin=0, ymax=1,
     legend pos=north east,
     ymajorgrids=true,
     grid style=dashed,
]\n"""



for sys in Systems:  
    L = []
    for gold_k in Datasets:
        for alpha in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
            L.append(tuple([alpha, H[alpha][sys][gold_k]["extF1"]["f1"]]))
    
    #print("L:",L)
    textP = textP + "\\addplot[color=%s, mark=none, %s]\n"%(sys2color[sys],db2typeline[gold_k])
    textP = textP + "coordinates {\n"
    textP = textP + "".join([ "(%s,%s)"%(str(x[0]),str(x[1])) for x in L])
    textP = textP + "};\n"
    textP = textP + "\\addlegendentry{%s}\n\n"%(sys)
            
textP = textP + "\\end{axis}\n"
textP = textP + "\\end{tikzpicture} \n\n"
fout.write(textP)
fout.write("}\n")
fout.write("\\end{figure}\n")


fout.write("\\end{document}")
fout.close()
