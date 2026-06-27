# Contextual Embeddings

## Overview
Imagine the word "bank." What does it mean? It could be the financial institution where you keep your money, or it could be the side of a river. The meaning depends entirely on the surrounding words, or the "context."

Traditional word embeddings, like Word2Vec or GloVe, assign a single, fixed vector (a list of numbers) to each word in a vocabulary. This means "bank" would have the same vector regardless of whether it appears in "I went to the **bank** to deposit money" or "The boat docked at the river **bank**." This approach fails to capture the rich, nuanced meanings words can have in different contexts.

**Contextual Embeddings** are a revolutionary advancement in Natural Language Processing (NLP) that solve this problem. Instead of assigning a fixed vector to each word, contextual embedding models generate a word's vector representation dynamically, taking into account the entire sentence or document it appears in. This means the word "bank" will have a different vector when used in a financial context compared to when it's used in a geographical context. These embeddings are powerful because they capture polysemy (words with multiple meanings), synonymy, and other semantic relationships that depend on the surrounding text.

## What Problem It Solves
Contextual Embeddings primarily address the limitations of **static word embeddings**. Let's break down the core problems:

1.  **Polysemy (Words with Multiple Meanings):** As discussed with "bank," many words have different meanings depending on their context. Static embeddings assign one vector per word, failing to distinguish between these meanings. This leads to a loss of semantic precision. For example, "apple" could refer to the fruit or the tech company. A static embedding would average these meanings into a single vector, making it less useful for tasks that require fine-grained understanding.

2.  **Lack of Contextual Nuance:** Language is inherently contextual. The meaning of a word is not just its dictionary definition but also how it interacts with other words in a sentence. Static embeddings treat words in isolation, ignoring syntactic roles (e.g., subject, object) and semantic relationships (e.g., who did what to whom). This makes it difficult for downstream NLP models to truly understand the sentence's meaning.

3.  **Fixed Representations:** Static embeddings are pre-computed and fixed. If a new meaning for a word emerges, or if a word is used in a novel way, the static embedding cannot adapt. Contextual embeddings, being dynamic, can potentially capture these evolving meanings.

4.  **Limited Expressiveness:** For tasks like machine translation, question answering, or sentiment analysis, a deep understanding of the sentence's meaning is crucial. Static embeddings provide a good starting point but often lack the expressiveness needed to capture complex linguistic phenomena like sarcasm, negation, or subtle emotional tones, which are heavily context-dependent.

By generating embeddings that are sensitive to the surrounding words, contextual embeddings provide a much richer and more accurate representation of language, significantly boosting the performance of various NLP tasks.

## How It Works
The magic of contextual embeddings lies in using sophisticated neural network architectures, most notably the **Transformer architecture** (which powers models like BERT, GPT, and RoBERTa) or recurrent neural networks (like in ELMo). While the specifics vary between models, the general principle is to process an entire sequence of words simultaneously to generate context-aware representations.

Here's a simplified, step-by-step breakdown of how it generally works:

1.  **Input Tokenization:**
    *   First, the input text (e.g., "The boat docked at the river bank.") is broken down into smaller units called **tokens**. These tokens can be words, sub-word units (like "un-", "##ing"), or even individual characters.
    *   Special tokens are often added: `[CLS]` at the beginning (for classification tasks) and `[SEP]` between sentences or at the end.

2.  **Initial Embeddings (Static + Positional):**
    *   Each token is initially converted into a basic, static vector representation. This is similar to traditional word embeddings but serves as a starting point.
    *   Crucially, **positional embeddings** are added to these initial token embeddings. Since models like Transformers process words in parallel without inherent sequential understanding, positional embeddings provide information about the order of words in the sentence. This tells the model where each word is located.

3.  **Processing through Neural Network Layers (e.g., Transformers):**
    *   The combined initial (token + positional) embeddings are then fed into multiple layers of a deep neural network.
    *   **Self-Attention (Key Mechanism):** This is the core innovation. In each layer, for every word in the sentence, the model calculates how much attention it should pay to every other word in the *same* sentence.
        *   For example, when processing the word "bank" in "The boat docked at the river bank," the self-attention mechanism might learn that "river" is highly relevant to understanding "bank" in this context, while "boat" and "docked" are also important.
        *   This mechanism allows information to flow between all words in the sequence, enabling each word's representation to be influenced by its entire context.
    *   **Feed-Forward Networks:** After attention, the output for each word passes through a standard feed-forward neural network, which further transforms the representation.
    *   **Layer Normalization and Residual Connections:** These techniques help stabilize training and allow for deeper networks.

4.  **Generating Contextual Embeddings:**
    *   After passing through many such layers (e.g., 12 layers in BERT-base, 24 in BERT-large), the final output for each token is its **contextual embedding**.
    *   This final vector for "bank" will be distinctly different when the input sentence is "I went to the **bank** to deposit money" versus "The boat docked at the river **bank**," because the self-attention mechanism learned different relationships and dependencies in each sentence.

5.  **Downstream Tasks:**
    *   These rich contextual embeddings can then be used as input features for various NLP tasks like text classification, named entity recognition, question answering, and more, often leading to significant performance improvements.

In essence, contextual embedding models learn a complex function that maps an input sequence of words to a sequence of vectors, where each vector is a sophisticated summary of its corresponding word's meaning *within that specific context*.

## Mathematical Intuition

At its heart, contextual embeddings aim to represent a word $w_i$ in a sequence $S = (w_1, w_2, \dots, w_n)$ not as a fixed vector, but as a function of the entire sequence.
Mathematically, for a given word $w_i$ at position $i$ in a sentence $S$, its contextual embedding $E_i$ is generated by a function $f$:
$$E_i = f(w_i, S)$$
This means $E_i$ depends not only on $w_i$ itself but also on all other words $w_j$ in the sequence $S$.

Let's delve a bit into the intuition behind the **Self-Attention mechanism**, which is central to Transformer-based contextual embedding models (like BERT).

For each token $w_i$ in the input sequence, we first obtain an initial embedding $x_i$. This $x_i$ is typically a sum of a token embedding and a positional embedding.
Then, for each token $w_i$, the self-attention mechanism computes three different vectors:
1.  **Query (Q) vector:** $q_i = x_i W^Q$
2.  **Key (K) vector:** $k_i = x_i W^K$
3.  **Value (V) vector:** $v_i = x_i W^V$
where $W^Q, W^K, W^V$ are learnable weight matrices. These matrices transform the initial embedding into different "perspectives" for comparison.

The core idea is to calculate an "attention score" between each query vector $q_i$ and all key vectors $k_j$ in the sequence. This score indicates how much attention word $i$ should pay to word $j$.
The attention score $a_{ij}$ between word $i$ and word $j$ is typically computed as a dot product, scaled by the square root of the dimension of the key vectors, $d_k$:
$$a_{ij} = \frac{q_i \cdot k_j}{\sqrt{d_k}}$$
These scores are then normalized using a softmax function to get attention weights $\alpha_{ij}$:
$$\alpha_{ij} = \frac{\exp(a_{ij})}{\sum_{k=1}^{n} \exp(a_{ik})}$$
These $\alpha_{ij}$ values represent the probability distribution of how much word $i$ "attends" to word $j$. Notice that $\sum_{j=1}^{n} \alpha_{ij} = 1$.

Finally, the output representation for word $i$, let's call it $z_i$, is a weighted sum of all the value vectors $v_j$ in the sequence, where the weights are the attention weights $\alpha_{ij}$:
$$z_i = \sum_{j=1}^{n} \alpha_{ij} v_j$$
This $z_i$ is the context-aware representation for word $w_i$ *after one attention head in one layer*.
The key insight here is that $z_i$ is not just a transformation of $x_i$; it's a blend of *all* $v_j$ vectors, weighted by how relevant each $w_j$ is to $w_i$ (as determined by $\alpha_{ij}$). This is how information from the entire context flows into the representation of each individual word.

Modern Transformer models use **Multi-Head Attention**, where this process is repeated multiple times in parallel with different $W^Q, W^K, W^V$ matrices, and the results are concatenated and linearly transformed. This allows the model to attend to different parts of the sequence and different types of relationships simultaneously.

After multiple layers of such self-attention and feed-forward networks, the final output vector for $w_i$ is its rich, contextual embedding $E_i$. This $E_i$ encapsulates not just the meaning of $w_i$ but also its semantic and syntactic role within the given sentence.

## Advantages

*   **Handles Polysemy and Contextual Nuance:** The most significant advantage is the ability to generate different embeddings for the same word based on its surrounding context, effectively resolving ambiguities and capturing subtle semantic differences.
*   **Richer Semantic Representations:** Contextual embeddings capture deeper linguistic properties, including syntax, semantics, and even pragmatic information, leading to a more comprehensive understanding of text.
*   **Improved Performance on Downstream Tasks:** Models using contextual embeddings as input features consistently achieve state-of-the-art results across a wide range of NLP tasks, such as sentiment analysis, named entity recognition, machine translation, question answering, and text summarization.
*   **Transfer Learning Powerhouse:** Pre-trained contextual embedding models (like BERT, GPT) can be fine-tuned on specific downstream tasks with relatively small amounts of task-specific data, significantly reducing the need for massive labeled datasets and training time from scratch.
*   **Captures Long-Range Dependencies:** Architectures like Transformers, with their self-attention mechanism, are particularly good at capturing dependencies between words that are far apart in a sentence or document, which was a challenge for earlier RNN-based models.
*   **Reduced Feature Engineering:** By providing high-quality, task-agnostic representations, contextual embeddings minimize the need for manual feature engineering, simplifying the NLP pipeline.

## Disadvantages

*   **High Computational Cost:** Training these large models (e.g., BERT, GPT-3) requires immense computational resources (GPUs/TPUs) and time, making them inaccessible for many researchers and organizations to train from scratch.
*   **Large Model Size:** Pre-trained contextual embedding models are often very large, with millions or even billions of parameters. This makes them memory-intensive and slow for inference on resource-constrained devices.
*   **Complexity:** The internal workings of these deep neural networks, especially the multi-head attention mechanisms, can be complex and difficult to interpret, making it challenging to understand *why* a particular embedding was generated.
*   **Data Hunger:** While fine-tuning requires less data, the initial pre-training phase demands vast amounts of unlabeled text data (billions of words) to learn robust representations.
*   **Environmental Impact:** The energy consumption associated with training and running these massive models contributes to a significant carbon footprint.
*   **Bias Amplification:** If the pre-training data contains societal biases (e.g., gender stereotypes, racial biases), the contextual embeddings will likely learn and amplify these biases, potentially leading to unfair or discriminatory outcomes in downstream applications.
*   **Latency for Real-time Applications:** Due to their size and complexity, generating contextual embeddings can introduce latency, which might be an issue for real-time NLP applications.

## Real World Applications

Contextual embeddings have revolutionized many areas of NLP, leading to significant improvements in various real-world applications:

1.  **Search Engines and Information Retrieval:**
    *   **Application:** Enhancing search relevance and understanding user queries.
    *   **How it works:** When a user types a query, contextual embeddings can capture the nuanced meaning of the query, even if it uses synonyms or rephrased terms. Similarly, documents are embedded contextually. The search engine can then match the query embedding to document embeddings more accurately than keyword matching, leading to more relevant search results. For example, a query like "best place to save money" can be understood to mean "bank" in a financial sense, leading to relevant financial institution results.

2.  **Question Answering Systems:**
    *   **Application:** Powering chatbots, virtual assistants, and knowledge base search.
    *   **How it works:** In systems like Google's BERT-powered search or customer service chatbots, contextual embeddings help the model understand the intent and specific entities in a user's question. It can then scan a large body of text (e.g., Wikipedia, product manuals) to find the most relevant sentence or passage that answers the question, even if the exact words aren't present. The model can identify the answer span within a document based on the contextual similarity between the question and parts of the document.

3.  **Machine Translation:**
    *   **Application:** Improving the quality and fluency of translated text.
    *   **How it works:** Contextual embeddings provide a much richer representation of source language sentences, allowing translation models to better grasp the meaning and nuances before translating. This helps in resolving ambiguities (e.g., translating "bank" correctly based on context) and producing more natural-sounding translations that preserve the original meaning and style.

4.  **Sentiment Analysis and Emotion Detection:**
    *   **Application:** Analyzing customer reviews, social media posts, and feedback for business intelligence.
    *   **How it works:** Contextual embeddings can capture the subtle emotional tones and sentiment expressed in text. For instance, they can differentiate between "This movie was *bad* in a good way" (sarcasm/positive) and "This movie was *bad*" (negative) by understanding the interplay of words. This leads to more accurate sentiment classification, helping businesses understand public opinion or customer satisfaction.

5.  **Named Entity Recognition (NER):**
    *   **Application:** Extracting specific entities like names, organizations, locations, and dates from unstructured text.
    *   **How it works:** By understanding the context, contextual embeddings help models accurately identify and classify entities. For example, in "Apple released a new iPhone," "Apple" is recognized as an organization. In "I ate an apple," "apple" is a fruit. The contextual embedding for "Apple" would be different in each case, enabling the NER model to make the correct classification.

## Python Example

This example will use the `transformers` library from Hugging Face to demonstrate how contextual embeddings differ for the same word ("bank") in different contexts. We'll use a pre-trained `DistilBERT` model, which is a smaller, faster version of BERT.

First, ensure you have the library installed:
`pip install transformers torch`

```python
import torch
from transformers import DistilBertTokenizer, DistilBertModel
from scipy.spatial.distance import cosine

# 1. Load pre-trained tokenizer and model
# DistilBERT is a smaller, faster, and lighter version of BERT.
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# 2. Define sentences with the target word in different contexts
sentence1 = "I went to the bank to deposit money."
sentence2 = "The boat docked at the river bank."
sentence3 = "The financial institution is called a bank." # Another financial context

# 3. Tokenize sentences and get input IDs
# return_tensors='pt' ensures PyTorch tensors are returned
inputs1 = tokenizer(sentence1, return_tensors='pt', add_special_tokens=True)
inputs2 = tokenizer(sentence2, return_tensors='pt', add_special_tokens=True)
inputs3 = tokenizer(sentence3, return_tensors='pt', add_special_tokens=True)

# 4. Get model outputs (embeddings)
# model(**inputs) returns a tuple, the first element is the last_hidden_state (embeddings)
with torch.no_grad(): # Disable gradient calculation for inference
    outputs1 = model(**inputs1)
    outputs2 = model(**inputs2)
    outputs3 = model(**inputs3)

# The last_hidden_state contains the contextual embeddings for each token
# Shape: (batch_size, sequence_length, hidden_size)
embeddings1 = outputs1.last_hidden_state
embeddings2 = outputs2.last_hidden_state
embeddings3 = outputs3.last_hidden_state

# 5. Extract the embedding for the target word "bank"
# We need to find the index of "bank" in each tokenized sentence.
# Note: tokenizer.tokenize() gives the raw tokens, inputs['input_ids'] gives their IDs.
# We'll use the tokenized list to find the index.

# Helper function to get the embedding for a specific word
def get_word_embedding(word, tokenized_inputs, embeddings):
    # Get the actual tokens (list of strings)
    tokens = tokenizer.convert_ids_to_tokens(tokenized_inputs['input_ids'][0])
    
    # Find the index of the word. Handle subword tokenization if necessary.
    # For 'bank', it's usually a single token.
    try:
        word_index = tokens.index(word)
    except ValueError:
        print(f"Warning: '{word}' not found as a single token in {tokens}. Trying subword search.")
        # If 'bank' is split, this simple approach won't work perfectly.
        # For simplicity, we assume 'bank' is a single token here.
        return None
    
    # Return the embedding for that specific token
    # [0] for batch_size, [word_index] for token position
    return embeddings[0, word_index, :]

# Get embeddings for "bank" in each context
bank_embedding_s1 = get_word_embedding("bank", inputs1, embeddings1)
bank_embedding_s2 = get_word_embedding("bank", inputs2, embeddings2)
bank_embedding_s3 = get_word_embedding("bank", inputs3, embeddings3)

if bank_embedding_s1 is not None and bank_embedding_s2 is not None and bank_embedding_s3 is not None:
    print(f"Embedding dimension: {bank_embedding_s1.shape[0]}")

    # 6. Calculate cosine similarity between the embeddings
    # Cosine similarity measures the cosine of the angle between two vectors.
    # A value close to 1 means high similarity, close to 0 means low similarity.

    # Similarity between "bank" (financial) and "bank" (river)
    similarity_financial_river = 1 - cosine(bank_embedding_s1.cpu().numpy(), bank_embedding_s2.cpu().numpy())
    print(f"\nCosine similarity between 'bank' (financial, S1) and 'bank' (river, S2): {similarity_financial_river:.4f}")

    # Similarity between "bank" (financial) and "bank" (another financial)
    similarity_financial_financial = 1 - cosine(bank_embedding_s1.cpu().numpy(), bank_embedding_s3.cpu().numpy())
    print(f"Cosine similarity between 'bank' (financial, S1) and 'bank' (financial, S3): {similarity_financial_financial:.4f}")

    # Similarity between "bank" (river) and "bank" (financial)
    similarity_river_financial = 1 - cosine(bank_embedding_s2.cpu().numpy(), bank_embedding_s3.cpu().numpy())
    print(f"Cosine similarity between 'bank' (river, S2) and 'bank' (financial, S3): {similarity_river_financial:.4f}")

    print("\n--- Expected Output Interpretation ---")
    print("The similarity between 'bank' in two financial contexts (S1 vs S3) should be significantly higher")
    print("than the similarity between 'bank' in a financial context (S1 or S3) and 'bank' in a river context (S2).")
    print("This demonstrates that contextual embeddings capture the different meanings of the word 'bank'.")
else:
    print("Could not retrieve all word embeddings. Please check tokenization logic.")

```

**Explanation of the Output:**

When you run this code, you will observe that:
*   The cosine similarity between `bank_embedding_s1` (financial) and `bank_embedding_s3` (financial) will be relatively high (e.g., > 0.8 or 0.9). This indicates that the model recognizes these two instances of "bank" as having similar meanings because they share a similar financial context.
*   The cosine similarity between `bank_embedding_s1` (financial) and `bank_embedding_s2` (river) will be significantly lower (e.g., < 0.6 or 0.7). This demonstrates that the model assigns very different vector representations to "bank" when it appears in a financial context versus a geographical context, effectively capturing the polysemy of the word.

This simple example clearly illustrates the core advantage of contextual embeddings: their ability to generate dynamic, context-dependent representations for words.

## Interview Questions

1.  **What are contextual embeddings, and how do they differ from static word embeddings like Word2Vec or GloVe?**
    *   **Answer:** Contextual embeddings are vector representations of words that change based on the surrounding words in a sentence or document. Unlike static embeddings (Word2Vec, GloVe), which assign a single, fixed vector to each word regardless of its context, contextual embeddings generate a dynamic vector that captures the specific meaning and role of a word in a given instance. This allows them to handle polysemy (words with multiple meanings) and capture nuanced semantic relationships.

2.  **Why are contextual embeddings necessary in NLP? What problem do they solve?**
    *   **Answer:** They are necessary to overcome the limitations of static embeddings, primarily the inability to handle polysemy and contextual nuance. Words often have different meanings depending on their context (e.g., "bank" as a financial institution vs. a river bank). Static embeddings fail to differentiate these meanings, leading to less accurate language understanding. Contextual embeddings solve this by providing context-aware representations, leading to a much richer and more precise understanding of text.

3.  **Name some popular models that generate contextual embeddings.**
    *   **Answer:** Popular models include ELMo (Embeddings from Language Models), BERT (Bidirectional Encoder Representations from Transformers), GPT (Generative Pre-trained Transformer) series (GPT-2, GPT-3, GPT-4), RoBERTa, XLNet, ALBERT, T5, and ELECTRA.

4.  **Briefly explain the core mechanism that allows models like BERT to create contextual embeddings.**
    *   **Answer:** The core mechanism is the **Transformer architecture**, specifically the **Self-Attention mechanism**. Self-attention allows each word in a sequence to attend to every other word in the same sequence. By calculating attention weights, the model determines how much influence each surrounding word has on the representation of the current word. This enables information to flow across the entire sequence, allowing the final embedding of a word to be a rich blend of its own meaning and the meanings of its context.

5.  **How do positional embeddings contribute to contextual embedding models?**
    *   **Answer:** Positional embeddings are crucial because Transformer models process words in parallel, meaning they don't inherently understand the order of words. Positional embeddings are added to the initial word embeddings to inject information about the absolute or relative position of each word in the sequence. This allows the model to differentiate between "dog bites man" and "man bites dog," which would otherwise have the same set of words but different meanings due to word order.

6.  **What are the main advantages of using contextual embeddings in NLP tasks?**
    *   **Answer:** Key advantages include:
        *   Better handling of polysemy and contextual nuance.
        *   Richer semantic representations of words and sentences.
        *   Significant performance improvements across a wide range of NLP tasks (e.g., QA, NER, sentiment analysis).
        *   Enabling powerful transfer learning, where pre-trained models can be fine-tuned on specific tasks with less data.
        *   Ability to capture long-range dependencies in text.

7.  **What are some disadvantages or challenges associated with contextual embeddings?**
    *   **Answer:** Disadvantages include:
        *   High computational cost for training and inference due to large model sizes.
        *   Large memory footprint, making deployment on edge devices challenging.
        *   Complexity and difficulty in interpreting the internal workings.
        *   Requirement for vast amounts of pre-training data.
        *   Potential to amplify biases present in the training data.
        *   Increased latency for real-time applications.

8.  **Explain the concept of "transfer learning" in the context of contextual embeddings.**
    *   **Answer:** Transfer learning with contextual embeddings involves two main stages:
        1.  **Pre-training:** A large language model (e.g., BERT) is trained on a massive corpus of unlabeled text data using self-supervised tasks (like masked language modeling or next sentence prediction) to learn general language understanding and generate contextual embeddings.
        2.  **Fine-tuning:** The pre-trained model (or just its embedding layer) is then adapted to a specific downstream NLP task (e.g., sentiment analysis) by adding a small task-specific output layer and training it on a relatively smaller labeled dataset for that task. The knowledge gained during pre-training is "transferred," allowing the model to achieve high performance with less task-specific data.

9.  **How would you use a pre-trained contextual embedding model (like BERT) for a text classification task?**
    *   **Answer:** You would typically use it in a fine-tuning approach:
        1.  Load a pre-trained BERT model and its tokenizer.
        2.  Tokenize your text classification dataset, ensuring it's in the format expected by BERT (e.g., adding `[CLS]` and `[SEP]` tokens).
        3.  Add a classification head (e.g., a linear layer) on top of the BERT model. This layer will take the contextual embedding of the `[CLS]` token (which typically aggregates sentence-level information) as input.
        4.  Train the entire model (BERT layers + classification head) on your labeled text classification dataset. The BERT layers will be fine-tuned to generate embeddings optimized for your specific task, and the classification head will learn to map these embeddings to your target classes.

10. **Can contextual embeddings help with out-of-vocabulary (OOV) words?**
    *   **Answer:** Yes, to some extent, especially with models that use **subword tokenization** (like WordPiece or BPE). Instead of treating entire words as tokens, these tokenizers break down rare or unknown words into smaller, known subword units (e.g., "unbelievable" might become "un", "##believe", "##able"). Since the model learns embeddings for these subword units, it can construct a meaningful representation for an OOV word by combining the embeddings of its constituent subwords, even if it hasn't seen the full word before. This is a significant improvement over static word embeddings, which typically assign a generic "unknown" token embedding to OOV words.

## Quiz

1.  What is the primary advantage of contextual embeddings over static word embeddings?
    A) They are faster to train.
    B) They use less memory.
    C) They can represent different meanings of a word based on its context.
    D) They only work with numerical data.

2.  Which of the following models is known for generating contextual embeddings?
    A) Word2Vec
    B) GloVe
    C) BERT
    D) FastText

3.  The core mechanism that allows Transformer-based models to create context-aware representations is:
    A) Convolutional Neural Networks (CNNs)
    B) Recurrent Neural Networks (RNNs)
    C) Self-Attention
    D) Principal Component Analysis (PCA)

4.  If the word "apple" appears in "Apple released a new iPhone" and "I ate an apple," how would a contextual embedding model likely represent it?
    A) With the exact same vector in both sentences.
    B) With two distinctly different vectors, reflecting the different meanings.
    C) With a single vector that averages the meanings of fruit and company.
    D) It would only be able to process one meaning per model.

5.  Which of these is a significant disadvantage of using large contextual embedding models?
    A) They cannot be used for transfer learning.
    B) They are typically very small and easy to deploy on mobile devices.
    C) They require substantial computational resources for training and inference.
    D) They only work for English language tasks.

### Answer Key

1.  **C) They can represent different meanings of a word based on its context.**
    *   **Explanation:** This is the defining characteristic and primary advantage of contextual embeddings, allowing them to handle polysemy and capture nuanced meanings.

2.  **C) BERT**
    *   **Explanation:** Word2Vec, GloVe, and FastText are all examples of models that generate static word embeddings. BERT is a prominent example of a model that generates contextual embeddings using the Transformer architecture.

3.  **C) Self-Attention**
    *   **Explanation:** Self-attention is the fundamental mechanism within the Transformer architecture that enables words to interact with and influence the representations of all other words in a sequence, thereby creating context-aware embeddings.

4.  **B) With two distinctly different vectors, reflecting the different meanings.**
    *   **Explanation:** The ability to differentiate between the meanings of "apple" (company vs. fruit) based on context is precisely what contextual embeddings are designed to do.

5.  **C) They require substantial computational resources for training and inference.**
    *   **Explanation:** Large contextual embedding models are computationally intensive, requiring powerful hardware (GPUs/TPUs) and significant time for both training and generating embeddings during inference.

## Further Reading

1.  **Attention Is All You Need (Transformer Paper):**
    *   **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
    *   **Description:** The seminal paper that introduced the Transformer architecture and the self-attention mechanism, which forms the backbone of most modern contextual embedding models like BERT and GPT. While mathematically dense, understanding its core ideas is crucial.

2.  **BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding:**
    *   **Link:** [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
    *   **Description:** The original paper introducing BERT, a highly influential contextual embedding model. It details the architecture, pre-training tasks (Masked Language Model, Next Sentence Prediction), and its impact on various NLP benchmarks.

3.  **Hugging Face Transformers Documentation:**
    *   **Link:** [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index)
    *   **Description:** An excellent practical resource for working with contextual embedding models. It provides comprehensive documentation, tutorials, and examples for using pre-trained models like BERT, GPT, RoBERTa, etc., for various NLP tasks in Python.