from flask import Flask, flash,render_template, request, send_from_directory,session
import os
import pandas as pd
import numpy as np

pwd = os.path.dirname(os.path.realpath(__file__))
wordsFile = "/words.csv"
data = pd.read_csv(pwd + wordsFile)

words = data['WORD'][:69]
domain = data['Domain'][:69]
expl = data['Explanation'][:69]
hint = data['Hint'][:69]
totalWords = len(words)

app = Flask(__name__)
app.secret_key = 'the random string'

def check(word,index):
    word = list(word)
    actual = list(words[index])
    out = 5*['0']
    for i in range(len(word)):
        if word[i] == actual[i]:
            out[i] = '2'
            word[i] = '_'
            actual[i] = '_'
    for i in range(len(word)):
        if (word[i] in actual) and (word[i] != '_'):
            out[i] = '1'
            ind = actual.index(word[i])
            actual[ind] = '_'
    return ''.join(out)


    

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        wordIndex = np.random.randint(low = 0, high=totalWords)
        print(words[wordIndex])
        session['wordIndex'] = wordIndex
        session['domain'] = domain[wordIndex]
        session['guessNum'] = 1

        session['guesses'] = ''
        session['colors'] = ''
        session['hintAsk'] = False
        session['done'] = False
 
        return render_template('index.html')
        
    if request.method == 'POST':
        if session['done']:
            wordIndex = np.random.randint(low = 0, high=totalWords)
            print(words[wordIndex])
            session['wordIndex'] = wordIndex
            session['domain'] = domain[wordIndex]
            session['guessNum'] = 1

            session['guesses'] = ''
            session['colors'] = ''
            session['hintAsk'] = False
            session['done'] = False
    
            return render_template('index.html')

        if request.form.get('check') == 'True':
            if len(request.form.get('guess').lower()) == 5 :
                if request.form.get('guess').upper() not in session['guesses']:
                    if request.form.get('guess').lower() in list(words):
                        session['guesses'] = session['guesses'] + "%s,"%(request.form.get('guess').upper())
                        gg = check(request.form.get('guess').lower(),session['wordIndex'])
                        session['colors'] = session['colors'] + "%s,"%(gg)
                        if gg == '22222':
                            flash('Your score : %d/7 '%(8-session['guessNum']-int(session['hintAsk'])))
                            flash('%s : %s'%(words[session['wordIndex']].upper(),expl[session['wordIndex']]))
                            session['done'] = True
                        elif session['guessNum'] == 6:
                            flash('Better luck next time!')
                            flash('%s : %s'%(words[session['wordIndex']],expl[session['wordIndex']]))
                            session['done'] = True
                        session['guessNum'] += 1
                    else:
                        flash('Word not found in our list!')
                else:
                    flash('Please enter a different 5-letter word!')
            else:
                flash('Please enter a 5-letter word!')

        if request.form.get('hint') == 'True':
            session['hintAsk'] = True
            session['hint'] = hint[session['wordIndex']]
            
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)

    
    
  
    
    
    
