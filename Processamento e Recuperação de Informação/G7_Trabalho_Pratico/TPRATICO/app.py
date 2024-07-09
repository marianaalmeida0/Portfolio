import streamlit as st
from PIL import Image
import ujson
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import os
import nltk
import numpy as np
import re
import streamlit as st
import numpy as np
# Autenticação com o Google Drive

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)


# Set up the NLTK components
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()


# STEMMER
with open('publication_list_stemmed.json', 'r') as f:
    pub_list_first_stem = ujson.load(f)
with open('publication_indexed_dictionary.json', 'r') as f:
    pub_index = ujson.load(f)
with open('author_list_stemmed.json', 'r') as f:
    author_list_first_stem = ujson.load(f)
with open('author_indexed_dictionary.json', 'r') as f:
    author_index = ujson.load(f)
with open('publication_list_stemmed_abstract.json', 'r') as f:
    pub_list_first_stem_abs = ujson.load(f)
with open('publication_indexed_dictionary_abstract.json', 'r') as f:
    pub_index_abs = ujson.load(f)
# DOCS ESPECIALIZADOS

with open('docs_list_stemmed.json', 'r') as f:
    pub_list_first_stem_docs = ujson.load(f)
with open('docs_indexed_dictionary.json', 'r') as f:
    pub_index_docs = ujson.load(f)

#LEMMA
with open('publication_list_lemmatized.json', 'r') as f:
    pub_list_first_lemma = ujson.load(f)
with open('publication_indexed_dictionary_lemmatized.json', 'r') as f:
    pub_index_lemma = ujson.load(f)
with open('author_list_lemmatized.json', 'r') as f:
    author_list_first_lemma = ujson.load(f)
with open('author_indexed_dictionary_lemmatized.json', 'r') as f:
    author_index_lemma= ujson.load(f)

with open('publication_list_lemmatized_abstract.json', 'r') as f:
    pub_list_first_lemma_abs = ujson.load(f)
    
with open('publication_indexed_dictionary_lemmatized_abstract.json', 'r') as f:
    pub_index_lemma_abs = ujson.load(f)

# DOCS ESPECIALIZADOS
with open('doc_list_lemmatized.json', 'r') as f:
    pub_list_first_lemma_docs = ujson.load(f)
with open('doc_indexed_dictionary_lemmatized.json', 'r') as f:
    pub_index_lemma_docs = ujson.load(f)



with open('doc_name.json', 'r') as f:
    doc_name = ujson.load(f)
with open('doc_html.json', 'r') as f:
    doc_html = ujson.load(f)


with open('author_names.json', 'r') as f:
    author_name = ujson.load(f)
with open('pub_name.json', 'r') as f:
    pub_name = ujson.load(f)
with open('pub_url.json', 'r') as f:
    pub_url = ujson.load(f)
with open('pub_cu_author.json', 'r') as f:
    pub_cu_author = ujson.load(f)
with open('pub_date.json', 'r') as f:
    pub_date = ujson.load(f)
with open('pub_abstracts.json','r') as f:
    pub_abst=ujson.load(f)


# Function to process text based on strategy (stemming or lemmatization)
def process_text(text, strategy):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words]

    if strategy == 'Stemming':
        processed_tokens = [stemmer.stem(token) for token in tokens]
    elif strategy == 'Lemmatization':
        processed_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    else:
        processed_tokens = tokens

    return processed_tokens


# Custom implementation of cosine similarity



def term_frequency(word, document):
    return document.count(word) / len(document)
tf = term_frequency

def inverse_document_frequency(word, corpus):
    count_of_documents = len(corpus) + 1
    count_of_documents_with_word = sum([1 for doc in corpus if word in doc]) + 1
    idf = np.log10(count_of_documents/count_of_documents_with_word) + 1
    return idf
idf = inverse_document_frequency

def TF_IDF(word, document, corpus):
    return tf(word, document) * idf(word, corpus)


def tf_idf_vectorizer(linha):


    if type(linha[0]) == str: # lista de 1 elemento
        linha = [linha]
    word_set = list(set(sum(linha, [])))
    word_to_index = {word:i for i, word in enumerate(word_set)}
    num_words = len(word_set)

    word_vectors = []
    for documento in linha:
        new_word_vector = [0 for i in range(num_words)]
        for palavra in documento:
            # get the score
            tf_idf_score = TF_IDF(palavra, documento, linha)
            # next get the index for this word in our word vector
            word_index = word_to_index[palavra] 
            # populate the vector
            new_word_vector[word_index] = tf_idf_score
        word_vectors.append(new_word_vector)
    return word_vectors

def cosseno_sim(mat_A, mat_B):
    matriz_sim = []
    magnitude_B = [sum(b[i]*b[i] for b in mat_B)**0.5 for i in range(len(mat_B[0]))]
    for linha in mat_A:
        dot_products = [sum(a*b for a, b in zip(linha, col)) for col in zip(*mat_B)] 
        magnitude_A = sum(a*a for a in linha)**0.5
        cosine_similarities = [dot_product / (magnitude_A * magnitude_B[i]) for i, dot_product in enumerate(dot_products)]
        matriz_sim.append(cosine_similarities)
    return matriz_sim


# Function to perform search based on input text, operator value, search type, and strategy
def search_data(input_text, operator_val, search_type, strategy,ranking_choice):
    output_data = {}
    processed_text = process_text(input_text, strategy)
    if operator_val == 2:  #Relevant operator (OR)
        input_text = input_text.lower().split()
        pointer = []
        for token in input_text:
            if len(input_text) < 2:
                st.warning("Please enter at least 2 words to apply the operator.")
                break
            stem_temp = ""
            word_file = []
            temp_file = []
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    if strategy == 'Stemming':
                        stem_temp += stemmer.stem(x) + " "
                    elif strategy == 'Lemmatization':
                        stem_temp += lemmatizer.lemmatize(x) + " "
            word_file.append(stem_temp)
            
            if strategy == 'Stemming':
                if search_type == "publication" and pub_index.get(word_file[0].strip()):
                    pointer = pub_index.get(word_file[0].strip())
                elif search_type == "abstracts" and pub_index_abs.get(word_file[0].strip()):
                    pointer = pub_index_abs.get(word_file[0].strip())
                elif search_type == "docs" and pub_index_docs.get(word_file[0].strip()):
                    pointer = pub_index_docs.get(word_file[0].strip())
                elif search_type == "author" and author_index.get(word_file[0].strip()):
                    pointer = author_index.get(word_file[0].strip())
                if len(pointer) == 0:
                    output_data = {}
                else:
                    for j in pointer:
                        if search_type == "publication":
                            temp_file.append(pub_list_first_stem[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_stem_abs[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_stem_docs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_stem[j])
                    temp_file1 = tfidf.fit_transform(temp_file)
                    if ranking_choice =='Sklearn Function':
                        output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                    else:
                      
                        i =0
                        matrix = []
                        for elem in temp_file:
                            elem = tf_idf_vectorizer(elem.split())[0]
                            matrix.append(elem)
                            i+=1

                        mat_inv = tf_idf_vectorizer(word_file)
                        output = cosseno_sim(matrix, mat_inv)
                        
                    for j in pointer:
                        output_data[j] = output[pointer.index(j)]


                        
            elif strategy == 'Lemmatization':
                if search_type == "publication" and pub_index_lemma.get(word_file[0].strip()):
                    pointer = pub_index_lemma.get(word_file[0].strip())
                elif search_type == "abstracts" and pub_index_lemma_abs.get(word_file[0].strip()):
                    pointer = pub_index_lemma_abs.get(word_file[0].strip())
                elif search_type == "docs" and pub_index_lemma_docs.get(word_file[0].strip()):
                    pointer = pub_index_lemma_docs.get(word_file[0].strip())
                elif search_type == "author" and author_index_lemma.get(word_file[0].strip()):
                    pointer = author_index_lemma.get(word_file[0].strip())
                if len(pointer) == 0:
                    output_data = {}
                else:
                    for j in pointer:
                        if search_type == "publication":
                            temp_file.append(pub_list_first_lemma[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_lemma_abs[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_lemma_docs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_lemma[j])

                    temp_file1 = tfidf.fit_transform(temp_file)
                    if ranking_choice =='Sklearn Function':
                        output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                    else:
                      
                        i =0
                        matrix = []
                        for elem in temp_file:
                            elem = tf_idf_vectorizer(elem.split())[0]
                            matrix.append(elem)
                            i+=1

                        mat_inv = tf_idf_vectorizer(word_file)
                        output = cosseno_sim(matrix, mat_inv)
                        
                    for j in pointer:
                        output_data[j] = output[pointer.index(j)]
        
    elif operator_val == 1 :  # AND Operator
        input_text = input_text.lower().split()
        pointer = []
        match_word = []
        for token in input_text:
            if len(input_text) < 2:
                st.warning("Please enter at least 2 words to apply the operator.")
                break
            temp_file = []
            set2 = set()
            word_file = []
            word_list = word_tokenize(token)
            stem_temp = ""
            for x in word_list:
                if x not in stop_words:
                    if strategy == 'Stemming':
                        stem_temp += stemmer.stem(x) + " "
                    elif strategy == 'Lemmatization':
                        stem_temp += lemmatizer.lemmatize(x) + " "
            word_file.append(stem_temp)
            if strategy == 'Stemming':
                if search_type == "publication" and pub_index.get(word_file[0].strip()):
                    set1 = set(pub_index.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "abstracts" and pub_index_abs.get(word_file[0].strip()):
                    set1 = set(pub_index_abs.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "docs" and pub_index_docs.get(word_file[0].strip()):
                    set1 = set(pub_index_docs.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "author" and author_index.get(word_file[0].strip()):
                    set1 = set(author_index.get(word_file[0].strip()))
                    pointer.extend(list(set1))

                if match_word == []:
                    match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                else:
                    match_word.extend(list(set1))
                    match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})

            elif strategy == 'Lemmatization':
                if search_type == "publication" and pub_index_lemma.get(word_file[0].strip()):
                    set1 = set(pub_index_lemma.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "abstracts" and pub_index_lemma_abs.get(word_file[0].strip()):
                    set1 = set(pub_index_lemma_abs.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "docs" and pub_index_lemma_docs.get(word_file[0].strip()):
                    set1 = set(pub_index_lemma_docs.get(word_file[0].strip()))
                    pointer.extend(list(set1))
                elif search_type == "author" and author_index_lemma.get(word_file[0].strip()):
                    set1 = set(author_index_lemma.get(word_file[0].strip()))
                    pointer.extend(list(set1))

                if match_word == []:
                    match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                else:
                    match_word.extend(list(set1))
                    match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})

        if len(input_text) > 1:
            match_word = {z for z in match_word if z in set2 or (set2.add(z) or False)}

            if len(match_word) == 0:
                output_data = {}
            else:
                for j in list(match_word):
                    if  strategy == 'Stemming':
                        if search_type == "publication":
                            temp_file.append(pub_list_first_stem[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_stem_abs[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_stem_docs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_stem[j])
                    elif strategy == 'Lemmatization':
                        if search_type == "publication":
                            temp_file.append(pub_list_first_lemma[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_lemma_docs[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_lemma_abs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_lemma[j])

                temp_file1 = tfidf.fit_transform(temp_file)
                
                if ranking_choice =='Sklearn Function':
                    output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                else:
                    i =0
                    matrix = []
                    for elem in temp_file:
                        elem = tf_idf_vectorizer(elem.split())[0]
                        matrix.append(elem)
                        i+=1

                    mat_inv = tf_idf_vectorizer(word_file)
                    output = cosseno_sim(matrix, mat_inv)   
                
                for j in list(match_word):
                    output_data[j] = output[list(match_word).index(j)]
        else:   
            if len(pointer) == 0:
                output_data = {}
            else:
                for j in pointer:
                    if  strategy == 'Stemming':
                        if search_type == "publication":
                            temp_file.append(pub_list_first_stem[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_stem_abs[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_stem_docs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_stem[j])
                    elif strategy == 'Lemmatization':
                        if search_type == "publication":
                            temp_file.append(pub_list_first_lemma[j])
                        elif search_type == "abstracts":
                            temp_file.append(pub_list_first_lemma_abs[j])
                        elif search_type == "docs":
                            temp_file.append(pub_list_first_lemma_docs[j])
                        elif search_type == "author":
                            temp_file.append(author_list_first_lemma[j])
                temp_file1 = tfidf.fit_transform(temp_file)
                if ranking_choice =='Sklearn Function':
                        output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                else:  
                    i =0
                    matrix = []
                    for elem in temp_file:
                        elem = tf_idf_vectorizer(elem.split())[0]
                        matrix.append(elem)
                        i+=1

                    mat_inv = tf_idf_vectorizer(word_file)
                    output = cosseno_sim(matrix, mat_inv)
                        
                for j in pointer:
                    output_data[j] = output[pointer.index(j)]
    elif operator_val == 3: 
    # NOT Operator
        pointer = []
        input_text = input_text.lower().strip()  # Remover espaços em branco extras
        stem_temp = ""
        word_file = []
        temp_file = []

        # Aplicar stemming ou lematização, conforme necessário
        if strategy == 'Stemming':
            stem_temp += stemmer.stem(input_text) + " "
        elif strategy == 'Lemmatization':
            stem_temp += lemmatizer.lemmatize(input_text) + " "

        word_file.append(stem_temp)

        if strategy == 'Stemming':
            # Verificar o tipo de pesquisa e o índice correspondente
            if search_type == "publication" and pub_index.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_stem)) if i not in pub_index.get(word_file[0].strip())]
            elif search_type == "abstracts" and pub_index_abs.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_stem_abs)) if i not in pub_index_abs.get(word_file[0].strip())]
            elif search_type == "docs" and pub_index_docs.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_stem_docs)) if i not in pub_index_docs.get(word_file[0].strip())]
            elif search_type == "author" and author_index.get(word_file[0].strip()):
                pointer = [i for i in range(len(author_list_first_stem)) if i not in author_index.get(word_file[0].strip())]

            if len(pointer) == 0:
                output_data = {}
            else:
                for j in pointer:
                    # Adicionar os documentos correspondentes à lista temporária
                    if search_type == "publication":
                        temp_file.append(pub_list_first_stem[j])
                    elif search_type == "abstracts":
                        temp_file.append(pub_list_first_stem_abs[j])
                    elif search_type == "docs":
                        temp_file.append(pub_list_first_stem_docs[j])
                    elif search_type == "author":
                        temp_file.append(author_list_first_stem[j])

                # Calcular a similaridade de cosseno
                temp_file1 = tfidf.fit_transform(temp_file)
                if ranking_choice =='Sklearn Function':
                        output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                else:
                    i =0
                    matrix = []
                    for elem in temp_file:
                        elem = tf_idf_vectorizer(elem.split())[0]
                        matrix.append(elem)
                        i+=1

                    mat_inv = tf_idf_vectorizer(word_file)
                    output = cosseno_sim(matrix, mat_inv)
                        
                for j in pointer:
                        output_data[j] = output[pointer.index(j)]

        elif strategy == 'Lemmatization':
            if search_type == "publication" and pub_index_lemma.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_lemma)) if i not in pub_index_lemma.get(word_file[0].strip())]
            elif search_type == "abstracts" and pub_index_lemma_abs.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_lemma_abs)) if i not in pub_index_lemma_abs.get(word_file[0].strip())]
            elif search_type == "docs" and pub_index_lemma_docs.get(word_file[0].strip()):
                pointer = [i for i in range(len(pub_list_first_lemma_docs)) if i not in pub_index_lemma_docs.get(word_file[0].strip())]
            elif search_type == "author" and author_index_lemma.get(word_file[0].strip()):
                pointer = [i for i in range(len(author_list_first_lemma)) if i not in author_index_lemma.get(word_file[0].strip())]

            if len(pointer) == 0:
                output_data = {}
            else:
                for j in pointer:
                    if search_type == "publication":
                        temp_file.append(pub_list_first_lemma[j])
                    elif search_type == "abstracts":
                        temp_file.append(pub_list_first_lemma_abs[j])
                    elif search_type == "docs":
                        temp_file.append(pub_list_first_lemma_docs[j])
                    elif search_type == "author":
                        temp_file.append(author_list_first_lemma[j])

                temp_file1 = tfidf.fit_transform(temp_file)
                
                if ranking_choice =='Sklearn Function':
                        output = cosine_similarity(temp_file1, tfidf.transform(word_file))
                        
                else:
                      
                        i =0
                        matrix = []
                        for elem in temp_file:
                            elem = tf_idf_vectorizer(elem.split())[0]
                            matrix.append(elem)
                            i+=1

                        mat_inv = tf_idf_vectorizer(word_file)
                        output = cosseno_sim(matrix, mat_inv)
                        
                for j in pointer:
                    output_data[j] = output[pointer.index(j)]
                
    elif operator_val == 4:
        processed_text = process_text(input_text, strategy)
        input_text = input_text.lower().split()
        output_data = {}
       
        if 'or' in input_text:
            or_indexes = [i for i, x in enumerate(input_text) if x == "or"]
            for or_index in or_indexes:
                word_1 = input_text[or_index - 1]
                word_2 = input_text[or_index + 1]
                word_input = word_1 + ' ' + word_2
                if output_data:  # Verifica se há resultados de operador OR para interseccionar
                    output_data = {k: v for k, v in output_data.items() if k in search_data(word_input, 2, search_type, strategy,ranking_choice)}
                # Atualiza o dicionário com os resultados do operador OR
                else:
                    output_data.update(search_data(word_input, 2, search_type, strategy,ranking_choice))
        if 'and' in input_text:
            and_indexes = [i for i, x in enumerate(input_text) if x == "and"]
            for and_index in and_indexes:
                word_1 = input_text[and_index - 1]
                word_2 = input_text[and_index + 1]
                word_input = word_1 + ' ' + word_2
                # Atualiza o dicionário com os resultados do operador AND
                if output_data:  # Verifica se há resultados de operador OR para interseccionar
                    output_data = {k: v for k, v in output_data.items() if k in search_data(word_input, 1, search_type, strategy,ranking_choice)}
                else:
                    output_data.update(search_data(word_input, 1, search_type, strategy,ranking_choice))

        if 'not' in input_text:
                not_index = input_text.index("not")
                word_1 = input_text[not_index + 1]
                # Chama search_data() com operador 3 (NOT) e armazena os resultados na seccao_1
                seccao_1 = search_data(word_1,3 , search_type, strategy,ranking_choice)
                if output_data:  # Verifica se há resultados de operador OR para interseccionar
                    output_data = {k: v for k, v in output_data.items() if k in seccao_1}
                else:
                    output_data=seccao_1
          


    return output_data
 
def show_pdfs():
    pdf_dir = '/home/maryy/TPRATICO/' 
    pdf_files = [file for file in os.listdir(pdf_dir) if file.endswith('.pdf')]
    if pdf_files:
        st.markdown("### Available PDFs:")
        c=0
        for pdf_file in pdf_files:
            c+=1
            number = re.search(r'\d+', pdf_file).group()
            st.markdown(f"- [View PDF {number}]({'http://localhost:8000/' + pdf_file})", unsafe_allow_html=True)
    else:
        st.info("No Available Documents.")

   
def app():

    # Load the image and display it
    image = Image.open('logo.png')
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(image,caption='University of Minho',width=200)
   

    # Add a text description
    st.markdown("<p style='text-align: center;'>Information Retrieval</p>", unsafe_allow_html=True)


    input_text = st.text_input("Search research:", key="query_input")
    operator_val = st.radio(
        "Search Filters",
        ['AND', 'OR', 'NOT', 'All operators'],
        index=1,
        key="operator_input",
        horizontal=True,
    )
    search_type = st.radio(
        "Search in:",
        ['Titles', 'Abstracts','Authors', 'C.I.H Documents'],
        index=0,
        key="search_type_input",
        horizontal=True,
    )
    
    # Adicionar botões de seleção para a estratégia de indexação
    strategy = st.radio(
    "Select indexing strategy:", 
    ['Stemming', 'Lemmatization'], 
    index=0, 
    key="strategy", 
    horizontal=True,
)
    ranking_choice = st.radio(
        "Choose ranking method:",
        ['Sklearn Function', 'Custom Implementation'],
        index=0,
        key="ranking_choice",
        horizontal=True,
    )
 
    if st.button("SEARCH"):
        if search_type == "Titles":
            output_data = search_data(input_text, 1 if operator_val == 'AND' else (2 if operator_val == 'OR' else (3 if operator_val == 'NOT' else 4 ) ), "publication", strategy,ranking_choice)
        elif search_type == "Abstracts":
            output_data = search_data(input_text, 1 if operator_val == 'AND' else (2 if operator_val == 'OR' else (3 if operator_val == 'NOT' else 4 ) ), "abstracts", strategy,ranking_choice)

        elif search_type == "Authors":
            output_data = search_data(input_text, 1 if operator_val == 'AND' else (2 if operator_val == 'OR' else (3 if operator_val == 'NOT' else 4 ) ), "author", strategy,ranking_choice)
        
        elif search_type == "C.I.H Documents":
            output_data = search_data(input_text, 1 if operator_val == 'AND' else (2 if operator_val == 'OR' else (3 if operator_val == 'NOT' else 4 ) ), "docs", strategy,ranking_choice)
        
        else:
            output_data = {}
            

        # Display the search results
        show_results(output_data, search_type, input_text)

    elif st.button(" All Centre for Intelligent Healthcare Documents saved"):
        show_pdfs()

    st.markdown("<p style='text-align: center;'> By Madalena Passos, Mariana Almeida and Mariana Ribeiro", unsafe_allow_html=True)


def show_results(output_data, search_type, input_text):
    aa = 0
    rank_sorting = sorted(output_data.items(), key=lambda z: z[1], reverse=True)
    # Show the total number of research results
    st.info(f"Showing results for: {len(rank_sorting)}")

    # Show the cards
    N_cards_per_row = 3
    for n_row, (id_val, ranking) in enumerate(rank_sorting):
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # Draw the card
        with cols[n_row % N_cards_per_row]:
            if search_type == "Titles":
                st.caption(f"{pub_date[id_val].strip()}")
                st.markdown(f"**{pub_cu_author[id_val].strip()}**")
                for word in input_text.split():
                    if word in pub_name[id_val] or word.lower() in pub_abst[id_val]:
                        if word not in stop_words:
                            word_escaped = re.escape(word)
                            pub_name[id_val] = re.sub(rf'\b{word_escaped}\b', r'```' + r'\g<0>' + r'```', pub_name[id_val], flags=re.IGNORECASE)

                st.markdown(f"*{pub_name[id_val].strip()}*")
                st.markdown(f"[View]({pub_url[id_val]})")
                st.markdown(f"Ranking: {ranking[0]:.5f}")

            elif search_type=="Abstracts": 
                st.caption(f"{pub_date[id_val].strip()}")
                st.markdown(f"**{pub_name[id_val].strip()}**")
                
                #   st.markdown(f"{pub_cu_author[id_val].strip()}")
                st.markdown(f"<span style='color: gray;'>{pub_cu_author[id_val].strip()}</span>", unsafe_allow_html=True)
                
                highlighted_text = pub_abst[id_val]
                resultado=""
                for word in input_text.split():
                    if word.lower() in highlighted_text.lower() and word not in stop_words:
                        word_escaped = re.escape(word)
                        match = re.search(rf'\b{word_escaped}\b', highlighted_text, flags=re.IGNORECASE)
                        if match:
                            start = max(match.start() - 150, 0)
                            end = min(match.end() + 150, len(highlighted_text))
                            snippet = highlighted_text[start:end]
                            snippet = re.sub(rf'\b{word_escaped}\b', r'```' + r'\g<0>' + r'```', snippet, flags=re.IGNORECASE)
                            resultado=resultado + " ... "+ snippet
                            
                if resultado=="":
                    # meter fim e inicio
                   resultado = pub_abst[id_val][:300]
                   st.markdown(f"*... {resultado} ...*")
                else:
                    st.markdown(f"*... {resultado} ...*")

                st.markdown(f"Ranking: {ranking[0]:.5f}")
                st.markdown(f"[View]({pub_url[id_val]})")
            
                                                                
            elif search_type == "Authors":
                st.caption(f"{pub_date[id_val].strip()}")
                st.markdown(f"**{author_name[id_val].strip()}**")
                st.markdown(f"*{pub_name[id_val].strip()}*")
                st.markdown(f"[View]({pub_url[id_val]})")
                st.markdown(f"Ranking: {ranking[0]:.2f}")

            elif search_type == "C.I.H Documents":
                doc_name_clean = doc_name[id_val].strip()
                number = re.search(r'\d+', doc_name_clean).group()  
                doc_path = "http://localhost:8000/" + doc_name_clean  
                doc_link = f"[View PDF {number}]({doc_path})"  
                st.markdown(f"- {doc_link}")    
                st.markdown(f"Ranking: {ranking[0]:.5f}")

        aa += 1

    if aa == 0:
        st.info("No results found. Please try again.")
    else:
        st.info(f"Results shown for: {aa}")


if __name__ == '__main__':
    app()