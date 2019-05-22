#!/usr/bin/python3
# -*- coding: utf-8 -*-


from nifwrapper import *
import pickle


##
# Author: Henry Rosales Méndez
# ------
#
# Description: 
# -----------
# - Skipping combinations that yield gold standard without annotations.
# - Unifiying dataset
# - Eliminating annotations from the system result that don't have corresponding
#   annotations in the gold standard (As Gerbil)
#

cat2membership = {
    "el:Mnt-Full":0.5536,
    "el:Mnt-Short":0.6677777778,
    "el:Mnt-Extended":0.5536,
    "el:Mnt-Alias":0.7766666667,
    "el:Mnt-NumericTemporal":0.28,
    "el:Mnt-CommonForm":0.1540909091,
    "el:Mnt-ProForm":0.475,
    "el:PoS-NounSingular":0.5036574074,
    "el:PoS-NounPlural":0.3326984127,
    "el:PoS-Adjective":0.2544444444,
    "el:PoS-Verb":0.06142857143,
    "el:PoS-Adverb":0.2544444444,
    "el:Olp-None":0.3478205128,
    "el:Olp-Maximal":0.6798148148,
    "el:Olp-Intermediate":0.2709259259,
    "el:Olp-Minimal":0.2709259259,
    "el:Ref-Direct":0.3702287582,
    "el:Ref-Anaphoric":0.4833333333,
    "el:Ref-Metaphoric":0.125,
    "el:Ref-Metonymic":0.7777777778,
    "el:Ref-Related":0.7777777778,
    "el:Ref-Descriptive":0.7777777778,
}

Categories = ["el:Mnt-Full", "el:Mnt-Short", "el:Mnt-Extended", "el:Mnt-Alias", "el:Mnt-NumericTemporal", "el:Mnt-CommonForm", "el:Mnt-ProForm", "el:PoS-NounSingular", "el:PoS-NounPlural", "el:PoS-Adjective", "el:PoS-Verb", "el:PoS-Adverb", "el:Olp-None", "el:Olp-Maximal", "el:Olp-Intermediate", "el:Olp-Minimal", "el:Ref-Direct", "el:Ref-Anaphoric", "el:Ref-Metaphoric", "el:Ref-Metonymic", "el:Ref-Related", "el:Ref-Descriptive"] 

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



group2listCat = {
    0:["el:Mnt-Full", "el:Mnt-Short", "el:Mnt-Extended", "el:Mnt-Alias", "el:Mnt-NumericTemporal", "el:Mnt-CommonForm", "el:Mnt-ProForm"],
    1:["el:PoS-NounSingular", "el:PoS-NounPlural", "el:PoS-Adjective", "el:PoS-Verb", "el:PoS-Adverb"],
    2:["el:Olp-None", "el:Olp-Maximal", "el:Olp-Intermediate", "el:Olp-Minimal"],
    3:["el:Ref-Direct", "el:Ref-Anaphoric", "el:Ref-Metaphoric", "el:Ref-Metonymic", "el:Ref-Related", "el:Ref-Descriptive"]
}

list_len = [7,5,4,6]

#number of variations: 7*5*4*6 = 840
catCombined = []
L = [-1,-1,-1,-1]
cant = 0
def rec_comb(p):
    global catCombined
    global L
    global cant
    
    if (p == 4):
        t = 0
        Lt = []
        for x in L:
            Lt.append(group2listCat[t][x])
            t = t + 1
        catCombined.append(Lt)
        cant = cant + 1
    elif L[p] < list_len[p]:
        for i in range(list_len[p]):
            L[p] = L[p] + 1
            rec_comb(p+1)
    if p<4:
        L[p] = -1
rec_comb(0)

        
asGerbil = True
asGerbil_text = ""
if asGerbil:
    asGerbil_text = "As Gerbil"

H = {}
cant = 0
for Ltag in catCombined:
    c = "_".join(Ltag)
    cant = cant + 1
    print(cant,"--> ",c)
    H[c] = {}
    for gold_k in Datasets:
        H[c][gold_k] = {}
        for sys_k in Systems:
            
            ## -- Loading gold standard
            file_gold = open(Datasets[gold_k], "r")
            gold_t = "".join(file_gold.readlines())
            file_gold.close()
            
            parser = NIFParser()
            parser.showWarnings = False
            wrp_gold = parser.parser_turtle(gold_t)
            
            
            ## -- 
            wrp_gold.KeepOnlyListTag(Ltag)
            if wrp_gold.getCantAnnotations() == 0:
                continue
            #fn = "comb_test.ttl"
            #fn = fn.replace(":","_")
            #fcat = open(fn,"w")
            #fcat.write(wrp_gold.toString())
            #fcat.close()
            
            wrp_gold.beSureOnlyOneAnnotation()
            
            ## -- Loading system results
            file_system = open(Systems[sys_k][gold_k], "r")
            system_t = "".join(file_system.readlines())
            file_system.close()

            parser_s = NIFParser()
            parser_s.showWarnings = False
            wrp_sys = parser_s.parser_turtle(system_t)
            wrp_sys.beSureOnlyOneAnnotation()
            if asGerbil:
                wrp_sys.KeepOnlyAnnotationsOf(wrp_gold)
            
            ##-- Benchmark
            wrp_gold.setMembershipAttribute(cat2membership)
            bmk = NIFBenchmark(wrp_sys, wrp_gold)
            
            sc = {"microF1":bmk.microF()}
            H[c][gold_k][sys_k] = sc


#pickle.dump(H,  open('Figure4-combinations_of_tags.pkl', 'wb') )
#H = pickle.load(open('Figure4-combinations_of_tags.pkl', 'rb'))


cat2label = {
    "el:Mnt-Full":"Full Mention",
    "el:Mnt-Short":"Short Mention",
    "el:Mnt-Extended":"Extended Mention",
    "el:Mnt-Alias":"Alias",
    "el:Mnt-NumericTemporal":"Numeric/Temporal",
    "el:Mnt-CommonForm":"Common Form",
    "el:Mnt-ProForm":"Pro-form",
    "el:PoS-NounSingular":"Singular Noun",
    "el:PoS-NounPlural":"Plural Noun",
    "el:PoS-Adjective":"Adjective",
    "el:PoS-Verb":"Verb",
    "el:PoS-Adverb":"Adverb",
    "el:Olp-None":"Non-Overlapping",
    "el:Olp-Maximal":"Maximal Overlap",
    "el:Olp-Intermediate":"Intermediate Overlap",
    "el:Olp-Minimal":"Minimal Overlap",
    "el:Ref-Direct":"Direct",
    "el:Ref-Anaphoric":"Anaphoric",
    "el:Ref-Metaphoric":"Metaphoric",
    "el:Ref-Metonymic":"Metonymic",
    "el:Ref-Related":"Approximate",
    "el:Ref-Descriptive":"Descriptive"
}



INV = {}
for c in H:
    for gold_k in H[c]:
        for sys in H[c][gold_k]:
            t = H[c][gold_k][sys]
            
            if not sys in INV:
                INV[sys] = {}
            
            if not gold_k in INV[sys]:
                INV[sys][gold_k] = {}            
            
            
            if not c in INV[sys][gold_k]:
                INV[sys][gold_k][c] = t
            else: 
                input("Error!?")



db2typeline = { "Unified":"solid", "KORE50":"solid", "VoxEL":"solid", "ACE04":"solid"}
db2color    = { "Unified":"blue","KORE50":"blue", "VoxEL":"red", "ACE04":"brown"}

mesure2name ={"microF1": "Recall", "extF":"Recall*"}


fout = open("Figure4-combinations_of_tags.tex","w")
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

#--- Summary

fout.write("\n\n\n%%%%%%%%%%%% Summary Chart %%%%%%%%%%%%%%\n\n")


sys2color = { 
    "Babelfyr": "black",
    "Babelfys": "green",
    "TagME": "blue",
    "DBpSpotlight": "red",
    "AIDA":"violet",
    "FREMENER": "orange"
}

gold2len = dict([ tuple([ x , len(INV["Babelfyr"][x]) ]) for x in INV["Babelfyr"]])

for measure in ["microF1"]:#, "extF"]:
    fout.write("\\begin{figure}[t]\n")
    fout.write("\\label{fig:charts}\n")
    fout.write("\\caption{Precision, Recall and $F_1$ of selected EL systems over the unified datasets for each of the non-empty combination of tags.}")
    fout.write("\\resizebox{\\textwidth}{!}{\n")
    for mm in ["precision", "recall", "f1"]:
        for gold_k in ["Unified"]:#["KORE50","VoxEL","ACE04"]:
            textP = """
\\begin{tikzpicture}
\\begin{axis}[
    title={%s-%s-No accumulative %s},
    xlabel={tags},
    ylabel={%s},
    xmin=0, xmax=%s,
    ymin=0, ymax=1,
    legend pos=north east,
    ymajorgrids=true,
    grid style=dashed,
]\n"""%(mm,gold_k,asGerbil_text,mm,str(gold2len[gold_k]-1))
            for sys in INV:        
                L = [tuple([INV[sys][gold_k][x][measure][mm], x]) for x in INV[sys][gold_k]]
                Ls = sorted(L, key=lambda x: x[0], reverse=True)
                
                textP = textP + "\\addplot[color=%s, mark=none, %s]\n"%(sys2color[sys],db2typeline[gold_k])
                textP = textP + "coordinates {\n"
                textP = textP + "".join([ "(%s,%s)"%(str(i_),str(round(Ls[i_][0],2))) for i_ in range(len(Ls)) ])
                textP = textP + "};\n"
                textP = textP + "\\addlegendentry{%s}\n\n"%(sys)
                
            textP = textP + "\\end{axis}\n"
            textP = textP + "\\end{tikzpicture}\n\n"
            fout.write(textP)
    fout.write("}\n")
    fout.write("\\end{figure}\n")




fout.write("\n\n\n%%%%%%%%%%%% Acumulado %%%%%%%%%%%%%%\n\n")

for measure in ["microF1"]:#, "extF"]:
    fout.write("\\begin{figure}[t]\n")
    fout.write("\\resizebox{\\textwidth}{!}{\n")
    for mm in ["precision", "recall", "f1"]:
        for gold_k in ["Unified"]:
            textP = """
    \\begin{tikzpicture}
    \\begin{axis}[
        title={Acumulado %s-%s %s},
        xlabel={tags},
        ylabel={%s},
        xmin=0, xmax=%s,
        ymin=0, ymax=1,
        legend pos=north east,
        ymajorgrids=true,
        grid style=dashed,
    ]\n"""%(mm,gold_k,asGerbil_text,mm,str(gold2len[gold_k]-1))
            print("-----> gold_k:",gold_k)
            for sys in INV:  
                print("=> sys:",sys)
                sys_k = sys
                L = [tuple([INV[sys][gold_k][x][measure][mm], x]) for x in INV[sys][gold_k]]
                Ls = sorted(L, key=lambda x: x[0], reverse=True)
                
                #--------- Agregando           
                L_Agregated = []
                L_Ltags = []
                for i_ in range(len(Ls)):
                    
                    Ltag = Ls[i_][1].split("_")
                    L_Ltags.append(Ltag)
                    
                    ## -- Loading gold standard
                    file_gold = open(Datasets[gold_k], "r")
                    gold_t = "".join(file_gold.readlines())
                    file_gold.close()
                    
                    parser = NIFParser()
                    parser.showWarnings = False
                    wrp_gold = parser.parser_turtle(gold_t)
                    
                    
                    wrp_gold.KeepOnlyListOfListTag(L_Ltags)
                    wrp_gold.beSureOnlyOneAnnotation()
                    
                    
                    #fn = "comb_test.ttl"
                    #fcat = open(fn,"w")
                    #fcat.write(wrp_gold.toString())
                    #fcat.close()
                    
                    
                    ## -- Loading system results
                    file_system = open(Systems[sys_k][gold_k], "r")
                    system_t = "".join(file_system.readlines())
                    file_system.close()

                    parser_s = NIFParser()
                    parser_s.showWarnings = False
                    wrp_sys = parser_s.parser_turtle(system_t)
                    wrp_sys.beSureOnlyOneAnnotation()
                    
                    if asGerbil:
                        wrp_sys.KeepOnlyAnnotationsOf(wrp_gold)
                    
                    ##-- Benchmark
                    wrp_gold.setMembershipAttribute(cat2membership)
                    bmk = NIFBenchmark(wrp_sys, wrp_gold)
                    
                    sc = bmk.microF()
                    L_Agregated.append(tuple([sc[mm],Ls[i_][1]]))


                Ls = [x for x in L_Agregated]
                
                textP = textP + "\\addplot[color=%s, mark=none, %s]\n"%(sys2color[sys],db2typeline[gold_k])
                textP = textP + "coordinates {\n"
                textP = textP + "".join([ "(%s,%s)"%(str(i_),str(round(Ls[i_][0],2))) for i_ in range(len(Ls)) ])
                textP = textP + "};\n"
                textP = textP + "\\addlegendentry{%s}\n\n"%(sys)
            textP = textP + "\\end{axis}\n"
            textP = textP + "\\end{tikzpicture}\n\n"
            fout.write(textP)

    fout.write("}\n")
    fout.write("\\end{figure}\n")


fout.write("\\end{document}")
fout.close()
