import dbm, re, sys, os, pdfplumber
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

#DBMS
db = dbm.open('TLA', 'c')
db['TLA'] = 'Three Letter Acronym'
inp = sys.argv[1]

#Download pdf
def downloadPDF(download_url, filename):
    response = urllib.request.urlopen(download_url)   
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

#Get text pdf
def getTextPDF(path):
    pdffileobj=pdfplumber.open(path)
    text = ''
    for page in pdffileobj.pages:
        text = text + page.extract_text()

    pdffileobj.close()
    return text
    
#For HTML
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

if inp[-4:].lower() == '.pdf':
    if inp[:8] == 'https://':
        downloadPDF(inp,"try")
        pdfPath = "try.pdf"
        text = getTextPDF(pdfPath)
        os.remove(pdfPath)
    else:
        pdfPath = inp
        text = getTextPDF(pdfPath)

else:
    if inp[:8] == 'https://':
        html = urllib.request.urlopen('https://github.com/deimos2683/deimos2683.github.io/tree/master/news').read()
        text = text_from_html(html)
    else:
        print("Invalid Input")
        sys.exit()

# Remove punctuations
text = re.sub(r'[^\w\s]', " ", text)

# Actual Algo
acronyms_list=[]
acronyms = []; fullforms =[]
text = text.split()

for i in range(len(text)):
  words = text[i]

  if words[-1]=="s":
    words=words[:-1]
    if(words.isupper()==True and len(words)>1==True and words.isalpha()==True):
      pass
    else:
      words = words+'s'

  if(words.isupper()==True and len(words)>1==True and words.isalpha()==True):
    acronyms_list.append(words)
    start = max(i-10,0); stop = min(len(text),i+11)

    #Find first letter matches
    firstLetters = (''.join([str(elem[0]).lower() for elem in text[start:i]]))

    firstLetters = firstLetters[::-1]
    try:
        tlaIndex = firstLetters.index((words.lower()[::-1]))
        acronyms.append(words)
        fullforms.append( (' '.join([ str(elem) for elem in text[-tlaIndex+i-len(words):-tlaIndex+i] ]) ) )
    except ValueError:
        firstLetters = (''.join([str(elem[0]).lower() for elem in text[i+1:stop]]))
        
        try:
            tlaIndex = firstLetters.index(words.lower())
            acronyms.append(words)
            fullforms.append( (' '.join([ str(elem) for elem in text[i+1+tlaIndex:i+1+tlaIndex+len(words)] ]) ) )
        except ValueError:
            pass

not_found = []
for word in list(set(acronyms_list)):
    if word in acronyms:
        print(word," : ", fullforms[acronyms.index(word)])
    else:
        full = db.get(word)
        if (full != None):
            print(word," : ", str(full.decode("utf-8")))
        else:
            not_found.append(word)
print("\nNot found : ",not_found)

for i in range(len(acronyms)):
    db[acronyms[i]] = fullforms[i] 

db.close()