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

Categories = ["el:Mnt-Full", "el:Mnt-Short", "el:Mnt-Extended", "el:Mnt-Alias", "el:Mnt-NumericTemporal", "el:Mnt-CommonForm", "el:Mnt-ProForm", "el:PoS-NounSingular", "el:PoS-NounPlural", "el:PoS-Adjective", "el:PoS-Verb", "el:PoS-Adverb", "el:Olp-None", "el:Olp-Maximal", "el:Olp-Intermediate", "el:Olp-Minimal", "el:Ref-Direct", "el:Ref-Anaphoric", "el:Ref-Metaphoric", "el:Ref-Metonymic", "el:Ref-Related", "el:Ref-Descriptive", "All"]



Datasets = {
    "KORE50":"Gold/2019_05_19_KORE50.ttl", 
    "VoxEL": "Gold/2019_05_19_VoxEL.ttl",
    "ACE04": "Gold/2019_05_21_ACE04.ttl"
}


# Systems Results, plus Coreference and WSD annotations
#Name_t = "ALL"
Systems_ALL = {
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



# Systems wsdNLTK
Systems_WSD = {
    "Babelfyr": {
        "VoxEL":"SystemsResults_with_WSD/BABELFYr_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/BABELFYr_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/BABELFYr_ACE_wsdNLTK.ttl"},
    "Babelfys": {
        "VoxEL":"SystemsResults_with_WSD/BABELFYs_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/BABELFYs_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/BABELFYs_ACE_wsdNLTK.ttl"},
    "TagME": {
        "VoxEL":"SystemsResults_with_WSD/TAGME_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/TAGME_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/TAGME_ACE_wsdNLTK.ttl"},
    "DBpSpotlight": {
        "VoxEL":"SystemsResults_with_WSD/DBpediaSpotlight_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/DBpediaSpotlight_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/DBpediaSpotlight_ACE_wsdNLTK.ttl"},
    "AIDA": {
        "VoxEL":"SystemsResults_with_WSD/AIDA_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/AIDA_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/AIDA_ACE_wsdNLTK.ttl"},
    "FREMENER": {
        "VoxEL":"SystemsResults_with_WSD/FREMENER_VoxEL_wsdNLTK.ttl",
        "KORE50":"SystemsResults_with_WSD/FREMENER_KORE50_wsdNLTK.ttl",
        "ACE04":"SystemsResults_with_WSD/FREMENER_ACE_wsdNLTK.ttl"},
}



# Systems NeuralCoref 
Systems_NCR = {
    "Babelfyr": {
        "VoxEL":"SystemsResults_with_Coref/BABELFYr_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/BABELFYr_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/BABELFYr_ACE_NeuralCoref.ttl"},
    "Babelfys": {
        "VoxEL":"SystemsResults_with_Coref/BABELFYs_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/BABELFYs_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/BABELFYs_ACE_NeuralCoref.ttl"},
    "TagME": {
        "VoxEL":"SystemsResults_with_Coref/TAGME_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/TAGME_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/TAGME_ACE_NeuralCoref.ttl"},
    "DBpSpotlight": {
        "VoxEL":"SystemsResults_with_Coref/DBpediaSpotlight_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/DBpediaSpotlight_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/DBpediaSpotlight_ACE_NeuralCoref.ttl"},
    "AIDA": {
        "VoxEL":"SystemsResults_with_Coref/AIDA_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/AIDA_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/AIDA_ACE_NeuralCoref.ttl"},
    "FREMENER": {
        "VoxEL":"SystemsResults_with_Coref/FREMENER_VoxEL_NeuralCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/FREMENER_KORE50_NeuralCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/FREMENER_ACE_NeuralCoref.ttl"},
}




# Systems CoreNLPCoref
Systems_SCR = {
    "Babelfyr": {
        "VoxEL":"SystemsResults_with_Coref/BABELFYr_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/BABELFYr_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/BABELFYr_ACE_CoreNLPCoref.ttl"},
    "Babelfys": {
        "VoxEL":"SystemsResults_with_Coref/BABELFYs_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/BABELFYs_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/BABELFYs_ACE_CoreNLPCoref.ttl"},
    "TagME": {
        "VoxEL":"SystemsResults_with_Coref/TAGME_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/TAGME_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/TAGME_ACE_CoreNLPCoref.ttl"},
    "DBpSpotlight": {
        "VoxEL":"SystemsResults_with_Coref/DBpediaSpotlight_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/DBpediaSpotlight_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/DBpediaSpotlight_ACE_CoreNLPCoref.ttl"},
    "AIDA": {
        "VoxEL":"SystemsResults_with_Coref/AIDA_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/AIDA_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/AIDA_ACE_CoreNLPCoref.ttl"},
    "FREMENER": {
        "VoxEL":"SystemsResults_with_Coref/FREMENER_VoxEL_CoreNLPCoref.ttl",
        "KORE50":"SystemsResults_with_Coref/FREMENER_KORE50_CoreNLPCoref.ttl",
        "ACE04":"SystemsResults_with_Coref/FREMENER_ACE_CoreNLPCoref.ttl"},
}


##--- Unificar Gold Standard

def colorV(v):
    ch = "i"
    if v < 0:
        ch = "d"
        v = -v
    if v < 0.01: return "\\hlzero"
    if v>=0.01 and v<0.09: return "\\"+ch+"hlone"
    if v>=0.09 and v<0.19: return "\\"+ch+"hltwo"
    if v>=0.19 and v<0.29: return "\\"+ch+"hlthree"
    if v>=0.29 and v<0.39: return "\\"+ch+"hlfour"
    if v>=0.39 and v<0.49: return "\\"+ch+"hlfive"
    if v>=0.49 and v<0.59: return "\\"+ch+"hlsix"
    if v>=0.59 and v<0.69: return "\\"+ch+"hlseven"
    if v>=0.69 and v<0.79: return "\\"+ch+"hleight"
    return "\\"+ch+"hlnine"


def colorI(H,t,measure):
    global H_bl
    value = H[t[0]][t[1]][t[2]][measure]
    tab4 = H_bl[t[0]][t[1]][t[2]][measure] 
    
    if not t[0] in H_bl:
        return colorV(0)
    dif = value - tab4
    return colorV(dif)

def pp(H,t,measure):
    value = H[t[0]][t[1]][t[2]][measure]
    tt = str(round(value,2))
    if len(tt) == 1:
        tt = tt + ".00"
    elif len(tt) == 3:
        tt = tt + "0"
    return tt

fgoldUnified = open("goldUnified.ttl","w")
for g in Datasets:
    file_gold = open(Datasets[g], "r")
    gold_t = "".join(file_gold.readlines())
    fgoldUnified.write(gold_t)
    
fgoldUnified.close()

Datasets = {"Unified":"goldUnified.ttl"}

for Systems_t in [(Systems_ALL, "ALL", "Table8.tex"),
                  (Systems_WSD, "WSD", "Table7.tex"),
                  (Systems_NCR, "NCR", "Table6.tex"),
                  (Systems_SCR, "SCR", "Table5.tex")]: 
    
    Systems = Systems_t[0]
    Name_t = Systems_t[1]
    filename_table = Systems_t[2]

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


    LEN = {}
    H = {}
    for c in Categories:
        print("------------------cat:",c)
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
                if c != "All":
                    wrp_gold.KeepOnlyTag(c)
                
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
                
    [H_bl,LEN_1] = pickle.load(open('Table3-categories_baseline.pkl', 'rb'))

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
        "el:Ref-Descriptive":"Descriptive",
        "All": "All"
    }


    fout = open(filename_table,"w")
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

    \\newcommand{\\ihlzero}{\\cellcolor{white}}
    \\newcommand{\\ihlone}{\\cellcolor{blue!3}}
    \\newcommand{\\ihltwo}{\\cellcolor{blue!6}}
    \\newcommand{\\ihlthree}{\\cellcolor{blue!9}}
    \\newcommand{\\ihlfour}{\\cellcolor{blue!12}}
    \\newcommand{\\ihlfive}{\\cellcolor{blue!15}}
    \\newcommand{\\ihlsix}{\\cellcolor{blue!18}}
    \\newcommand{\\ihlseven}{\\cellcolor{blue!21}}
    \\newcommand{\\ihleight}{\\cellcolor{blue!24}}
    \\newcommand{\\ihlnine}{\\cellcolor{blue!27}}
    \\newcommand{\\ihlten}{\\cellcolor{blue!30}}


    \\newcommand{\\dhlzero}{\\cellcolor{white}}
    \\newcommand{\\dhlone}{\\cellcolor{red!3}}
    \\newcommand{\\dhltwo}{\\cellcolor{red!6}}
    \\newcommand{\\dhlthree}{\\cellcolor{red!9}}
    \\newcommand{\\dhlfour}{\\cellcolor{red!12}}
    \\newcommand{\\dhlfive}{\\cellcolor{red!15}}
    \\newcommand{\\dhlsix}{\\cellcolor{red!18}}
    \\newcommand{\\dhlseven}{\\cellcolor{red!21}}
    \\newcommand{\\dhleight}{\\cellcolor{red!24}}
    \\newcommand{\\dhlnine}{\\cellcolor{red!27}}
    \\newcommand{\\dhlten}{\\cellcolor{red!30}}


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
            
            babelfyr =  tuple([c,gold_k,"Babelfyr"])
            #print("babelfyr:",babelfyr)
            
            babelfys =  tuple([c,gold_k,"Babelfys"])  #H[c][gold_k]["Babelfys"]
            #print("babelfys:",babelfys)
            
            tagme =  tuple([c,gold_k,"TagME"])
            #print("tagme:",tagme)
            
            db = tuple([c,gold_k,"DBpSpotlight"])
            #print("db:",db)
            
            aida = tuple([c,gold_k,"AIDA"])
            #print("aida:",aida)
            
            freme = tuple([c,gold_k,"FREMENER"])
            #print("freme:",freme)

            txtU = (txtU +  cat2label[c].ljust(20) + 
                "\n &"+str(round((LEN[gold_k][c]["FREMENER"]),2)).ljust(7)+    
                "\n &"+colorI(H,babelfys,"precision",)+" "+pp(H,babelfys,"precision") + 
                "\n &"+colorI(H,babelfys,"recall")+" "+pp(H,babelfys,"recall") + 
                "\n &"+colorI(H,babelfys,"f1")+" "+pp(H,babelfys,"f1") + 
                " "+
                "\n &"+colorI(H,babelfyr,"precision")+" "+pp(H,babelfyr,"precision") +
                "\n &"+colorI(H,babelfyr,"recall")+" "+pp(H,babelfyr,"recall") +
                "\n &"+colorI(H,babelfyr,"f1")+" "+pp(H,babelfyr,"f1") +
                " "+
                "\n &"+colorI(H,tagme,"precision")+" "+pp(H,tagme,"precision") + 
                "\n &"+colorI(H,tagme,"recall")+" "+pp(H,tagme,"recall") + 
                "\n &"+colorI(H,tagme,"f1")+" "+pp(H,tagme,"f1")+ 
                " "+
                "\n &"+colorI(H,db,"precision")+" "+pp(H,db,"precision") + 
                "\n &"+colorI(H,db,"recall")+" "+pp(H,db,"recall") + 
                "\n &"+colorI(H,db,"f1")+" "+pp(H,db,"f1") + 
                " "+
                "\n &"+colorI(H,aida,"precision")+" "+pp(H,aida,"precision") + 
                "\n &"+colorI(H,aida,"recall")+" "+pp(H,aida,"recall") + 
                "\n &"+colorI(H,aida,"f1")+" "+pp(H,aida,"f1") + 
                " " +
                "\n &"+colorI(H,freme,"precision")+" "+pp(H,freme,"precision") + 
                "\n &"+colorI(H,freme,"recall")+" "+pp(H,freme,"recall") + 
                "\n &"+colorI(H,freme,"f1")+" "+pp(H,freme,"f1") +  
                "\\\\")
            
            tt = "\n"
            if c in set(["el:Mnt-ProForm", "el:PoS-Adverb", "el:Olp-Minimal"]):
                tt = "\\midrule\n"
            txtU = txtU + tt;

        fout.write("""
    \\begin{table*}[th]
    \\centering
    \\caption{(%s) Precision, Recall and $F_1$ of Babelfy, TagME, DBpedia Spotlight, AIDA and FREME on the """ %(Name_t))
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
