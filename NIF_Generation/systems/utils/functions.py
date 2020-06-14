#!/usr/bin/python3
# -*- coding: utf-8 -*-


# This function return the id in a url, example in follow
# > url2id('http://es.dbpedia.org/resource/Barack_Obama')
# > 'Barack_Obama'
def url2id(url):
    try:
        i = -1
        while url[-i]!='/':
            i = i+1
        return url[-i+1:len(url)]
    except Exception as err:
        print("Error in url2id ("+url+")")
        print(err)
        return url




# This function return the id normalized in a url in the format of SemEval2015 Task15, example in follow
# > url2id('http://es.dbpedia.org/resource/Barack_Obama')
# > 'wiki:barack obama'
def url2id_wiki_normalized(url):
    try:
        i = -1
        while url[-i]!='/':
            i = i+1
        txt = url[-i+1:len(url)]
        return "wiki:"+txt.replace("_"," ").lower()
    except Exception as err:
        print("Error in url2id ("+url+")")
        print(err)
        return url


#return de position of the token of the word in 'text' that starts in the position 'pos'
def position2numbertoken(txt,pos):
    return txt.strip(" ")[:pos].count(" ")


#return de position of the token of the word in 'text' that starts in the position 'pos'.
#In this case, there are many sentences
def position2numbertoken_doc(txt,pos):
    cantOfEndPoint = txt.strip(" ")[:pos].count(".")

    posOfLastPoint = pos
    while posOfLastPoint>0 and txt[posOfLastPoint]!=".":
        posOfLastPoint -= 1
    if posOfLastPoint+1 < len(txt):
        posOfLastPoint += 1
    PosTokenInSentence = txt[posOfLastPoint:pos].lstrip(" ").count(" ")
    return [cantOfEndPoint,PosTokenInSentence]


# Return True if existe the file in the path of "filename"
def ExistFile(filename):
    exist = True
    try:
        f = open(filename,"r")
    except:
        exist = False
    return exist


# input: YAGO:Barack_Obama
# output: wiki:barack obama
def yago2wikiid(txt):
    return "wiki:"+txt.strip(" \n").replace("_"," ").lower()[5:]
