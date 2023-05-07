import gensim
from gensim import corpora

# Load the dataset
doc1 = "The quick brown fox jumps over the lazy dog"
doc2 = "The brown dog is quick"
doc3 = "The black cat is slow"
doc4 = "The quick brown fox eats the lazy dog"

documents = [doc1, doc2, doc3, doc4]

# Tokenize the documents
texts = [[word for word in document.lower().split()] for document in documents]

# Create a dictionary from the tokenized documents
dictionary = corpora.Dictionary(texts)

# Convert the tokenized documents into a bag-of-words corpus
corpus = [dictionary.doc2bow(text) for text in texts]

# Train an LDA model on the corpus
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary, passes=10)

# Print the topics and their associated words
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")
