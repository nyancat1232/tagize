from nltk.stem import WordNetLemmatizer

def lemmatize_filtered_stopwords(filtered):
    lemmatized=[] #지금 lemmatize 부분이 반복적으로 쓰인거 같음. => 모듈화하기
    for word,pos in filtered:
        for_lemma_tag=pos[0].lower()
        try:
            lemmatized.append(WordNetLemmatizer().lemmatize(word=word,pos=for_lemma_tag))
        except:
            if for_lemma_tag=='j':
                lemmatized.append(WordNetLemmatizer().lemmatize(word=word,pos='a'))
            pass
    return lemmatized