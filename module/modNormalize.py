import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

character = ['.',',',';',':','-,','...','?','!','(',')','[',']','{','}','<','>','"','/','\'','#','-','@']

class normalize():

    # mengubah semua kata menjadi huruf kecil
    def casefolding(self, text):
        norm_lower = text.lower()
        return norm_lower

    # memisah kalimat menjadi kata-kata ke dalam list yang dipisahkan dengan koma
    def tokenize(self, sentence, stopword=None, removepunct=False, splitby='space'):
        if splitby.strip().lower()=='space':
            words = re.split(r'\s',sentence)
        elif splitby.strip().lower()=='word':
            words = re.split('(\w+)?',sentence)
        else:
            raise NotImplementedError

        if removepunct:
            table = string.maketrans("","")
            words = [z.translate(table.string.punctuation).strip() for z in words]

        words = [x.strip().lower() for x in words if x.strip()]

        self.words = words
        return list(words)

    # filtering atau menghilangkan kata yang tidak memiliki makna (tidak penting)
    def stopwords(self, word):
        words = self.words
        f = open('stopword_list_tala.txt', 'r')
        z = f.readlines()
        z = list(map(lambda x: x.strip(), z))
        words = filter(lambda x: x not in z, words)
        return list(words)

    # stemming atau mengubah kata menjadi kata dasar (kata penting)
    def stemmingNorm(self, text, datatype='sentence'):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        if datatype == 'sentence':
            output = stemmer.stem(text)
            return output
        elif datatype == 'word':
            output = []
            for i in text:
                if i in character:
                    output.append(i)
                else:
                    stemmed = stemmer.stem(i)
                    output.append(stemmed)
            return output
