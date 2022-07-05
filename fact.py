    # import required module
import os
import xml.etree.cElementTree as ET;
import re
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
import nltk as nltk
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# assign directory
def remove_stop_words(sen):
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(sen)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    sen=filtered_sentence
    return sen
def remove_stop_words_list(sen):
    stop_words = set(stopwords.words('english'))
    
    filtered_sentence = []
    for w in sen:
        if w not in stop_words:
            filtered_sentence.append(w)
    sen=filtered_sentence
    return sen


directory = 'CA Cases_with HN alongwith Bold_Italic'
f=open("facts_cue_phrases.txt",'r')
facts=f.readlines()
for i in range(len(facts)):
    facts[i]=facts[i].strip()
    facts[i]=facts[i].lower()
    # facts[i]=remove_stop_words(facts[i])
f=open("arguments_cue_phrases.txt",'r')
arguments=f.readlines()
for i in range(len(arguments)):
    arguments[i]=arguments[i].strip()
    arguments[i]=arguments[i].lower()
    # arguments[i]=remove_stop_words(arguments[i])

# iterate over files in
# that directory

for filename in os.listdir(directory):  
    f = os.path.join(directory, filename)
    # f="Civil Appeal/12 01 2021 SC 5231-32 of 2016.xml"
    print(f)
    # break

    f1=open(f,'r')
    # print(f1)
    tree=ET.ElementTree(file=f)
    root=tree.getroot()
    # print(f)
    allpara=[]
    for chld in root:
        # print(chld)
        if(chld.tag=='JudgmentText'):
            # print(chld)
            for para in chld:
                if(para.tag!='I'):
                    txt=para.text
                    if(txt!=None and len(txt)>0):
                        txt=txt.strip()
                        txt=txt.lower()
                        allpara.append(txt)
                # else:
                #     allpara.append("STOP")
    # print(allpara)
    fact_on=0
    data=[]
    for i in allpara:
        ok=False
        # i=remove_stop_words(i)
        if(fact_on==1 or fact_on==0):
            if(i=='STOP'):
                fact_on=0
            for j in arguments:
                if(len(i)<2*len(j)):
                    continue
                if(fuzz.partial_ratio(j,i)>80):
                    # print("argument")
                    # print(len(i))
                    # print(i)
                    # print(len(j))
                    # print("-----------------Fact end-------------------------")
                    fact_on=-1
                    break
        if(fact_on==0):
            for j in facts:
                if(fuzz.partial_ratio(j,i)>90):
                    # print(i)
                    # print("----------Fact start-----------")
                    # print(j)
                    # print(i)
                    fact_on=1
                    # ok=True
                    
        if( not ok):
            # print(i)
            text = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(text)
            tense = {}
            tense["future"] = len([word for word in tagged if word[1] == "MD"])
            tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
            tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
            # print(tense)
            if(fact_on==1):
                if(tense["present"]>tense["future"] and tense["present"]>tense["past"]):
                    fact_on=0
            elif(fact_on==0):
                if(tense["past"]>=tense["future"] and tense["present"]<=tense["past"]):
                    fact_on=1
                
        
        if(fact_on==1):
            data.append(i)
    f=os.path.join("result", os.path.splitext(filename)[0]+".txt")
    # f="result/12 01 2021 SC 5231-32 of 2016.txt"
    f1=open(f,"w")
    l=""
    for i in data:
        i=i+'\n'
        l=l+i
    # print(l)
    # print(f1)
    f1.write(l)
    # print(l)
    # print(f1)
    # break