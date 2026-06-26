# Word2Vec (Skip-gram)

## Overview
Word2Vec is a groundbreaking technique in Natural Language Processing (NLP) developed by Google in 2013. It's not a single algorithm but a family of models used to create "word embeddings" – dense vector representations of words. These embeddings are numerical vectors that capture the semantic and syntactic relationships between words. Imagine mapping words into a multi-dimensional space where words with similar meanings are located closer to each other.

The "Skip-gram" model is one of the two main architectures within Word2Vec (the other being Continuous Bag-of-Words, or CBOW). Skip-gram's core idea is to predict the surrounding context words given a target word. For example, if the target word is "cat," Skip-gram tries to predict words like "purrs," "meows," "pet," or "animal" that might appear near "cat" in a sentence. By doing this repeatedly across a large text corpus, the model learns meaningful vector representations for each word. These vectors are incredibly powerful because they allow machines to understand and process human language in a much more nuanced way than traditional methods.

## What Problem It Solves
Before Word2Vec, representing words for machine learning models was often done using methods like one-hot encoding. Let's say you have a vocabulary of 10,000 words. "Cat" might be represented as a vector of 10,000 zeros with a single '1' at the 500th position. While simple, this approach has several critical drawbacks:

1.  **High Dimensionality and Sparsity**: For large vocabularies, one-hot vectors are extremely long and mostly empty (sparse). This leads to high computational costs and memory usage.
2.  **Lack of Semantic Meaning**: One-hot vectors treat every word as completely independent. The vector for "cat" has no inherent relationship with the vector for "kitten" or "dog." This means the model cannot understand that "cat" and "kitten" are related, or that "cat" and "dog" are both animals. There's no way to measure similarity or relatedness between words based on their one-hot representations.
3.  **Curse of Dimensionality**: With sparse, high-dimensional data, machine learning models struggle to find meaningful patterns, often requiring vast amounts of data to generalize effectively.

Word2Vec (Skip-gram) addresses these problems by:

*   **Creating Dense Representations**: Instead of sparse vectors of thousands of dimensions, Word2Vec produces dense vectors (typically 50-300 dimensions) where every element has a non-zero value. This significantly reduces dimensionality and memory footprint.
*   **Capturing Semantic and Syntactic Relationships**: The most significant advantage is that these dense vectors encode meaning. Words that are semantically similar (e.g., "king" and "queen") will have vectors that are close to each other in the vector space. Words that are syntactically similar (e.g., "walking" and "running" are both verbs) might also exhibit similar patterns. This allows for analogies like "king - man + woman = queen" to hold true in the vector space.
*   **Enabling Transfer Learning**: Once trained on a large corpus, these word embeddings can be used as features in various downstream NLP tasks (e.g., sentiment analysis, text classification) without needing to train embeddings from scratch for each new task. This saves time and improves performance, especially on smaller datasets.

In essence, Word2Vec (Skip-gram) provides a way for machines to "understand" words not just as unique identifiers, but as points in a meaningful semantic space, bridging the gap between raw text and numerical data that machine learning models can process effectively.

## How It Works
The Skip-gram model works by taking a large corpus of text and learning to predict context words from a target word. Let's break down the process:

1.  **Data Preparation: (Target, Context) Pairs**:
    *   The first step is to prepare the training data. We slide a "window" of a fixed size (e.g., 2 or 5 words) across each sentence in the corpus.
    *   For each word in the corpus, we designate it as the **target word** (also called the input word or center word).
    *   All other words within the window around the target word become **context words** (also called output words).
    *   For example, consider the sentence: "The quick brown fox jumps over the lazy dog."
    *   If "fox" is the target word and our window size is 2, the context words would be "quick", "brown" (to the left) and "jumps", "over" (to the right).
    *   This process generates many (target, context) pairs. For each target word, we generate multiple pairs, one for each context word within its window.

2.  **Model Architecture: A Shallow Neural Network**:
    *   Skip-gram uses a very simple neural network architecture, typically with just two layers: an input layer, a hidden layer, and an output layer. There are no activation functions in the hidden layer, making it essentially a projection layer.
    *   **Input Layer**: This layer takes the one-hot encoded vector of the target word as input. If your vocabulary size is $V$, the input vector will be $V$-dimensional.
    *   **Hidden Layer**: This layer has $N$ neurons, where $N$ is the desired dimensionality of our word embeddings (e.g., 100, 300). The weights connecting the input layer to the hidden layer form the "input word matrix" ($W_{input}$). When a one-hot vector for a target word is fed into the network, it effectively "selects" a row from this $W_{input}$ matrix. This row *is* the word embedding (vector) for that target word.
    *   **Output Layer**: This layer has $V$ neurons, one for each word in the vocabulary. It uses a softmax activation function to output a probability distribution over all words in the vocabulary. This distribution tells us the probability of each word being a context word for the given target word. The weights connecting the hidden layer to the output layer form the "output word matrix" ($W_{output}$). Each column of $W_{output}$ can be thought of as a "context vector" for a word.

3.  **Training Process**:
    *   The goal of training is to adjust the weights (which are our word embeddings) in both the input and output matrices such that the model accurately predicts context words for given target words.
    *   For each (target, context) pair:
        *   The one-hot vector of the target word is fed into the network.
        *   It passes through the hidden layer, where its embedding vector is retrieved.
        *   This embedding vector is then used to calculate scores for all possible context words in the output layer.
        *   The softmax function converts these scores into probabilities.
        *   The model then compares this predicted probability distribution with the actual context word (which is also represented as a one-hot vector).
        *   An error is calculated (e.g., using cross-entropy loss).
        *   This error is backpropagated through the network, and the weights (our word embeddings) are updated using an optimization algorithm like stochastic gradient descent (SGD).

4.  **Optimization Techniques (Crucial for Efficiency)**:
    *   The softmax calculation in the output layer is computationally very expensive because it requires summing over all $V$ words in the vocabulary for every training step. For a large vocabulary, this is prohibitive.
    *   To overcome this, Word2Vec typically employs two main optimization techniques:
        *   **Hierarchical Softmax**: This uses a Huffman tree to represent the vocabulary, reducing the computation from $V$ to $\log(V)$.
        *   **Negative Sampling**: This is the more commonly used and generally preferred method. Instead of predicting all context words, it transforms the problem into a binary classification task. For each (target, context) pair, it samples a small number of "negative" (non-context) words from the vocabulary. The model then learns to distinguish the actual context word from these randomly sampled negative words. This significantly reduces the computational cost per training step.

5.  **Result: Word Embeddings**:
    *   After training, the weights in the hidden layer (the $W_{input}$ matrix) become our learned word embeddings. Each row of this matrix corresponds to the dense vector representation of a word in our vocabulary. These vectors are what we use for downstream NLP tasks. Sometimes, the output matrix ($W_{output}$) is also used, or an average of both.

In summary, Skip-gram learns word embeddings by training a simple neural network to predict the surrounding words given a central word. The magic lies in the fact that words that frequently appear in similar contexts will end up having similar vector representations.

## Mathematical Intuition

Let's dive into the mathematical underpinnings of the Skip-gram model.

### 1. Word Representations
Each word $w$ in our vocabulary $V$ is associated with two vectors:
*   An "input" or "center" vector, $v_w \in \mathbb{R}^d$. This is the vector we typically use as the word embedding.
*   An "output" or "context" vector, $u_w \in \mathbb{R}^d$. This vector is used when $w$ appears as a context word.

Here, $d$ is the dimensionality of the word embeddings (e.g., 100 or 300).

### 2. Probability of a Context Word
The core idea of Skip-gram is to maximize the probability of observing a context word $w_o$ given a target word $w_c$. This probability is modeled using the softmax function:

$$P(w_o | w_c) = \frac{\exp(u_{w_o}^T v_{w_c})}{\sum_{w' \in V} \exp(u_{w'}^T v_{w_c})}$$

Let's break this down:
*   $u_{w_o}^T v_{w_c}$: This is the dot product between the context vector of the output word $w_o$ and the input vector of the center word $w_c$. The dot product measures the similarity between two vectors. A higher dot product means the words are more similar or frequently co-occur.
*   $\exp(\cdot)$: The exponential function ensures that the values are positive.
*   $\sum_{w' \in V} \exp(u_{w'}^T v_{w_c})$: This is the normalization term, summing the exponentiated dot products for *all* words in the vocabulary $V$ with respect to the center word $w_c$. This ensures that the probabilities sum to 1.

### 3. Objective Function (Log-Likelihood)
The goal of training is to find the word vectors ($v_w$ and $u_w$ for all $w \in V$) that maximize the overall probability of observing the context words given the target words across the entire corpus. This is typically formulated as maximizing the log-likelihood:

$$J = \sum_{t=1}^T \sum_{-m \le j \le m, j \ne 0} \log P(w_{t+j} | w_t)$$

Where:
*   $T$ is the total number of words in the corpus.
*   $w_t$ is the target word at position $t$.
*   $w_{t+j}$ is a context word within the window of size $m$ around $w_t$.
*   $m$ is the window size. We sum over all context words within this window.
*   $\log P(w_{t+j} | w_t)$: This is the log probability of observing the context word $w_{t+j}$ given the target word $w_t$, as defined by the softmax function above. Taking the logarithm simplifies calculations and turns products into sums.

The training process involves using an optimization algorithm (like stochastic gradient descent) to iteratively adjust all $v_w$ and $u_w$ vectors to maximize this objective function.

### 4. Computational Challenge and Negative Sampling
The softmax function's denominator involves summing over the entire vocabulary $V$. If $V$ is large (e.g., 100,000 words), this calculation is extremely slow for every training step.

To address this, **Negative Sampling** is introduced. Instead of updating all $V$ output weights, Negative Sampling converts the multi-class classification problem into a binary classification problem. For each (target, context) pair, we treat the actual context word as a "positive" example and randomly sample a small number ($k$) of "negative" words from the vocabulary.

The new objective function for a single (target, context) pair $(w_c, w_o)$ with $k$ negative samples $w_1, \dots, w_k$ is:

$$J_{neg}(w_o, w_c) = \log \sigma(u_{w_o}^T v_{w_c}) + \sum_{i=1}^k E_{w_i \sim P_n(w)} [\log \sigma(-u_{w_i}^T v_{w_c})]$$

Where:
*   $\sigma(x) = \frac{1}{1 + e^{-x}}$ is the sigmoid function, which squashes values between 0 and 1, representing a probability.
*   $\log \sigma(u_{w_o}^T v_{w_c})$: This term aims to maximize the probability that the actual context word $w_o$ is a "positive" sample (i.e., its dot product with $v_{w_c}$ is high).
*   $\sum_{i=1}^k E_{w_i \sim P_n(w)} [\log \sigma(-u_{w_i}^T v_{w_c})]$: This term aims to minimize the probability that the randomly sampled "negative" words $w_i$ are positive samples (i.e., their dot products with $v_{w_c}$ are low). The negative sign inside the sigmoid makes $\sigma(-x)$ small when $x$ is large, effectively pushing down the similarity for negative samples.
*   $P_n(w)$ is the noise distribution from which negative samples are drawn, typically based on the unigram distribution of words raised to the power of 3/4.

By using Negative Sampling, we only update the weights for the positive context word and a few negative words, drastically speeding up training while still learning high-quality embeddings.

## Advantages
*   **Captures Semantic and Syntactic Relationships**: The primary advantage is its ability to learn word vectors that reflect the meaning and grammatical roles of words. This allows for tasks like finding synonyms, analogies, and understanding word relationships.
*   **Dense and Low-Dimensional Representations**: Unlike sparse one-hot encodings, Word2Vec produces dense vectors, which are more efficient for storage and computation, and mitigate the curse of dimensionality.
*   **Efficient Training**: With optimizations like Negative Sampling or Hierarchical Softmax, Word2Vec can be trained efficiently on very large text corpora, even with millions of words.
*   **Transfer Learning**: Pre-trained Word2Vec embeddings can be used as features in various downstream NLP tasks, often leading to better performance, especially when task-specific training data is limited.
*   **Flexibility**: The model is relatively simple and can be easily adapted or extended.
*   **Handles Large Vocabularies**: Can effectively learn embeddings for hundreds of thousands or even millions of words.

## Disadvantages
*   **Out-of-Vocabulary (OOV) Words**: Word2Vec cannot generate embeddings for words not seen during training. These OOV words are typically handled by assigning them a random vector, a zero vector, or an `<UNK>` (unknown) token vector, which can degrade performance.
*   **Ignores Subword Information**: Word2Vec treats each word as an atomic unit. It doesn't consider the internal structure of words (e.g., prefixes, suffixes, roots). This means "unhappy" and "happy" are treated as distinct words, even though they share a common root and meaning. This is particularly problematic for morphologically rich languages.
*   **Context-Independent Embeddings**: Each word has a single, fixed embedding regardless of its context. This means polysemous words (words with multiple meanings, like "bank" – river bank vs. financial bank) will have a single vector that tries to average out all its meanings, which can be suboptimal.
*   **Requires Large Corpora**: To learn high-quality, robust embeddings, Word2Vec needs a very large amount of text data. Performance can be poor on small datasets.
*   **Hyperparameter Tuning**: Performance is sensitive to hyperparameters like embedding dimension, window size, number of negative samples, and learning rate, which often require careful tuning.
*   **Training Time**: While efficient for its task, training on truly massive corpora can still take a significant amount of time and computational resources.

## Real World Applications
Word2Vec (Skip-gram) embeddings have become a fundamental building block in many NLP systems and are widely used across various industries:

1.  **Recommendation Systems**: By representing items (e.g., movies, products, articles) as "words" and user interaction sequences (e.g., viewing history, purchase history) as "sentences," Word2Vec can learn embeddings for items. Items with similar embeddings can then be recommended to users. For example, if a user watches "Movie A" and "Movie B," and "Movie C" has a similar embedding to "Movie A," "Movie C" might be recommended.
2.  **Sentiment Analysis and Text Classification**: Word embeddings provide rich features for machine learning models. Instead of using sparse bag-of-words or TF-IDF, the average or sum of Word2Vec embeddings for words in a document can be used as input to classifiers (e.g., SVM, Logistic Regression, Neural Networks) to determine sentiment (positive/negative), categorize news articles, or detect spam.
3.  **Information Retrieval and Search Engines**: Word2Vec can improve search relevance. If a user searches for "car repair," and the system has embeddings, it can also retrieve documents containing "auto mechanic" or "vehicle service" because these terms have similar vector representations, even if the exact keywords aren't present. This enables semantic search.
4.  **Machine Translation**: Word embeddings can be used in neural machine translation models to represent words in both source and target languages. By understanding the semantic relationships between words, these models can produce more accurate and fluent translations.
5.  **Question Answering Systems**: In QA systems, Word2Vec embeddings help in understanding the semantic similarity between a user's question and potential answers or relevant passages in a knowledge base. If a question contains "capital of France," the system can match it to "Paris" even if the exact phrase isn't present in the answer.

## Mathematical Intuition

Let's dive into the mathematical underpinnings of the Skip-gram model.

### 1. Word Representations
Each word $w$ in our vocabulary $V$ is associated with two vectors:
*   An "input" or "center" vector, $v_w \in \mathbb{R}^d$. This is the vector we typically use as the word embedding.
*   An "output" or "context" vector, $u_w \in \mathbb{R}^d$. This vector is used when $w$ appears as a context word.

Here, $d$ is the dimensionality of the word embeddings (e.g., 100 or 300).

### 2. Probability of a Context Word
The core idea of Skip-gram is to maximize the probability of observing a context word $w_o$ given a target word $w_c$. This probability is modeled using the softmax function:

$$P(w_o | w_c) = \frac{\exp(u_{w_o}^T v_{w_c})}{\sum_{w' \in V} \exp(u_{w'}^T v_{w_c})}$$

Let's break this down:
*   $u_{w_o}^T v_{w_c}$: This is the dot product between the context vector of the output word $w_o$ and the input vector of the center word $w_c$. The dot product measures the similarity between two vectors. A higher dot product means the words are more similar or frequently co-occur.
*   $\exp(\cdot)$: The exponential function ensures that the values are positive.
*   $\sum_{w' \in V} \exp(u_{w'}^T v_{w_c})$: This is the normalization term, summing the exponentiated dot products for *all* words in the vocabulary $V$ with respect to the center word $w_c$. This ensures that the probabilities sum to 1.

### 3. Objective Function (Log-Likelihood)
The goal of training is to find the word vectors ($v_w$ and $u_w$ for all $w \in V$) that maximize the overall probability of observing the context words given the target words across the entire corpus. This is typically formulated as maximizing the log-likelihood:

$$J = \sum_{t=1}^T \sum_{-m \le j \le m, j \ne 0} \log P(w_{t+j} | w_t)$$

Where:
*   $T$ is the total number of words in the corpus.
*   $w_t$ is the target word at position $t$.
*   $w_{t+j}$ is a context word within the window of size $m$ around $w_t$.
*   $m$ is the window size. We sum over all context words within this window.
*   $\log P(w_{t+j} | w_t)$: This is the log probability of observing the context word $w_{t+j}$ given the target word $w_t$, as defined by the softmax function above. Taking the logarithm simplifies calculations and turns products into sums.

The training process involves using an optimization algorithm (like stochastic gradient descent) to iteratively adjust all $v_w$ and $u_w$ vectors to maximize this objective function.

### 4. Computational Challenge and Negative Sampling
The softmax function's denominator involves summing over the entire vocabulary $V$. If $V$ is large (e.g., 100,000 words), this calculation is extremely slow for every training step.

To address this, **Negative Sampling** is introduced. Instead of updating all $V$ output weights, Negative Sampling converts the multi-class classification problem into a binary classification problem. For each (target, context) pair, we treat the actual context word as a "positive" example and randomly sample a small number ($k$) of "negative" words from the vocabulary.

The new objective function for a single (target, context) pair $(w_c, w_o)$ with $k$ negative samples $w_1, \dots, w_k$ is:

$$J_{neg}(w_o, w_c) = \log \sigma(u_{w_o}^T v_{w_c}) + \sum_{i=1}^k E_{w_i \sim P_n(w)} [\log \sigma(-u_{w_i}^T v_{w_c})]$$

Where:
*   $\sigma(x) = \frac{1}{1 + e^{-x}}$ is the sigmoid function, which squashes values between 0 and 1, representing a probability.
*   $\log \sigma(u_{w_o}^T v_{w_c})$: This term aims to maximize the probability that the actual context word $w_o$ is a "positive" sample (i.e., its dot product with $v_{w_c}$ is high).
*   $\sum_{i=1}^k E_{w_i \sim P_n(w)} [\log \sigma(-u_{w_i}^T v_{w_c})]$: This term aims to minimize the probability that the randomly sampled "negative" words $w_i$ are positive samples (i.e., their dot products with $v_{w_c}$ are low). The negative sign inside the sigmoid makes $\sigma(-x)$ small when $x$ is large, effectively pushing down the similarity for negative samples.
*   $P_n(w)$ is the noise distribution from which negative samples are drawn, typically based on the unigram distribution of words raised to the power of 3/4.

By using Negative Sampling, we only update the weights for the positive context word and a few negative words, drastically speeding up training while still learning high-quality embeddings.

## Python Example

This example uses the `gensim` library, which is a popular and efficient library for Word2Vec in Python. We'll create a dummy corpus, train a Skip-gram model, and then explore the learned embeddings.

```python
import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import numpy as np

# Download necessary NLTK data (only run once)
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

# 1. Generate or load a dummy dataset
# A list of sentences representing our text corpus
corpus = [
    "The quick brown fox jumps over the lazy dog.",
    "I love to eat apples and bananas.",
    "The dog barks loudly at the cat.",
    "Cats and dogs are common pets.",
    "The fox is a clever animal.",
    "Apples are healthy fruits.",
    "Bananas are yellow and sweet."
]

print("Original Corpus:")
for sentence in corpus:
    print(sentence)
print("-" * 30)

# 2. Preprocess the text: Tokenization
# Word2Vec expects a list of lists of words (tokens)
tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

print("\nTokenized Corpus:")
for tokens in tokenized_corpus:
    print(tokens)
print("-" * 30)

# 3. Fit the model/operation: Train Word2Vec (Skip-gram)
# Parameters:
#   vector_size: Dimensionality of the word vectors.
#   window: The maximum distance between the current and predicted word within a sentence.
#   min_count: Ignores all words with total frequency lower than this.
#   sg: Training algorithm: 1 for skip-gram, 0 for CBOW.
#   epochs: Number of iterations (epochs) over the corpus.
#   workers: Use these many worker threads to train the model.
#   negative: If > 0, negative sampling will be used, the number of "noise words" to draw.
model = Word2Vec(
    sentences=tokenized_corpus,
    vector_size=100,      # 100-dimensional word vectors
    window=5,             # Context window size of 5 words
    min_count=1,          # Include all words that appear at least once
    sg=1,                 # Use Skip-gram model
    epochs=100,           # Train for 100 epochs
    workers=4,            # Use 4 CPU cores for training
    negative=5            # Use 5 negative samples
)

print("\nWord2Vec (Skip-gram) model trained successfully!")
print("-" * 30)

# 4. Make predictions/results and evaluate or print the output

# Get the vector for a specific word
word_vector_dog = model.wv['dog']
print(f"Vector for 'dog' (first 5 dimensions): {word_vector_dog[:5]}...")
print(f"Vector dimension for 'dog': {len(word_vector_dog)}")
print("-" * 30)

# Find most similar words
print("Words most similar to 'dog':")
similar_words_dog = model.wv.most_similar('dog', topn=3)
for word, similarity in similar_words_dog:
    print(f"  {word}: {similarity:.4f}")
print("-" * 30)

print("Words most similar to 'fox':")
similar_words_fox = model.wv.most_similar('fox', topn=3)
for word, similarity in similar_words_fox:
    print(f"  {word}: {similarity:.4f}")
print("-" * 30)

print("Words most similar to 'apples':")
similar_words_apples = model.wv.most_similar('apples', topn=3)
for word, similarity in similar_words_apples:
    print(f"  {word}: {similarity:.4f}")
print("-" * 30)

# Demonstrate word analogies (King - Man + Woman = Queen)
# Note: With a small corpus, analogies might not be perfect, but we can try.
# Let's try a simpler analogy: "dog" - "barks" + "meows" should be somewhat close to "cat"
# This requires words to be present in the vocabulary and sufficient training data.
try:
    analogy_result = model.wv.most_similar(positive=['dog', 'meows'], negative=['barks'], topn=1)
    print(f"Analogy: 'dog' - 'barks' + 'meows' is similar to:")
    for word, similarity in analogy_result:
        print(f"  {word}: {similarity:.4f}")
except KeyError as e:
    print(f"Could not perform analogy due to missing word in vocabulary: {e}")
    print("Analogy results are often better with larger, more diverse corpora.")
print("-" * 30)

# Check similarity between two words
similarity_dog_cat = model.wv.similarity('dog', 'cat')
similarity_dog_apples = model.wv.similarity('dog', 'apples')
print(f"Similarity between 'dog' and 'cat': {similarity_dog_cat:.4f}")
print(f"Similarity between 'dog' and 'apples': {similarity_dog_apples:.4f}")
print("-" * 30)

# Get the entire vocabulary
print(f"Vocabulary size: {len(model.wv.index_to_key)}")
print(f"First 10 words in vocabulary: {model.wv.index_to_key[:10]}")
print("-" * 30)

# Save and load the model
model.save("word2vec_skipgram_model.bin")
print("Model saved as 'word2vec_skipgram_model.bin'")

loaded_model = Word2Vec.load("word2vec_skipgram_model.bin")
print("Model loaded successfully!")
print(f"Loaded model's vector for 'dog' (first 5 dimensions): {loaded_model.wv['dog'][:5]}...")
print("-" * 30)

# Out-of-vocabulary word handling
oov_word = "elephant"
if oov_word in model.wv:
    print(f"Vector for '{oov_word}': {model.wv[oov_word][:5]}...")
else:
    print(f"'{oov_word}' is an out-of-vocabulary word and does not have a vector in this model.")
```

**Explanation of the Code:**

1.  **Corpus Creation**: We start with a small list of sentences to simulate a text corpus. In a real-world scenario, this would be a much larger dataset (e.g., Wikipedia, news articles).
2.  **Tokenization**: `nltk.word_tokenize` is used to break down sentences into individual words. We also convert words to lowercase to treat "The" and "the" as the same word. Word2Vec expects a list of lists of tokens.
3.  **Model Training**:
    *   `gensim.models.Word2Vec` is instantiated.
    *   `sentences=tokenized_corpus`: Our prepared data.
    *   `vector_size=100`: Each word will be represented by a 100-dimensional vector.
    *   `window=5`: The model considers 5 words to the left and 5 words to the right of the target word as context.
    *   `min_count=1`: Words appearing less than once are ignored. For this small corpus, we set it to 1 to include all words.
    *   `sg=1`: This is the crucial parameter that specifies we want to use the **Skip-gram** algorithm. `sg=0` would use CBOW.
    *   `epochs=100`: The model will iterate over the entire corpus 100 times to refine the word vectors.
    *   `workers=4`: Utilizes multiple CPU cores for faster training.
    *   `negative=5`: Uses Negative Sampling with 5 negative samples per positive sample, which is a common and efficient optimization.
4.  **Exploring Embeddings**:
    *   `model.wv['word']`: Accesses the vector for a specific word. `wv` stands for "word vectors."
    *   `model.wv.most_similar('word', topn=N)`: Finds the `N` words whose vectors are closest (most similar) to the given word's vector in the embedding space. Similarity is typically measured using cosine similarity.
    *   `model.wv.most_similar(positive=['word1', 'word2'], negative=['word3'])`: Allows for vector arithmetic, demonstrating analogies. For example, `positive=['king', 'woman'], negative=['man']` might yield "queen".
    *   `model.wv.similarity('word1', 'word2')`: Calculates the cosine similarity between two word vectors.
5.  **Saving/Loading**: The trained model can be saved to disk and loaded later, which is essential for production systems or resuming training.
6.  **OOV Handling**: Demonstrates how to check if a word exists in the model's vocabulary. Words not seen during training will not have an embedding.

## Interview Questions

Here are some common interview questions about Word2Vec (Skip-gram) along with detailed answers:

1.  **What are word embeddings, and why are they important?**
    *   **Answer**: Word embeddings are dense, low-dimensional vector representations of words that capture their semantic and syntactic meanings. They are important because traditional word representations (like one-hot encoding) are sparse, high-dimensional, and fail to capture relationships between words. Embeddings allow machine learning models to understand words in context, enabling them to process natural language more effectively, find synonyms, perform analogies, and improve performance on various NLP tasks like sentiment analysis, machine translation, and information retrieval.

2.  **Explain the core idea behind Word2Vec.**
    *   **Answer**: The core idea of Word2Vec is the "distributional hypothesis," which states that words that appear in similar contexts tend to have similar meanings. Word2Vec learns word embeddings by training a shallow neural network to predict words based on their context. It takes a large text corpus and, through this predictive task, learns to map each word to a dense vector such that words with similar meanings are located close to each other in the vector space.

3.  **What is the difference between Skip-gram and CBOW in Word2Vec?**
    *   **Answer**:
        *   **Skip-gram**: Predicts the surrounding context words given a target (center) word. It's like saying, "If I see 'cat', what words are likely to appear around it (e.g., 'purrs', 'meows')?"
        *   **CBOW (Continuous Bag-of-Words)**: Predicts the target (center) word given its surrounding context words. It's like saying, "If I see 'the', 'quick', 'fox', 'jumps', what word is likely in the middle (e.g., 'brown')?"
    *   **Key Differences**: Skip-gram is generally better at handling rare words and phrases because it trains on each context-target pair, effectively giving more weight to rare words. CBOW is typically faster to train and performs well for frequent words.

4.  **Why is Skip-gram often preferred for rare words compared to CBOW?**
    *   **Answer**: Skip-gram is preferred for rare words because it treats each (target, context) pair as a new observation. If a rare word appears, say, 10 times in the corpus, and each time it has 5 context words, Skip-gram will generate 50 training examples where the rare word is the target. CBOW, on the other hand, uses the context to predict the target. If a rare word is the target, it might only be predicted a few times, and its context might be dominated by common words, making its embedding less distinct. Skip-gram's approach effectively "amplifies" the signal from rare words.

5.  **Describe the architecture of the Skip-gram model.**
    *   **Answer**: The Skip-gram model uses a simple, shallow neural network with three layers:
        1.  **Input Layer**: Takes a one-hot encoded vector of the target word.
        2.  **Hidden Layer (Projection Layer)**: This layer has $N$ neurons (where $N$ is the desired embedding dimension). It has no activation function. The weights connecting the input layer to the hidden layer form the "input word matrix." When a one-hot vector is input, it effectively selects a row from this matrix, which *is* the word embedding for the target word.
        3.  **Output Layer**: This layer has $V$ neurons (where $V$ is the vocabulary size). It uses a softmax activation function to output a probability distribution over all words in the vocabulary, indicating the likelihood of each word being a context word for the given target word. The weights connecting the hidden layer to the output layer form the "output word matrix."

6.  **What is Negative Sampling, and why is it used in Word2Vec?**
    *   **Answer**: Negative Sampling is an optimization technique used to speed up Word2Vec training, especially for large vocabularies. The original Skip-gram objective requires calculating the softmax over the entire vocabulary for every training step, which is computationally expensive. Negative Sampling transforms the problem from predicting the exact context word out of $V$ possibilities to a binary classification task. For each (target, actual context) pair (a "positive" sample), it randomly samples a small number of "negative" (non-context) words from the vocabulary. The model then learns to distinguish the positive sample from these negative samples. This significantly reduces the number of weights that need to be updated in each training step, making training much faster.

7.  **What is the role of the window size in Word2Vec? How does it affect the learned embeddings?**
    *   **Answer**: The window size defines the maximum distance between the target word and context words. A smaller window size (e.g., 2-5) tends to capture more syntactic relationships and immediate co-occurrences (e.g., "eat" and "apple"). A larger window size (e.g., 10-15) tends to capture more semantic relationships and broader topical associations (e.g., "doctor" and "hospital"). The choice of window size depends on the specific task and the nature of the text. Smaller windows are often better for tasks requiring fine-grained semantic similarity, while larger windows might be better for document-level understanding.

8.  **How does Word2Vec handle out-of-vocabulary (OOV) words? What are its limitations regarding OOV words?**
    *   **Answer**: Word2Vec cannot generate embeddings for words that were not present in the training corpus. When an OOV word is encountered during inference, it typically either:
        *   Is ignored.
        *   Is mapped to a special `<UNK>` (unknown) token, which has its own learned embedding (if `<UNK>` was part of the training vocabulary).
        *   Is assigned a random vector or a zero vector.
    *   **Limitations**: This is a significant limitation. It means Word2Vec cannot handle new words, typos, or rare words not seen during training, which can lead to information loss or poor performance in real-world applications where text is dynamic.

9.  **What are some limitations of Word2Vec embeddings?**
    *   **Answer**:
        *   **OOV Words**: Cannot handle words not in the training vocabulary.
        *   **Context-Independent**: Each word has a single, fixed embedding, failing to capture polysemy (words with multiple meanings, like "bank").
        *   **Ignores Subword Information**: Treats words as atomic units, missing morphological information (e.g., "run," "running," "ran" are distinct).
        *   **Requires Large Corpora**: Needs substantial text data to learn high-quality embeddings.
        *   **Hyperparameter Sensitivity**: Performance can be sensitive to choices like window size, embedding dimension, and negative samples.

10. **How would you evaluate the quality of Word2Vec embeddings?**
    *   **Answer**:
        *   **Intrinsic Evaluation**:
            *   **Word Similarity Tasks**: Compare the cosine similarity between learned word vectors to human-judged similarity scores (e.g., WordSim-353, SimLex-999 datasets).
            *   **Word Analogy Tasks**: Test if vector arithmetic holds (e.g., "king - man + woman = queen").
        *   **Extrinsic Evaluation**:
            *   **Downstream Task Performance**: Use the embeddings as features in a specific NLP task (e.g., text classification, named entity recognition, sentiment analysis) and measure the task's performance (accuracy, F1-score). This is often considered the most reliable evaluation method as it assesses the practical utility of the embeddings.
            *   **Visualization**: Use dimensionality reduction techniques like t-SNE or PCA to project high-dimensional embeddings into 2D or 3D space and visually inspect if related words cluster together.

## Quiz

1.  What is the primary goal of Word2Vec (Skip-gram)?
    A) To classify text documents into categories.
    B) To translate text from one language to another.
    C) To learn dense vector representations of words that capture semantic relationships.
    D) To perform syntactic parsing of sentences.

2.  In the Skip-gram model, what is the task it tries to accomplish during training?
    A) Predict the target word given its context words.
    B) Predict the context words given a target word.
    C) Predict the next word in a sequence.
    D) Predict the part-of-speech tag for each word.

3.  Which of the following is a significant advantage of Word2Vec embeddings over one-hot encoding?
    A) They are sparse and high-dimensional.
    B) They are computationally less expensive to store.
    C) They capture semantic relationships between words.
    D) They can handle out-of-vocabulary words inherently.

4.  What is the main reason for using Negative Sampling in Word2Vec?
    A) To increase the dimensionality of word vectors.
    B) To make the model more robust to noise in the input data.
    C) To reduce the computational cost of the softmax operation in the output layer.
    D) To allow the model to learn subword information.

5.  A limitation of Word2Vec (Skip-gram) is its inability to handle:
    A) Large text corpora.
    B) Semantic relationships between words.
    C) Out-of-vocabulary words.
    D) Different window sizes.

---

### Answer Key

1.  **C) To learn dense vector representations of words that capture semantic relationships.**
    *   **Explanation**: Word2Vec's core purpose is to transform words into numerical vectors (embeddings) where the geometric relationships between these vectors reflect the semantic relationships between the words.

2.  **B) Predict the context words given a target word.**
    *   **Explanation**: This is the defining characteristic of the Skip-gram architecture. It takes a central word and tries to predict the words that appear around it within a specified window.

3.  **C) They capture semantic relationships between words.**
    *   **Explanation**: One-hot encoding treats each word as an independent entity, providing no information about its meaning or relationship to other words. Word2Vec embeddings, through their training process, learn to place semantically similar words close to each other in the vector space.

4.  **C) To reduce the computational cost of the softmax operation in the output layer.**
    *   **Explanation**: The softmax function requires summing over all words in the vocabulary, which is very slow for large vocabularies. Negative Sampling approximates this by turning it into a binary classification problem with a few negative samples, significantly speeding up training.

5.  **C) Out-of-vocabulary words.**
    *   **Explanation**: Word2Vec learns embeddings only for words present in its training corpus. If a new word appears that was not seen during training, the model cannot generate an embedding for it, making it an out-of-vocabulary (OOV) word.

## Further Reading

1.  **Original Word2Vec Paper**:
    *   Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv preprint arXiv:1301.3781.
    *   [Link to PDF](https://arxiv.org/pdf/1301.3781.pdf) (This is the foundational paper, highly recommended for a deeper dive into the original formulation.)

2.  **Gensim Word2Vec Documentation**:
    *   The official documentation for the `gensim` library's Word2Vec implementation. It provides practical details on parameters, usage, and best practices.
    *   [Link to Gensim Docs](https://radimrehurek.com/gensim/models/word2vec.html)

3.  **"Deep Learning for NLP" by Stanford (CS224N)**:
    *   Lecture notes and videos from Stanford's highly regarded course on Deep Learning for Natural Language Processing. Specifically, lectures on Word2Vec provide excellent conceptual and mathematical explanations.
    *   [Link to CS224N Course Website](http://web.stanford.edu/class/cs224n/) (Look for lectures related to Word2Vec, typically early in the course.)