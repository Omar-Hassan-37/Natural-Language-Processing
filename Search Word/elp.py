import nltk
import os

class EventHandler:
    def __init__(self, list_widget, entry_widget):
        self.list_widget = list_widget
        self.entry_widget = entry_widget
        self.index=0
        self.pred = []
    def get_list(self, event):
        
        #only listen to space key
        if event.keysym != 'space':
            return
        
        #clear list
        if self.list_widget.size() > 0:
            self.list_widget.delete(0,self.list_widget.size())
        
        entered_text = self.entry_widget.get()
        splitted_text = entered_text.strip().split(' ')
        

        if len(splitted_text) == 1:
            #get list of predictions
            if splitted_text[0] in freqDist:
                self.pred = freqDist[splitted_text[0]]
            else:
                self.pred=[]

            for i in range(5):
                if i >= len(self.pred):
                    break
                self.list_widget.insert(i, self.pred[i][0][0] + ' ' + self.pred[i][0][1])
                
        elif len(splitted_text) == 2:
            pred_second = [w[0][1] for w in self.pred if w[0][0] == splitted_text[1]]
            
            for i in range(5):
                if i >= len(pred_second):
                    break
                self.list_widget.insert(i, splitted_text[0] + ' ' +splitted_text[1]+ ' ' + pred_second[i])
        


directory = 'Sports'
os.listdir(directory)

tokens = []
for w in os.listdir(directory):
    tokens.extend(nltk.word_tokenize(
        open(directory + '/'+ w, encoding='utf-8').read()
             ))
    
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
tokens_rem_stop = [w for w in tokens if w not in arb_stopwords]

def trigrams(words):
    tris=[]
    for i in range(0,len(words)-2):
        tris.append((words[i], words[i+1], words[i+2]))
    return tris

trigrams = trigrams(tokens_rem_stop)
tri_to_bi = [(w0, (w1, w2)) for w0, w1, w2 in trigrams]

freqDist = {}

for i in tri_to_bi:

    
    if i[0] not in freqDist:
        freqDist[i[0]] = {i[1]:1}
    else:
        if i[1] not in freqDist[i[0]]:
            freqDist[i[0]][i[1]]=1
        else:
            freqDist[i[0]][i[1]] += 1
            

for k in freqDist:
    l = []
    for j in freqDist[k]:
        l.append((j, freqDist[k][j]))
    l.sort(key=lambda x: x[1], reverse=True)
    freqDist[k] = l

import tkinter as tk
window = tk.Tk()
w = tk.Listbox()
greeting = tk.Entry()
e = EventHandler(w, greeting)

greeting.bind('<KeyPress>', e.get_list)
greeting.pack()



w.pack()

window.mainloop()