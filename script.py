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


file_system_no_heAnd = open("Questionnaire_System_without_he-and-his-four-siblings.ttl", "r")
system_t_no_heAnd = "".join(file_system_no_heAnd.readlines())
file_system_no_heAnd.close()



## --------------------- Parsing

parser = NIFParser()
wrp_gold = parser.parser_turtle(gold_t)


#-----
parser = NIFParser()
wrp_sys = parser.parser_turtle(system_t)

parser = NIFParser()
wrp_sys_no_Moscow = parser.parser_turtle(system_t_no_Moscow)

parser = NIFParser()
wrp_sys_no_heAnd = parser.parser_turtle(system_t_no_heAnd)


## --------------------- Measurement
bmk = NIFBenchmark(wrp_sys, wrp_gold)
bmk_no_heAnd = NIFBenchmark(wrp_sys_no_heAnd, wrp_gold)
bmk_no_Moscow = NIFBenchmark(wrp_sys_no_Moscow, wrp_gold)

m = {}  # membership function 
m["https://example.org/doc1#char=21,34"] = 1 # Martin Bashir
m["https://example.org/doc1#char=60,87"] = 0.97 # Living with Michael Jackson
m["https://example.org/doc1#char=72,87"] = 0.75 # Michael Jackson
m["https://example.org/doc1#char=93,104"] = 0.94 # King of Pop
m["https://example.org/doc1#char=101,104"] = 0.33 # Pop
m["https://example.org/doc1#char=119,122"] = 1 # Joe
m["https://example.org/doc1#char=162,164"] = 0.56 # he
m["https://example.org/doc1#char=162,186"] = 0.50 # he and his four siblings
m["https://example.org/doc1#char=169,172"] = 0.39 # his
m["https://example.org/doc1#char=0,7"] = 0.61 # Russian
m["https://example.org/doc1#char=14,24"] = 0.97 # Kommersant
m["https://example.org/doc1#char=38,44"] = 0.94 # Moscow
m["https://example.org/doc1#char=61,67"] = 0.94 # Greeks
m["https://example.org/doc1#char=73,76"] = 0.36 # gas
m["https://example.org/doc1#char=102,109"] = 0.92 # Tsipras
m["https://example.org/doc1#char=131,138"] = 0.53 # Russian
m["https://example.org/doc1#char=131,148"] = 0.97 # Russian President


m2 = {}  # membership function 
m2["https://example.org/doc1#char=21,34"] = 1 # Martin Bashir
m2["https://example.org/doc1#char=60,87"] = 1 # Living with Michael Jackson
m2["https://example.org/doc1#char=72,87"] = 1 # Michael Jackson
m2["https://example.org/doc1#char=93,104"] = 1 # King of Pop
m2["https://example.org/doc1#char=101,104"] = 1 # Pop
m2["https://example.org/doc1#char=119,122"] = 1 # Joe
m2["https://example.org/doc1#char=162,164"] = 0.3 # he
m2["https://example.org/doc1#char=162,186"] = 0.3 # he and his four siblings
m2["https://example.org/doc1#char=169,172"] = 0.3 # his
m2["https://example.org/doc1#char=0,7"] = 1 # Russian
m2["https://example.org/doc1#char=14,24"] = 1 # Kommersant
m2["https://example.org/doc1#char=38,44"] = 1 # Moscow
m2["https://example.org/doc1#char=61,67"] = 1 # Greeks
m2["https://example.org/doc1#char=73,76"] = 0.3 # gas
m2["https://example.org/doc1#char=102,109"] = 1 # Tsipras
m2["https://example.org/doc1#char=131,138"] = 1 # Russian
m2["https://example.org/doc1#char=131,148"] = 1 # Russian President


print("==============================\nNormal settings\n-------")
print("Micro F1:",bmk.microF())
print("Micro FEL:",bmk.microFEL(m))
print("Micro FEL_0.8:",bmk.microFEL(m2))

print("==============================\nExcluding Moscow\n-------")
print("Micro F1:",bmk_no_Moscow.microF())
print("Micro FEL:",bmk_no_Moscow.microFEL(m))
print("Micro FEL_0.8:",bmk_no_Moscow.microFEL(m2))

print("==============================\nExcluding 'he and his four siblings'\n-------")
print("Micro F1:",bmk_no_heAnd.microF())
print("Micro FEL:",bmk_no_heAnd.microFEL(m))
print("Micro FEL_0.8:",bmk_no_heAnd.microFEL(m2))
