import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import ujson

# Preprosessing data before indexing
with open('scraper_results.json', 'r') as doc:
    scraper_results = doc.read()



# Initialize empty lists to store publication name, URL, author, and date
pubName = []
pubURL = []
pubCUAuthor = []
pubDate = []

# Load the scraped results using ujson
data_dict = ujson.loads(scraper_results)



# Get the length of the data_dict (number of publications)
array_length = len(data_dict)
print(array_length)


# Separate name, url, date, author in different file
for item in data_dict:
    pubName.append(item["name"])
    pubURL.append(item["pub_url"])
    pubCUAuthor.append(item["cu_author"])
    pubDate.append(item["date"])

with open('pub_name.json', 'w') as f:
    ujson.dump(pubName, f)

with open('pub_url.json', 'w') as f:
    ujson.dump(pubURL, f)

with open('pub_cu_author.json', 'w') as f:
    ujson.dump(pubCUAuthor, f)

with open('pub_date.json', 'w') as f:
    ujson.dump(pubDate, f)

# Open a file with publication names and abstracts in read mode
with open('pub_name.json', 'r') as f:
    publication = f.read()

with open('pub_abstracts.json', 'r') as f:
    abstracts = f.read()

# Load JSON File
pubName = ujson.loads(publication)
pubAbstract = ujson.loads(abstracts)

print("NAMEEE",len(pubName))
print("Abstract",len(pubAbstract))
# Downloading libraries to use its methods
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Predefined stopwords in nltk are used
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
pub_list_first_lemma = []
pub_list = []
pub_list_wo_sc = []
'''

for file in pubName:
    # Splitting strings to tokens(words)
    words = word_tokenize(file)
    lemma_word = ""
    for i in words:
        if i.lower() not in stop_words:
            lemma_word += lemmatizer.lemmatize(i) + " "
    pub_list_first_lemma.append(lemma_word)
    pub_list.append(file)
'''
for file in pubAbstract:
    # Splitting strings to tokens(words)
    words = word_tokenize(file)
    lemma_word = ""
    for i in words:
        if i.lower() not in stop_words:
            lemma_word += lemmatizer.lemmatize(i) + " "
    pub_list_first_lemma.append(lemma_word)
    pub_list.append(file)

# Removing all below characters
special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
for file in pub_list:
    word_wo_sc = ""
    if len(file.split()) == 1:
        pub_list_wo_sc.append(file)
    else:
        for a in file:
            if a in special_characters:
                word_wo_sc += ' '
            else:
                word_wo_sc += a
        pub_list_wo_sc.append(word_wo_sc)

# Lemmatization Process
pub_list_lemma_wo_sw = []
for name in pub_list_wo_sc:
    words = word_tokenize(name)
    lemma_word = ""
    for a in words:
        if a.lower() not in stop_words:
            lemma_word += lemmatizer.lemmatize(a) + ' '
    pub_list_lemma_wo_sw.append(lemma_word.lower())

data_dict = {}  # Inverted Index holder

# Indexing process
for a in range(len(pub_list_lemma_wo_sw)):
    for b in pub_list_lemma_wo_sw[a].split():
        if b not in data_dict:
            data_dict[b] = [a]
        else:
            data_dict[b].append(a)

print(len(pub_list_wo_sc))
print(len(pub_list_lemma_wo_sw))
print(len(pub_list_first_lemma))
print(len(pub_list))

with open('publication_list_lemmatized_abstract.json', 'w') as f:
    ujson.dump(pub_list_first_lemma, f)

with open('publication_indexed_dictionary_lemmatized_abstract.json', 'w') as f:
    ujson.dump(data_dict, f)
