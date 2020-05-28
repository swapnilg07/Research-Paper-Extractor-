import json
import re
import nltk
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from nltk.corpus import wordnet
nltk.download('wordnet')

person_list = []
def get_human_names(text):
    try:
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1:
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
    except Exception as e:
        print(e)

def convert_pdf_to_txt(path):
    try:
        l=[]
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 10
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        l.append(text)
        return l
    except:
        return []

def classifier(l):
    parts=["head","abstract","introduction","conclusion","references"]
    cur=1
    theory=[""]*len(parts)
    try:
        for i in range(0,len(l)):
            k=l[i]
            k=k.lower()
            if cur<=4 and parts[cur] in k:
                cur+=1
            else:
                theory[cur-1]+="\n"+l[i]
    except Exception as e:
        print(e)
    return theory

def disc_reference(l):
    s=""
    try:
        for i in l:
            if i=='[':
                s=s+"\n\n["
            elif i!='\n':
                s=s+i
    except Exception as e:
        print(e)
    return s

def pdftojson(s):
    l=convert_pdf_to_txt(s)
    if(len(l)>0):
        l=l[0].split("\n")
    d=classifier(l)

    #Geting Names from the head
    person_names=person_list
    names = get_human_names(d[0])
    for person in person_list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if(name in person):
                    person_names.remove(person)
                    break

    mails=re.findall('\S+@\S+', d[0])
    my_details={"Name":'\n'.join([str(elem) for elem in person_names]) ,"mail":'\n'.join([str(elem) for elem in mails]),"Abstract":d[1],"Introduction":d[2],"Conclusion":d[3],"References":disc_reference(d[4])}

    with open('personal.json', 'a') as json_file:
        json.dump(my_details, json_file)
    return my_details

if __name__=="__main__":
    details=pdftojson(r'C:\Users\swapn\pythonproject\pdftojson\pdftojson\1806.04558v4.pdf')
