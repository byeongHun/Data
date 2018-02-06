'''
Created on Aug 26, 2015

@author: ybh
'''
import sys
import re
# from lxml import etree
from xml.dom import minidom
import xml.etree.ElementTree as ET
#fout = open("data","w")

def clean(line):
	'''remove white space in sentence'''
	line=line.strip()
	line=line.replace("\t","")

	return line

def makeEndTag(tag):
	tags=[]

	tag_names=tag.strip().split("><")
	# print tag_names
	if len(tag_names) < 2:
		return tag.replace("<","</")

	for i in range(len(tag_names)):
		if i==0: # first tag
			tags.append(tag_names[i][1:])
		elif i==len(tag_names)-1: # last tag
			tags.append(tag_names[i][:-1])
		else:
			tags.append(tag_names[i])

	endtag=""
	for tag in reversed(tags): # loop backwards
		endtag += "</"+tag+">"

	return endtag

def removeOtherTags(content):
	content=re.sub("\<\w+\>|\<\/\w+\>"," ",content)
	content=re.sub("\&\#\w[\d|\w]+\;"," ",content)
	content=re.sub("\<\w+ \w+\=\"\w+\"\>"," ",content)
	content=re.sub("\n+", "\n", content)
	content=re.sub("\s\s+"," ",content)

	return content


def extractCorpus(line):
	title=extractTitle(line)
	abstract=extractAbstract(line)

def extractTitle(line):
	'''
	<title-group><article-title>	</article-title></title-group>
	'''
	tags=["<title-group><article-title>"]

	title=""
	for tag in tags:
		if not tag in line:
			continue

		splitData=line.split(tag)
		endtag=makeEndTag(tag)
		# print endtag
		splitTitle=splitData[1].split(endtag)
		# print splitTitle[0]
		title=splitTitle[0]
	
	title = removeOtherTags(title)
	print title
	#print >> fout,title

def extractAbstract(line):
	'''
	<abstract>	</abstract>
	'''
	tags=["<abstract>"]

	abstract=""
	for tag in tags:
		if not tag in line:
			continue

		splitData=line.split(tag)
		endtag=makeEndTag(tag)
		print endtag
		splitAbstract=splitData[1].split(endtag)
		# print splitAbstract[0]
		abstract=splitAbstract[0]
	
	abstract = removeOtherTags(abstract)
	print abstract


'''input xmlFn'''
xmlFn=sys.argv[1]
article=open(xmlFn).readlines()
for line in article:
	line=clean(line)
	extractCorpus(line)

