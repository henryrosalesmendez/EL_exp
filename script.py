#!/usr/bin/python3
# -*- coding: utf-8 -*-


from nifwrapper import *

## -- Loading gold standard
file_gold = open("Questionnaire_Gold.ttl", "r")
gold_t = "".join(file_gold.readlines())
file_gold.close()

## -- Loading system results
file_system = open("Questionnaire_System.ttl", "r")
system_t = "".join(file_system.readlines())
file_system.close()

file_system_no_Moscow = open("Questionnaire_System_without_Moscow.ttl", "r")
system_t_no_Moscow = "".join(file_system_no_Moscow.readlines())
file_system_no_Moscow.close()


file_system_no_Russian = open("Questionnaire_System_without_Russian.ttl", "r")
system_t_no_Russian = "".join(file_system_no_Russian.readlines())
file_system_no_Russian.close()



## --------------------- Parsing

parser = NIFParser()
wrp_gold = parser.parser_turtle(gold_t)


#-----
parser = NIFParser()
wrp_sys = parser.parser_turtle(system_t)

parser = NIFParser()
wrp_sys_no_Moscow = parser.parser_turtle(system_t_no_Moscow)

parser = NIFParser()
wrp_sys_no_Russian = parser.parser_turtle(system_t_no_Russian)


## --------------------- Measurement
bmk = NIFBenchmark(wrp_sys, wrp_gold)
bmk_no_Russian = NIFBenchmark(wrp_sys_no_Russian, wrp_gold)
bmk_no_Moscow = NIFBenchmark(wrp_sys_no_Moscow, wrp_gold)

m = {}  # membership function 
m["https://example.org/doc1#char=21,34"] = 1 # Martin Bashir
m["https://example.org/doc1#char=60,87"] = 0.97 # Living with Michael Jackson
m["https://example.org/doc1#char=72,87"] = 0.75 # Michael Jackson
m["https://example.org/doc1#char=93,104"] = 0.97 # King of Pop
m["https://example.org/doc1#char=101,104"] = 0.35 # Pop
m["https://example.org/doc1#char=119,122"] = 1 # Joe
m["https://example.org/doc1#char=162,164"] = 0.57 # he
m["https://example.org/doc1#char=162,186"] = 0.51 # he and his four siblings
m["https://example.org/doc1#char=169,172"] = 0.4 # his
m["https://example.org/doc1#char=0,7"] = 0.77 # Russian
m["https://example.org/doc1#char=14,24"] = 1 # Kommersant
m["https://example.org/doc1#char=38,44"] = 1 # Moscow
m["https://example.org/doc1#char=61,67"] = 0.97 # Greeks
m["https://example.org/doc1#char=73,76"] = 0.38 # gas
m["https://example.org/doc1#char=102,109"] = 0.97 # Tsipras
m["https://example.org/doc1#char=131,138"] = 0.58 # Russian
m["https://example.org/doc1#char=131,148"] = 1 # Russian President


m2 = {}  # membership function 
m2["https://example.org/doc1#char=21,34"] = 1 # Martin Bashir
m2["https://example.org/doc1#char=60,87"] = 1 # Living with Michael Jackson
m2["https://example.org/doc1#char=72,87"] = 0.8 # Michael Jackson
m2["https://example.org/doc1#char=93,104"] = 1 # King of Pop
m2["https://example.org/doc1#char=101,104"] = 0.8 # Pop
m2["https://example.org/doc1#char=119,122"] = 1 # Joe
m2["https://example.org/doc1#char=162,164"] = 0.8 # he
m2["https://example.org/doc1#char=162,186"] = 0.8 # he and his four siblings
m2["https://example.org/doc1#char=169,172"] = 0.8 # his
m2["https://example.org/doc1#char=0,7"] = 0.8 # Russian
m2["https://example.org/doc1#char=14,24"] = 1 # Kommersant
m2["https://example.org/doc1#char=38,44"] = 1 # Moscow
m2["https://example.org/doc1#char=61,67"] = 1 # Greeks
m2["https://example.org/doc1#char=73,76"] = 0.8 # gas
m2["https://example.org/doc1#char=102,109"] = 1 # Tsipras
m2["https://example.org/doc1#char=131,138"] = 0.8 # Russian
m2["https://example.org/doc1#char=131,148"] = 1 # Russian President


print("==============================\nNormal settings\n-------")
print("Micro F1:",bmk.microF())
print("Micro FEL:",bmk.microFEL(m))
print("Micro FEL_0.8:",bmk.microFEL(m2))

print("==============================\nExcluding Moscow\n-------")
print("Micro F1:",bmk_no_Moscow.microF())
print("Micro FEL:",bmk_no_Moscow.microFEL(m))
print("Micro FEL_0.8:",bmk_no_Moscow.microFEL(m2))

print("==============================\nExcluding Russian\n-------")
print("Micro F1:",bmk_no_Russian.microF())
print("Micro FEL:",bmk_no_Russian.microFEL(m))
print("Micro FEL_0.8:",bmk_no_Russian.microFEL(m2))
