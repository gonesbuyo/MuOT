import csv
import re
import spacy
from collections import Counter
import json
import random

nlp = spacy.load('en')

""" PREPROCESSING """
def preprocess(path):
    
    with open(path) as f:

        rows = []

        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            rows.append(row)

        songs = []
        authors = []
        lyrics = [] 
        ids = []

        for d in rows:
            songs.append(d['song'])
            authors.append(d['author'])
            ids.append(d['youtube_id'])

            lyric = d['lyric'].split('\n')
            pattern = re.compile(r"(\[|{|\().*(\]|}|\))")

            for line in lyric:
                if pattern.match(line):
                    lyric.remove(line)

            lyrics.append(lyric)
        
        
    return (songs, authors, lyrics, ids)
    
""" LEMMATIZING """
def lemmatize(line):
    
    doc = nlp(line)
    lemmas = []
    
    for word in doc:
        lemmas.append(word.lemma_)
    output = ' '.join(lemmas)
    
    return output

""" POS TAGGING """
def posTag(line):
    
    terms = []
    doc = nlp(line)
    
    for word in doc:
        if (word.pos_ == 'NOUN' or word.pos_ == 'ADJ') and str(word) != '-PRON-':
            terms.append(str(word))
            
    return terms
    
""" TERM FREQUENCIES """
def termFreq(terms, n):
    
    maxValues = []
    counts = Counter(terms)
    d = dict(counts)
    # print(d)
    
    for i in range(n):
        # if i < len(d):
        if len(d)> 0:
            maxVal = max(d, key=d.get)
            maxValues.append(maxVal)
            d.pop(maxVal)
        
    return maxValues

""" OBTAIN MOST FREQUENT TERMS """
def lyric2Frecs(path, n):
    
    output = {}
    songs, authors, lyrics, ids = preprocess(path)
    
    i = 0
    for lyric in lyrics:
        song = songs[i]
        author = authors[i]
        iD = ids[i]
    
        for line in lyric:
            line = lemmatize(line)
            terms = posTag(line)
            
        if len(terms) > 0:
            keywords = termFreq(terms, n)
            output[song] = (author, keywords, iD)
            
        i += 1
        
    return output

n = 6
# path = '/home/cxb0141/Escritorio/datalyrics.csv'
path = '/home/cxb0141/Escritorio/lyricsIDs.csv'

output = lyric2Frecs(path, n)

with open('/home/cxb0141/Escritorio/freqWords.json', 'w') as out_path:
    json.dump(output, out_path, indent=4)

""" SELECT THE SONG ID THAT BEST FITS A GIVEN LIST OF RESULTS FOR AN IMAGE """
def fitSong(results, songWords):
    
    fits = []
    lengths = []
    
    for song in songWords:
        
        # print(songWords[song][1])
        intersec = list(set(songWords[song][1]).intersection(results))
        length = len(intersec)
        
        if length > 0:
            fits.append([length, song, intersec])
            lengths.append(length)

    maximum = max(lengths)
            
    """for fit in fits:
        if fit[0] = maximum:"""
    selected = list(filter(lambda e: e[0] == maximum, fits))
    song = random.choice(selected)
    # print(song)
    
    # print(songWords)
    # print(songWords[song])
    songID = songWords[song[1]][2]
    
    return songID


def finalOutput(results):
	songID = fitSong(results, output)
	print(songID)

	return(songID)