# Word2Vec (CBOW)

## Overview

Word2Vec is a groundbreaking technique in Natural Language Processing (NLP) developed by Google in 2013. Its primary goal is to learn high-quality, dense vector representations of words, known as "word embeddings," from large text corpora. These embeddings capture semantic and syntactic relationships between words, meaning words with similar meanings or that appear in similar contexts will have similar vector representations in a multi-dimensional space.

CBOW stands for **Continuous Bag-of-Words**. It is one of the two main architectures within the Word2Vec framework (the other being Skip-gram). In essence, CBOW tries to predict a target word based on its surrounding context words. Think of it like filling in the blank: given the words "the quick brown ___ jumps over the lazy dog," CBOW would try to predict "fox." The "bag-of-words" part implies that the order of context words doesn't matter; they are simply averaged or summed to form a single context representation.

The beauty of Word2Vec (CBOW) lies in its simplicity and efficiency. It trains a shallow neural network to perform this prediction task, and as a byproduct of this training, the weights learned by the network become the desired word embeddings. These embeddings are incredibly useful because they transform words from discrete, symbolic tokens into continuous, numerical vectors that machine learning models can easily process, thereby unlocking deeper understanding of language.

## What Problem It Solves

Before Word2Vec, representing words for machine learning models was often done using methods like one-hot encoding or TF-IDF. While these methods have their uses, they suffer from significant limitations:

1.  **Sparsity and High Dimensionality**: One-hot encoding represents each word as a vector where only one dimension is '1' and all others are '0'. For a vocabulary of 100,000 words, each word becomes a 100,000-dimensional vector, which is extremely sparse and computationally expensive.
2.  **Lack of Semantic Meaning**: One-hot vectors treat each word as an independent entity. The vector for "king" has no inherent relationship to the vector for "queen" or "man" or "woman." The dot product between any two distinct one-hot vectors is always zero, implying no similarity, which is semantically incorrect. They don't capture any notion of "relatedness" or "similarity" between words.
3.  **Curse of Dimensionality**: With very high-dimensional data, models often struggle to generalize, requiring vast amounts of data to learn meaningful patterns.
4.  **Inability to Handle Synonyms/Related Words**: If a model is trained on "car," it won't automatically understand "automobile" unless explicitly taught, even though they are synonyms. Traditional methods don't inherently group similar words.

Word2Vec (CBOW) addresses these problems by:

*   **Creating Dense Representations**: Instead of sparse, high-dimensional one-hot vectors, Word2Vec produces dense, lower-dimensional vectors (e.g., 50 to 300 dimensions). This significantly reduces computational overhead.
*   **Capturing Semantic and Syntactic Relationships**: The core innovation is that words appearing in similar contexts tend to have similar meanings. By training a model to predict words from their context, Word2Vec learns to embed words such that their vector representations reflect these relationships. For example, the vector for "king" might be close to "queen," and the vector difference between "king" and "man" might be similar to the difference between "queen" and "woman" (i.e., `vector("king") - vector("man") + vector("woman") ≈ vector("queen")`).
*   **Enabling Transfer Learning**: Once trained on a large corpus, these word embeddings can be used as features in various downstream NLP tasks (like sentiment analysis, machine translation, text classification), often leading to significant performance improvements, even with smaller task-specific datasets.

In essence, Word2Vec (CBOW) provides a way to convert words into a numerical format that not only reduces dimensionality but also encodes rich semantic information, making them much more useful for machine learning algorithms.

## How It Works

The CBOW model works by predicting a target word given its surrounding context words. Let's break down the mechanism step-by-step:

1.  **Data Preparation (Context-Target Pairs)**:
    *   You start with a large corpus of text (e.g., Wikipedia articles, news articles).
    *   For each word in the corpus, you define a "context window" (e.g., 2 words before and 2 words after).
    *   The words within this window become the "context words," and the word in the center becomes the "target word."
    *   Example: Sentence "The quick brown fox jumps over the lazy dog."
        *   If "fox" is the target word, and the window size is 2, the context words are "quick", "brown", "jumps", "over".
        *   This creates a training sample: `(context: ["quick", "brown", "jumps", "over"], target: "fox")`.
    *   The order of context words doesn't matter in CBOW; they are treated as a "bag."

2.  **Model Architecture (Shallow Neural Network)**:
    *   CBOW uses a shallow neural network with three layers:
        *   **Input Layer**: Represents the context words. Each context word is typically represented as a one-hot encoded vector.
        *   **Projection Layer (Hidden Layer)**: This layer averages the word vectors of the context words. It's a linear layer, meaning there's no non-linear activation function applied here. The size of this layer determines the dimensionality of the word embeddings (e.g., 100, 300 dimensions).
        *   **Output Layer**: This layer is a softmax classifier that predicts the probability distribution over all words in the vocabulary, indicating which word is most likely to be the target word.

3.  **Training Process**:

    *   **Step 1: Input Context Words**:
        *   For a given training sample `(context, target)`, each context word is converted into its one-hot vector representation. If your vocabulary has $V$ words, each one-hot vector will be of size $V$.

    *   **Step 2: Input to Projection Layer**:
        *   Each one-hot vector for a context word is multiplied by an "input weight matrix" ($W_{in}$). This matrix has dimensions $V \times N$, where $V$ is the vocabulary size and $N$ is the desired embedding dimension. Each row of $W_{in}$ effectively represents the embedding vector for a word when it acts as a context word.
        *   This multiplication transforms the one-hot vector into an $N$-dimensional word vector.
        *   All the $N$-dimensional word vectors for the context words are then averaged (or summed) to create a single "context vector" ($h$) of size $N$. This averaging step is where the "bag-of-words" concept comes into play.

    *   **Step 3: Projection Layer to Output Layer**:
        *   The context vector ($h$) is then multiplied by an "output weight matrix" ($W_{out}$). This matrix has dimensions $N \times V$. Each column of $W_{out}$ can be thought of as a vector representation of a word when it acts as a target word.
        *   This multiplication results in a vector of size $V$, where each element corresponds to a "score" for each word in the vocabulary.

    *   **Step 4: Softmax Activation**:
        *   A softmax function is applied to these scores to convert them into probabilities. The output is a probability distribution over all words in the vocabulary, indicating the model's prediction for the target word. The sum of these probabilities is 1.

    *   **Step 5: Calculate Loss**:
        *   The predicted probability distribution is compared to the actual one-hot vector of the target word using a loss function, typically **cross-entropy loss**. The goal is to minimize this loss, meaning the model's predicted probability for the actual target word should be as high as possible.

    *   **Step 6: Backpropagation and Weight Update**:
        *   The error (loss) is backpropagated through the network.
        *   Gradient descent (or an optimized variant like Adam or SGD) is used to update the weights in both the input weight matrix ($W_{in}$) and the output weight matrix ($W_{out}$).
        *   These weight matrices are what we are ultimately interested in, as they contain the word embeddings. After training, either $W_{in}$ or $W_{out}$ (or an average of both) can be used as the final word embeddings. Typically, $W_{in}$ is chosen.

This process is repeated for millions or billions of context-target pairs from the corpus. Over time, the model learns to adjust its weights such that words appearing in similar contexts get similar vector representations.

## Mathematical Intuition

Let's formalize the steps involved in CBOW.

Assume:
*   $V$: Size of the vocabulary.
*   $N$: Desired dimension of the word embeddings.
*   $w_t$: The target word.
*   $w_{t-c}, \dots, w_{t-1}, w_{t+1}, \dots, w_{t+c}$: The $2c$ context words, where $c$ is the context window size.
*   $x_i$: One-hot vector for context word $w_i$. It's a $V \times 1$ vector.
*   $y$: One-hot vector for the target word $w_t$. It's a $V \times 1$ vector.

**1. Input Layer to Projection Layer:**

Each context word $w_i$ is represented by a one-hot vector $x_i$.
We have an input weight matrix $W_{in}$ of size $V \times N$. Each row of $W_{in}$ corresponds to a word in the vocabulary and is its $N$-dimensional embedding vector. Let $v_w$ denote the $N$-dimensional vector for word $w$ from $W_{in}$.

For each context word $w_i$, its embedding vector is obtained by:
$$v_{w_i} = W_{in}^T x_i$$
(Note: If $x_i$ is a column vector, $W_{in}^T x_i$ selects the $i$-th row of $W_{in}$. Often, $W_{in}$ is defined such that its rows are the word vectors, so $x_i^T W_{in}$ would select the $i$-th row if $x_i$ is a row vector. For simplicity, let's assume $W_{in}$'s rows are the word vectors, and $x_i$ is a one-hot vector that picks the $i$-th row.)

The projection layer (hidden layer) computes the average of the context word vectors:
$$h = \frac{1}{2c} \sum_{i \in \text{context}} v_{w_i}$$
This $h$ is an $N \times 1$ vector, representing the aggregated context.

**2. Projection Layer to Output Layer:**

We have an output weight matrix $W_{out}$ of size $N \times V$. Each column of $W_{out}$ can be thought of as a "context vector" for a word when it acts as a target. Let $u_w$ denote the $N$-dimensional vector for word $w$ from $W_{out}$ (specifically, the $w$-th column of $W_{out}$).

The score for each word $w_j$ in the vocabulary being the target word, given the context vector $h$, is calculated as:
$$s_j = u_{w_j}^T h$$
This is a dot product between the context vector $h$ and the output vector representation $u_{w_j}$ of word $w_j$.

**3. Softmax Activation:**

To convert these scores into probabilities, we apply the softmax function. The probability of word $w_j$ being the target word is:
$$P(w_j | \text{context}) = \frac{\exp(s_j)}{\sum_{k=1}^{V} \exp(s_k)}$$
This gives us a probability distribution over all words in the vocabulary.

**4. Loss Function:**

The goal is to maximize the probability of the actual target word $w_t$ given its context. This is equivalent to minimizing the negative log-likelihood (cross-entropy loss). If $y_t$ is the one-hot vector for the true target word $w_t$, and $P(w_j | \text{context})$ is the predicted probability for word $w_j$, the loss for a single training example is:
$$L = - \log P(w_t | \text{context})$$
More generally, using the one-hot vector $y_t$:
$$L = - \sum_{j=1}^{V} y_{t,j} \log P(w_j | \text{context})$$
where $y_{t,j}$ is 1 if $j=t$ and 0 otherwise.

**5. Learning Word Embeddings:**

The training process involves using gradient descent (or its variants) to update the matrices $W_{in}$ and $W_{out}$ to minimize this loss function over the entire training corpus.
The gradients are computed with respect to $W_{in}$ and $W_{out}$, and the weights are adjusted iteratively.

After training, the rows of the $W_{in}$ matrix (or sometimes $W_{out}$, or an average of both) are taken as the final word embeddings. These $N$-dimensional vectors capture the semantic and syntactic properties of words based on their contexts.

The key intuition is that by forcing the model to predict the center word from its surrounding words, the model learns to assign similar vectors to words that appear in similar contexts. The "hidden layer" (projection layer) effectively becomes a lookup table for these word vectors.

## Advantages

*   **Efficiency**: CBOW is computationally efficient, especially when dealing with large datasets. Its shallow architecture and simple operations (averaging, matrix multiplications) make it faster to train compared to more complex neural networks.
*   **Captures Semantic Relationships**: It effectively learns dense word embeddings that capture semantic and syntactic similarities between words. Words with similar meanings or that appear in similar contexts will have similar vector representations.
*   **Good for Frequent Words**: CBOW tends to perform better than Skip-gram for more frequent words, as it averages multiple context words, providing a more stable signal for prediction.
*   **Reduced Dimensionality**: It transforms high-dimensional, sparse one-hot vectors into lower-dimensional, dense vectors, which are more manageable and efficient for downstream tasks.
*   **Transfer Learning**: Pre-trained CBOW embeddings can be used as features in various NLP tasks, often leading to significant performance improvements, especially when task-specific data is limited.

## Disadvantages

*   **Less Effective for Rare Words**: Because CBOW averages the context words, rare words might not get enough distinct context signals to learn robust embeddings. Skip-gram often performs better with rare words as it predicts context from a single target word.
*   **Fixed Vocabulary**: Word2Vec models are trained on a fixed vocabulary. If a new word (an "out-of-vocabulary" or OOV word) appears that wasn't in the training corpus, the model cannot generate an embedding for it. This requires special handling (e.g., assigning a random vector, using a special OOV token, or retraining).
*   **Ignores Word Order within Context**: The "bag-of-words" assumption means that the order of words within the context window is disregarded. While often effective, this can sometimes lead to a loss of nuanced meaning where word order is crucial (e.g., "dog bites man" vs. "man bites dog").
*   **Context Window Size**: The choice of context window size is a hyperparameter that can significantly impact the quality of embeddings. A small window might capture more syntactic relationships, while a larger window might capture more semantic relationships. Finding the optimal size can require experimentation.
*   **Computational Cost for Very Large Vocabularies**: While efficient, the softmax layer in the output still requires computing probabilities over the entire vocabulary, which can be slow for extremely large vocabularies. Techniques like Negative Sampling or Hierarchical Softmax are used to mitigate this.

## Real World Applications

Word2Vec (CBOW) embeddings have become a fundamental building block in many NLP systems due to their ability to represent words meaningfully.

1.  **Recommendation Systems**: By understanding the semantic similarity between items (e.g., movies, products, articles) based on their descriptions or user reviews, Word2Vec can power recommendation engines. For instance, if a user likes a movie whose description contains words like "sci-fi" and "adventure," the system can recommend other movies whose descriptions contain similar word embeddings.
2.  **Sentiment Analysis and Text Classification**: Word embeddings provide rich features for classifying text. Instead of using sparse features, the dense, semantically meaningful vectors of words in a document can be averaged or fed into a neural network to determine sentiment (positive, negative, neutral), topic, or category. This significantly improves the performance of models on tasks like spam detection, news categorization, or customer review analysis.
3.  **Machine Translation**: Word embeddings can help bridge the gap between languages. By learning embeddings for words in different languages that map to a common vector space, machine translation systems can better understand the semantic equivalence of words and phrases, leading to more accurate translations.
4.  **Information Retrieval and Search Engines**: Word2Vec can enhance search capabilities. Instead of just matching keywords, search engines can use word embeddings to understand the semantic intent of a query. If a user searches for "car," the engine can also retrieve documents containing "automobile," "vehicle," or "sedan" because their embeddings are close in the vector space, leading to more relevant search results.
5.  **Question Answering Systems**: In QA systems, Word2Vec can help in understanding the relationship between words in a question and words in potential answers. By comparing the embeddings of question terms with document terms, the system can identify passages or sentences that are semantically similar to the question, even if they don't share exact keywords.

## Python Example

We'll use the `gensim` library, which provides an efficient and user-friendly implementation of Word2Vec.

```python
import gensim
from gensim.models import Word2Vec
import numpy as np

# 1. Prepare a dummy dataset (list of sentences)
# In a real scenario, this would be a large text corpus.
sentences = [
    "the quick brown fox jumps over the lazy dog",
    "i love to eat apples and bananas",
    "the dog barks loudly at the cat",
    "cats are often lazy but sometimes playful",
    "i enjoy eating fruits like apples and oranges",
    "the fox is a wild animal",
    "dogs are loyal companions"
]

# 2. Preprocessing: Tokenize the sentences
# Gensim's Word2Vec model expects a list of lists of words.
tokenized_sentences = [sentence.split() for sentence in sentences]

print("Tokenized Sentences:")
for s in tokenized_sentences:
    print(s)
print("-" * 30)

# 3. Train the Word2Vec (CBOW) model
# vector_size: Dimension of the word embeddings (e.g., 100, 300)
# window: The maximum distance between the current and predicted word within a sentence.
# min_count: Ignores all words with total frequency lower than this.
# sg: Training algorithm: 0 for CBOW, 1 for Skip-gram. We use 0 for CBOW.
# epochs: Number of iterations (epochs) over the corpus.
model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=100,  # Embedding dimension
    window=5,         # Context window size
    min_count=1,      # Include all words for this small example
    sg=0,             # CBOW model
    epochs=100        # Number of training iterations
)

print(f"Model trained with CBOW (sg={model.sg})")
print(f"Vocabulary size: {len(model.wv.index_to_key)}")
print("-" * 30)

# 4. Explore the trained embeddings

# Get the vector for a specific word
word_vector_dog = model.wv['dog']
print(f"Vector for 'dog' (first 10 dimensions): {word_vector_dog[:10]}")
print(f"Vector dimension: {len(word_vector_dog)}")
print("-" * 30)

# Find most similar words
print("Words most similar to 'dog':")
similar_to_dog = model.wv.most_similar('dog', topn=3)
for word, similarity in similar_to_dog:
    print(f"  {word}: {similarity:.4f}")
print("-" * 30)

print("Words most similar to 'apples':")
similar_to_apples = model.wv.most_similar('apples', topn=3)
for word, similarity in similar_to_apples:
    print(f"  {word}: {similarity:.4f}")
print("-" * 30)

# Perform word analogies (King - Man + Woman = Queen)
# Note: With a small corpus, analogies might not be perfect,
# but it demonstrates the capability.
print("Word analogy: 'fox' - 'animal' + 'dog' (should be something like 'pet' or 'companion'):")
try:
    analogy_result = model.wv.most_similar(positive=['fox', 'dog'], negative=['animal'], topn=1)
    for word, similarity in analogy_result:
        print(f"  {word}: {similarity:.4f}")
except KeyError as e:
    print(f"Could not perform analogy: {e}. Ensure all words are in vocabulary.")
print("-" * 30)

# Check if a word is in the vocabulary
print(f"'cat' in vocabulary: {'cat' in model.wv}")
print(f"'elephant' in vocabulary: {'elephant' in model.wv}")
print("-" * 30)

# Save and Load the model (optional, but good practice)
model.save("word2vec_cbow_model.bin")
print("Model saved as word2vec_cbow_model.bin")

loaded_model = Word2Vec.load("word2vec_cbow_model.bin")
print(f"Loaded model vocabulary size: {len(loaded_model.wv.index_to_key)}")
print("Words most similar to 'cat' using loaded model:")
similar_to_cat_loaded = loaded_model.wv.most_similar('cat', topn=2)
for word, similarity in similar_to_cat_loaded:
    print(f"  {word}: {similarity:.4f}")
```

**Explanation of the Code:**

1.  **Dummy Dataset**: We create a small list of sentences. In a real application, this would be a much larger corpus (e.g., millions of sentences from Wikipedia, news articles, etc.).
2.  **Tokenization**: `gensim`'s `Word2Vec` model expects its input as a list of lists, where each inner list represents a sentence and contains individual words (tokens). We achieve this by splitting each sentence string by spaces.
3.  **Model Training**:
    *   `Word2Vec(...)`: This is the constructor for the Word2Vec model.
    *   `sentences=tokenized_sentences`: Our preprocessed input data.
    *   `vector_size=100`: We choose 100 dimensions for our word embeddings. Common choices range from 50 to 300.
    *   `window=5`: This means the model considers 5 words before and 5 words after the target word as its context.
    *   `min_count=1`: Words that appear less than `min_count` times are ignored. For this tiny example, we set it to 1 to include all words. For larger corpora, a higher `min_count` (e.g., 5 or 10) helps filter out rare words and noise.
    *   `sg=0`: This is the crucial parameter that specifies the training algorithm. `sg=0` means **CBOW (Continuous Bag-of-Words)**. `sg=1` would be Skip-gram.
    *   `epochs=100`: The number of times the model iterates over the entire corpus during training. More epochs can lead to better embeddings but also increase training time.
4.  **Exploring Embeddings**:
    *   `model.wv['word']`: Accesses the vector for a specific word. `wv` stands for "word vectors."
    *   `model.wv.most_similar('word', topn=N)`: Finds the `N` words whose embeddings are closest (most similar) to the given word's embedding in the vector space. Similarity is typically measured using cosine similarity.
    *   `model.wv.most_similar(positive=['word1', 'word2'], negative=['word3'])`: This allows for word analogies. It tries to find a word that is to `word1` as `word3` is to `word2` (e.g., `vector(word1) - vector(word3) + vector(word2)`).
5.  **Saving/Loading**: It's good practice to save your trained model so you don't have to retrain it every time. `model.save()` and `Word2Vec.load()` handle this.

Even with this small dataset, you'll observe that words like 'dog' and 'cat' or 'apples' and 'oranges' show some level of similarity, demonstrating the core principle of Word2Vec.

## Interview Questions

1.  **What is Word2Vec, and what problem does it solve in NLP?**
    *   **Answer**: Word2Vec is a group of shallow neural network models designed to generate word embeddings (dense vector representations of words). It solves the problem of representing words in a way that captures their semantic and syntactic relationships, overcoming the limitations of sparse representations like one-hot encoding which treat words as independent entities and don't encode meaning or similarity.

2.  **Explain the core idea behind the Continuous Bag-of-Words (CBOW) model.**
    *   **Answer**: The core idea of CBOW is to predict a target word based on its surrounding context words. It takes the context words within a fixed window around a target word, averages their vector representations, and then uses this averaged context vector to predict the most probable target word. The "bag-of-words" implies that the order of context words does not matter.

3.  **How does CBOW differ from Skip-gram, the other Word2Vec architecture?**
    *   **Answer**: CBOW predicts the target word from its context words, while Skip-gram does the opposite: it predicts the context words from a single target word. CBOW is generally faster to train and performs better for frequent words, while Skip-gram is better at handling rare words and can capture more nuanced semantic relationships.

4.  **Describe the architecture of the CBOW model. What are its main layers?**
    *   **Answer**: CBOW uses a shallow neural network with three layers:
        1.  **Input Layer**: Receives one-hot encoded vectors of the context words.
        2.  **Projection Layer (Hidden Layer)**: Averages the word vectors of the context words. This layer has no activation function and its size determines the embedding dimension.
        3.  **Output Layer**: A softmax layer that outputs a probability distribution over all words in the vocabulary, indicating the likelihood of each word being the target word.

5.  **What is the role of the "weight matrices" in Word2Vec (CBOW) training?**
    *   **Answer**: The weight matrices are what we learn during training, and they *are* the word embeddings. Specifically, the input-to-hidden weight matrix (often denoted $W_{in}$) contains the word vectors for words when they act as context words. Each row of this matrix is an $N$-dimensional embedding for a word. The hidden-to-output weight matrix ($W_{out}$) contains word vectors for words when they act as target words. After training, typically $W_{in}$ (or sometimes $W_{out}$ or an average of both) is used as the final set of word embeddings.

6.  **What is the loss function typically used in CBOW, and why?**
    *   **Answer**: The cross-entropy loss function is typically used. It measures the difference between the predicted probability distribution (from the softmax output) and the true probability distribution (a one-hot vector for the actual target word). Minimizing cross-entropy loss is equivalent to maximizing the likelihood of predicting the correct target word given its context.

7.  **How does CBOW handle out-of-vocabulary (OOV) words?**
    *   **Answer**: CBOW, like other traditional Word2Vec models, cannot inherently handle OOV words. Its vocabulary is fixed during training. If a word not present in the training corpus appears, the model has no pre-computed vector for it. Common strategies include:
        *   Ignoring OOV words.
        *   Mapping all OOV words to a special `<UNK>` (unknown) token and learning a single embedding for it.
        *   Using subword models (like FastText) which can construct embeddings for OOV words from their character n-grams.

8.  **What are the main advantages of using CBOW over traditional methods like one-hot encoding?**
    *   **Answer**: CBOW produces dense, lower-dimensional word embeddings that capture semantic and syntactic relationships between words. This overcomes the sparsity, high dimensionality, and lack of semantic meaning inherent in one-hot encoding, leading to better performance in many NLP tasks.

9.  **What are some limitations or disadvantages of the CBOW model?**
    *   **Answer**:
        *   Less effective for rare words compared to Skip-gram.
        *   Cannot handle out-of-vocabulary (OOV) words.
        *   Ignores word order within the context window (bag-of-words assumption).
        *   The choice of context window size is a hyperparameter that can impact performance.
        *   Computational cost of softmax can be high for very large vocabularies (though mitigated by techniques like Negative Sampling).

10. **How do you typically use pre-trained Word2Vec (CBOW) embeddings in a downstream NLP task?**
    *   **Answer**: Pre-trained embeddings are often used in two main ways:
        1.  **Feature Extraction**: The embeddings for words in a document are extracted and then averaged, summed, or fed into another neural network layer (e.g., a convolutional or recurrent layer) as input features for tasks like text classification, sentiment analysis, or named entity recognition.
        2.  **Embedding Layer Initialization**: In deep learning models, the embedding layer (which maps integer word IDs to vectors) can be initialized with the pre-trained Word2Vec embeddings. This provides a strong starting point for the model, especially when training data is limited. The embeddings can then either be kept static or fine-tuned during the model's training.

## Quiz

1.  What is the primary goal of Word2Vec (CBOW)?
    A) To classify text into categories.
    B) To translate text from one language to another.
    C) To learn dense, meaningful vector representations of words.
    D) To perform grammatical parsing of sentences.

2.  In the CBOW model, what does the "context" refer to?
    A) The entire document in which a word appears.
    B) The words immediately surrounding a target word within a defined window.
    C) The grammatical structure of a sentence.
    D) The overall topic of a paragraph.

3.  Which of the following best describes the input to the CBOW model's neural network?
    A) A single one-hot encoded vector of the target word.
    B) A sequence of character n-grams for the target word.
    C) One-hot encoded vectors of the context words.
    D) TF-IDF scores for all words in the vocabulary.

4.  What is a significant advantage of Word2Vec (CBOW) embeddings over one-hot encoding?
    A) They are always higher dimensional.
    B) They are sparse and computationally cheaper.
    C) They capture semantic relationships between words.
    D) They automatically handle out-of-vocabulary words.

5.  If you set `sg=0` when training a `gensim.models.Word2Vec` model, which algorithm are you using?
    A) Skip-gram
    B) Continuous Bag-of-Words (CBOW)
    C) FastText
    D) GloVe

---

### Answer Key

1.  **C) To learn dense, meaningful vector representations of words.**
    *   **Explanation**: The fundamental purpose of Word2Vec (both CBOW and Skip-gram) is to create numerical word embeddings that capture semantic and syntactic properties, making words understandable to machine learning models.

2.  **B) The words immediately surrounding a target word within a defined window.**
    *   **Explanation**: In CBOW, the context is defined by a sliding window around a central target word. These surrounding words are used to predict the target.

3.  **C) One-hot encoded vectors of the context words.**
    *   **Explanation**: CBOW takes the one-hot encoded representations of the context words as input, which are then projected into a lower-dimensional space and averaged.

4.  **C) They capture semantic relationships between words.**
    *   **Explanation**: Unlike one-hot encoding, which treats words as independent, CBOW embeddings are designed to place words with similar meanings or contexts closer together in the vector space, thus capturing semantic relationships.

5.  **B) Continuous Bag-of-Words (CBOW)**
    *   **Explanation**: In the `gensim` library's `Word2Vec` implementation, the `sg` parameter controls the algorithm: `sg=0` for CBOW and `sg=1` for Skip-gram.

## Further Reading

1.  **Original Word2Vec Paper**:
    *   **Title**: "Efficient Estimation of Word Representations in Vector Space"
    *   **Authors**: Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean
    *   **Link**: [https://arxiv.org/pdf/1301.3781.pdf](https://arxiv.org/pdf/1301.3781.pdf)
    *   **Note**: This is the foundational paper. While technical, it provides the original insights and details of the Word2Vec architectures.

2.  **Gensim Word2Vec Documentation**:
    *   **Link**: [https://radimrehurek.com/gensim/models/word2vec.html](https://radimrehurek.com/gensim/models/word2vec.html)
    *   **Note**: The official documentation for the `gensim` library's Word2Vec implementation. It's an excellent resource for understanding the practical usage, parameters, and capabilities of the model in Python.

3.  **"Neural Network Methods for Natural Language Processing" by Yoav Goldberg (Chapter 3: Word Embeddings)**:
    *   **Link**: [https://www.cs.bgu.ac.il/~yoavg/teaching/nn4nlp16/](https://www.cs.bgu.ac.il/~yoavg/teaching/nn4nlp16/) (Look for the book/lecture notes)
    *   **Note**: This book provides a clear and accessible explanation of word embeddings, including Word2Vec, from a neural network perspective. It offers good mathematical intuition without being overly dense. Chapter 3 specifically covers word embeddings in detail.