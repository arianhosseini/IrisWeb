

# coding: utf8
from __future__ import unicode_literals
__author__ = 'Arian'
from hazm import *
from flask import Flask
from flask import request
from flask import render_template
import os


app = Flask(__name__)
tagger = POSTagger(model='resources/postagger.model')

@app.route("/")
def index():
#    print "hello"
    return render_template('index.html', name="index")



@app.route("/ner",methods=['POST'])
def ner():
    if request.method == 'POST':        
        print(request.form['text'].encode('utf-8'))
        result = tagger.tag(word_tokenize(request.form['text']))
        outLine = ""
        for counter in range(len(result)-1):
            token = result[counter]
            outLine += token[0] + "\t" + token[1] + "\n"

        outLine += result[-1][0] + "\t" + result[-1][1]
        tempFile = open(os.getcwd()+'/projectTemp/evalText.txt','wb')
        tempFile.write(outLine.encode('utf-8'))
        tempFile.close()
        os.system("java -jar CoreNLP.jar")
        outputFile = open('result.txt','rb')
        result = outputFile.read().decode('utf-8')
        outputFile.close()
        tokens = result.split('\t')
        outText = ""
        for token in tokens:
            word = ""
            splitedText = token.split('/')
            if len(splitedText) > 1:
            #print splitedText[0]," ",splitedText[1]
                if splitedText[1] != "O" and splitedText[1] != "O\t":
                    tag = splitedText[1].split('_')
                    print(tag)
                    word = '<span class="'+ tag[1].lower() +'">' + splitedText[0] + '</span>'
                else:
                    word = splitedText[0]
            outText+= word +' '

#        print(outText)
        return outText.encode('utf-8')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6969,debug=True)
