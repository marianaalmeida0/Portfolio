
import numpy as np

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


def custom_cosine_similarity(corpus_unsplit, querry):


    corpus = [c.split() for c in corpus_unsplit]
    num_documents = len(corpus)
    word_set = list(set(sum(corpus, [])))
    # create a lookup for each word to it's index, 
    word_to_index = {word:i for i, word in enumerate(word_set)}

    num_words = len(word_set)
    word_vectors = []
    for document in corpus:
        # for our new document create a new word vector
        new_word_vector = [0 for i in range(num_words)]
        
        # now we loop through each word in our document and compute the tf-idf score and populate our vector with it,
        # we only care about words in this document because words outside of it will remain zero
        for word in document:
            # get the score
            tf_idf_score = TF_IDF(word, document, corpus)
            # next get the index for this word in our word vector
            word_index = word_to_index[word] 
            # populate the vector
            new_word_vector[word_index] = tf_idf_score
        
        # don't forget to add this new word vector to our list of existing word_vectors
        word_vectors.append(new_word_vector)


    
    querry_keywords = querry.split()

    # now we loop through each documents word vector, get the tf-idf score for each keyword, sum them up and that is our tf-idf for that document,
    # we keep track of the best document and return that as our result, 
    tf_idf_scores = []
    best_document_index = 0
    best_tf_idf = 0
    for i, word_vector in enumerate(word_vectors):
        document_tf_idf_score_for_querry = 0
        for word in querry_keywords:
            # first do a check, does this word appear in our corpus of documents?
            # if not skip this keyword
            if word not in word_set:
                continue
            
            # get the index for this keyword and directly pull it from the word vector
            word_index = word_to_index[word]
            document_tf_idf_score_for_querry += word_vector[word_index]
        tf_idf_scores.append(document_tf_idf_score_for_querry) # keep track of all tf_idf scores, just in case we want to review them,

        # does this tf_idf score for this document beat our previous best?
        if document_tf_idf_score_for_querry > best_tf_idf:
            best_tf_idf = document_tf_idf_score_for_querry
            best_document_index = i
        
    # then print out our results
    #print("results of querry: ", querry)
    print("best tf_idf score sum for querry: ", best_tf_idf)
    print("best document: ", corpus_unsplit[best_document_index])
    print("complete list of tf_idf scores: ", tf_idf_scores)
    return tf_idf_scores

corpus_unsplit=[
    "My dog can play fetch really well",
    "I had a dog that didn't really look like a dog but was a dog",
    "dog bunny cat bunny rooster dog pig goat horse dog dog cat cow sealion bird pidgeon penguins and whales and treasure chests and what other random items can go into this long document I wonder",
    "I have a cat",
    "I have a goat",
    "Why is everyone talking about their pets",
    "I have a zebra",
    "You don't have a zebra Timmy"
]
querry= "best document about dog"
print(custom_cosine_similarity(corpus_unsplit, querry))