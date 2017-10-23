#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import io, time, json
import requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
# from bs4 import BeautifulSoup

auth=('ANDREWID', 'PASSWORD')


'''
Download testcase
query: query file url
param: param file url

Demo:
    for i in range(63):
        query = 'http://boston.lti.cs.cmu.edu/classes/11-642/HW/HTS/tests/HW2-Train-%d.qry' % i
        param = 'http://boston.lti.cs.cmu.edu/classes/11-642/HW/HTS/tests/HW2-Train-%d.param' % i
        retrieve(query, param)
'''
def retrieve(query, param):
    i = 0
    query_response = requests.get(query, auth=auth)
    param_response = requests.get(param, auth=auth)
    
    p = param_response.content.strip()
    right = p[p.index('retrievalAlgorithm'):]
    algo = right[:right.index("\n")]
    print i, '-' * 10
    print algo
    print 
    print query_response.content.strip()
    
  
'''
Print in a user-friendly way
'''
def prettyPrintHTML(html):
    soup = BeautifulSoup(html, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text(separator="\n")

    # break into lines and remove leading and trailing space on each
    lines = (line for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

    

def getLeftSideSoup(filePath, logtype):
    testing_url = 'http://boston.lti.cs.cmu.edu/classes/11-642/HW/HTS/tes.cgi'
    payload = {'logtype': logtype, 'hwid': 'HW3', 'id':'yichenp'}
    files = {'infile': open(filePath, 'rb')}
    r = requests.post(testing_url, files=files, auth=auth, data=payload)
    html = r.content
    return BeautifulSoup(html, "html.parser")

'''
Retrieve the detailed score from trec_eval service
    If the total query number is N, there will be
    N line "map 195 0.0148"
    1 line "map all 0.2063"
    discard the map all line
'''
def getTrecDetailedScore(filePath):
    soup = getLeftSideSoup(filePath, 'Detailed')
    text_tmp = soup.get_text(separator="\n")
    text = [line.strip() for line in text_tmp.split('\n') if 'map ' in line and 'all' not in line]
    mapScore = [line[-6:] for line in text]
#     print "text"
#     print text
#     print " | ".join(mapScore)
#     print len(mapScore)
    return mapScore
    
'''
Used for deciding win loss rate
    Get TrecDetailedScore of baseline:
        baseLine = getTrecDetailedScore("hw3/output/E1-RankedBoolean.teln")
    Compare win loss between baseline and my-otuput.teln:
        getWinLoss(baseLine, 'My-output.teln')

Sample output:
    win, loss, equal 10 10  0
'''
def getWinLoss(baseLine, filePath):
    myScore = getTrecDetailedScore(filePath)
    for base, my in zip(baseLine, myScore):
        print base, my
    win = sum([1 for base, my in zip(baseLine, myScore) if base < my])
    loss = sum([1 for base, my in zip(baseLine, myScore) if base > my])
    equal = sum([1 for base, my in zip(baseLine, myScore) if base == my])
#     print " ".join(baseLine)
#     print " ".join(myScore)
    print "win, loss, equal %2d %2d %2d" % (win, loss, equal)

    
'''
Helper function for autoCheckCorrectness
'''
def getCheckListPlayload(nums):
    checklist = []
    for i in nums:
        checklist.append('HW3-Train-%d' % i)
    return checklist


'''
Used for testing software

Demo:
    checklist2 = ['HW2-train-Nested-0', 'HW2-train-Nested-1', 'HW2-train-Nested-2', 'HW2-train-Weight-0', 'HW2-train-Weight-1']
    autoCheckCorrectness(checklist2)
'''
def testSoftware(checklist, filePath, hwId):
    checking_url = 'http://boston.lti.cs.cmu.edu/classes/11-642/HW/HTS/hts.cgi'
    payload = {'submissionType': 'interim', 'hwid': hwId, 'test': checklist}
    files = {'infile': open(filePath, 'rb')}
    r = requests.post(checking_url, files=files, auth=auth, data=payload)
    html = r.content
    prettyPrintHTML(html)


'''
Used for trec_eval Service
    print the value of MAP, P10, P10, P30

Demo:
    getTrecSummaryScore('../xxxx.teln')
'''
def getTrecSummaryScore(filePath):
    res = []
    soup = getLeftSideSoup(filePath, 'Summary')

    text_tmp = soup.get_text(separator="\n")
    text = [line.strip() for line in text_tmp.split('\n') if 'map ' in line or 'P10 ' in line or 'P20 ' in line or 'P30 ' in line]
#     print '\n'.join(text)
    assert len(text) == 4
    temp = text.pop(0)
    text.append(temp)

    for line in text:
        print line[-6:]
        res.append(line[-6])
    print ""

    return res