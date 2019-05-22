#!/usr/bin/python3
# -*- coding: utf-8 -*-

##
#  Author: Henry Rosales Méndez
#  
#  Description: This script generate a the latex file 'Table3-categories.tex', which contains 
#      Tables 4, 5 and 6 of our paper. These tables show the behavior of five selected systems on 
#      our re-annotated and labeled datasets. In the validation stage, all the annotations from the systems
#      that don't have a corresponding annotation in the gold standard -- same initial and final 
#      position -- were deleted (as GERBIL). 
#
#




from nifwrapper import *
import pickle

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

'''
LEN = {}
H = {}
for c in Categories:
    print("cat:",c)
    H[c] = {}
    for gold_k in Datasets:
        H[c][gold_k] = {}
        for sys_k in Systems:
            if not gold_k in LEN:
                LEN[gold_k] = {}
            LEN[gold_k][c] = {}
            
            ## -- Loading gold standard
            file_gold = open(Datasets[gold_k], "r")
            gold_t = "".join(file_gold.readlines())
            file_gold.close()
            
            parser = NIFParser()
            parser.showWarnings = False
            wrp_gold = parser.parser_turtle(gold_t)
            
            
            ## -- 
            wrp_gold.KeepOnlyTag(c)
            
            #fn = "TTT_f/CAT_U_"+c+"_"+sys_k+"_"+gold_k+".ttl"
            #fn = fn.replace(":","_")
            #fcat = open(fn,"w")
            #fcat.write(wrp_gold.toString())
            #fcat.close()
            
            
            wrp_gold.beSureOnlyOneAnnotation()
            LEN[gold_k][c][sys_k] = wrp_gold.getCantAnnotations()
            
            ## -- Loading system results
            file_system = open(Systems[sys_k][gold_k], "r")
            system_t = "".join(file_system.readlines())
            file_system.close()

            parser_s = NIFParser()
            parser_s.showWarnings = False
            wrp_sys = parser_s.parser_turtle(system_t)
            wrp_sys.beSureOnlyOneAnnotation()
            
            wrp_sys.KeepOnlyAnnotationsOf(wrp_gold)
            
            ##-- Benchmark
            bmk = NIFBenchmark(wrp_sys, wrp_gold)
            
            recall_score = bmk.microF()
            H[c][gold_k][sys_k] = recall_score
            
'''
#pickle.dump([H,LEN], open('Table3-categories.pkl', 'wb') )
[H,LEN] = pickle.load(open('Table3-categories.pkl', 'rb'))


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
    "el:Ref-Related":"Related",
    "el:Ref-Descriptive":"Descriptive"
}


fout = open("Table3-categories.tex","w")
fout.write("""
\\documentclass{article}
\\usepackage[margin=0.5in]{geometry}
\\usepackage[utf8]{inputenc}
\\usepackage{textcomp}
\\usepackage{comment}
\\usepackage{pgfplots}
\\usepackage{booktabs} 
\\usepackage{multirow}

\\newcommand{\\hlzero}{\\cellcolor{white}}
\\newcommand{\\hlone}{\\cellcolor{black!3}}
\\newcommand{\\hltwo}{\\cellcolor{black!6}}
\\newcommand{\\hlthree}{\\cellcolor{black!9}}
\\newcommand{\\hlfour}{\\cellcolor{black!12}}
\\newcommand{\\hlfive}{\\cellcolor{black!15}}
\\newcommand{\\hlsix}{\\cellcolor{black!18}}
\\newcommand{\\hlseven}{\\cellcolor{black!21}}
\\newcommand{\\hleight}{\\cellcolor{black!24}}
\\newcommand{\\hlnine}{\\cellcolor{black!27}}
\\newcommand{\\hlten}{\\cellcolor{black!30}}

\\newcommand{\\ccell}[1]{\\multicolumn{1}{c}{#1}}
\\newcommand{\\rcell}[1]{\\multicolumn{1}{r}{#1}}
\\newcommand{\\lcell}[1]{\\multicolumn{1}{l}{#1}}
\\newcommand{\\tcell}[1]{\\multicolumn{3}{c}{#1}}

\\usepackage{times}
\\usepackage{latexsym}
\\usepackage{url}
\\usepackage{mdframed}
\\usepackage{inconsolata}
\\usepackage{fancyvrb}
\\usepackage{graphicx}
\\usepackage{amsmath}
\\usepackage{colortbl}
\\newcommand{\\argmin}{\\arg\\!\\min}
\\newcommand{\\argmax}{\\arg\\!\\max}
\\usepackage{amssymb}
\\usepackage{pifont}
\\newcommand{\\cmark}{\\ding{51}}
\\newcommand{\\xmark}{\\ding{55}}
\\usepackage{booktabs} 
\\usepackage{multirow}
\\usepackage{soul} %middleline
\\usepackage{pgfplots}
\\usepackage{float}
\\usepackage{ulem}


\\pgfplotsset{width=9cm,compat=1.9}

\\begin{document}
""")

def colorI(v):
    if v<0.1: return "\\hlzero"
    if v>=0.1 and v<0.2: return "\\hlone"
    if v>=0.2 and v<0.3: return "\\hltwo"
    if v>=0.3 and v<0.4: return "\\hlthree"
    if v>=0.4 and v<0.5: return "\\hlfour"
    if v>=0.5 and v<0.6: return "\\hlfive"
    if v>=0.6 and v<0.7: return "\\hlsix"
    if v>=0.7 and v<0.8: return "\\hlseven"
    if v>=0.8 and v<0.9: return "\\hleight"
    if v>=0.9: return "\\hlnine"
        

for gold_k in Datasets:
    print("gold_k -->",gold_k)
    txtP = ""
    txtR = ""
    txtF = ""
    txtU = ""

    for c in H:
        babelfy = 0
        tagme = 0
        db = 0
        aida = 0
        freme = 0
        #for gold_k in H[c]:
        line = gold_k
        
        babelfyr =  H[c][gold_k]["Babelfyr"]
        #print("babelfyr:",babelfyr)
        
        babelfys =  H[c][gold_k]["Babelfys"]
        #print("babelfys:",babelfys)
        
        tagme =  H[c][gold_k]["TagME"]
        #print("tagme:",tagme)
        
        db = H[c][gold_k]["DBpSpotlight"]
        #print("db:",db)
        
        aida = H[c][gold_k]["AIDA"]
        #print("aida:",aida)
        
        freme = H[c][gold_k]["FREMENER"]
        #print("freme:",freme)

        print('LEN[gold_k]',LEN[gold_k])
        txtU = (txtU +  cat2label[c].ljust(20) + 
            "\n &"+str(round((LEN[gold_k][c]["FREMENER"]),2)).ljust(7)+    
            "\n &"+colorI(babelfys["precision"])+" "+str(round((babelfys["precision"]),2)).ljust(7) + 
            "\n &"+colorI(babelfys["recall"])+" "+str(round((babelfys["recall"]),2)).ljust(7) + 
            "\n &"+colorI(babelfys["f1"])+" "+str(round((babelfys["f1"]),2)).ljust(7) + 
            " "+
            "\n &"+colorI(babelfyr["precision"])+" "+str(round((babelfyr["precision"]),2)).ljust(7) +
            "\n &"+colorI(babelfyr["recall"])+" "+str(round((babelfyr["recall"]),2)).ljust(7) +
            "\n &"+colorI(babelfyr["f1"])+" "+str(round((babelfyr["f1"]),2)).ljust(7) +
            " "+
            "\n &"+colorI(tagme["precision"])+" "+str(round((tagme["precision"]),2)).ljust(7) + 
            "\n &"+colorI(tagme["recall"])+" "+str(round((tagme["recall"]),2)).ljust(7) + 
            "\n &"+colorI(tagme["f1"])+" "+str(round((tagme["f1"]),2)).ljust(7) + 
            " "+
            "\n &"+colorI(db["precision"])+" "+str(round((db["precision"]),2)).ljust(7) + 
            "\n &"+colorI(db["recall"])+" "+str(round((db["recall"]),2)).ljust(7) + 
            "\n &"+colorI(db["f1"])+" "+str(round((db["f1"]),2)).ljust(7) + 
            " "+
            "\n &"+colorI(aida["precision"])+" "+str(round((aida["precision"]),2)).ljust(7) + 
            "\n &"+colorI(aida["recall"])+" "+str(round((aida["recall"]),2)).ljust(7) + 
            "\n &"+colorI(aida["f1"])+" "+str(round((aida["f1"]),2)).ljust(7) + 
            " " +
            "\n &"+colorI(freme["precision"])+" "+str(round((freme["precision"]),2)).ljust(7) + 
            "\n &"+colorI(freme["recall"])+" "+str(round((freme["recall"]),2)).ljust(7) + 
            "\n &"+colorI(freme["f1"])+" "+str(round((freme["f1"]),2)).ljust(7) +  
            "\\\\")
        
        tt = "\n"
        if c in set(["el:Mnt-ProForm", "el:PoS-Adverb", "el:Olp-Minimal"]):
            tt = "\\midrule\n"
        txtU = txtU + tt;

    fout.write("""

\\begin{table*}[th]
\\centering
\\caption{Precision, Recall and $F_1$ of Babelfy, TagME, DBpedia Spotlight, AIDA and FREME on the """)
    fout.write(gold_k)
    fout.write(""" dataset.
\\label{tab:dbs_precision}}
\\resizebox{1\\textwidth}{!}{
    \\begin{tabular}{lrrrrrrrrrrrrrrrrrrr}
            \\toprule
            \\ccell{} & \\ccell{\\textbf{$|A|$}}&\\tcell{\\textbf{ B$_s$}} &\\tcell{\\textbf{ B$_r$}} &\\tcell{\\textbf{T}} 
            &\\tcell{\\textbf{D}} &\\tcell{\\textbf{A}} &\\tcell{\\textbf{F}}\\\\ \\midrule
            \\ccell{} & \\ccell{}& \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}} & \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}}& \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}}& \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}}& \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}}& \\ccell{\\textbf{P}} & \\ccell{\\textbf{R}} & \\ccell{\\textbf{F$_1$}} \\\\ \\midrule
    """+txtU+"""
        \\bottomrule
    \\end{tabular}
}
\\end{table*}
    """)

fout.write("\\end{document}")
fout.close()
