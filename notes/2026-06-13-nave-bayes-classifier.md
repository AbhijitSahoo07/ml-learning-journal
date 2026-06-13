# Naïve Bayes Classifier

## Overview
The Naïve Bayes Classifier is a simple yet powerful probabilistic machine learning algorithm primarily used for classification tasks. It's based on Bayes' Theorem with an assumption of independence among predictors (features). This "naïve" assumption is where it gets its name, as it simplifies the calculations significantly, even if it's rarely true in real-world data. Despite this simplification, Naïve Bayes often performs surprisingly well, especially in areas like text classification and spam detection. It's a generative model, meaning it learns the joint probability distribution of the input data and the target variable.

Imagine you want to classify an email as "spam" or "not spam". A Naïve Bayes classifier would look at the words in the email and, based on its training, calculate the probability that an email containing those specific words belongs to the "spam" class versus the "not spam" class. The email is then assigned to the class with the highest probability.

## What Problem It Solves
The Naïve Bayes Classifier is designed to solve **classification problems**, where the goal is to assign a given data point to one of several predefined categories or classes. Specifically, it excels at:

1.  **Categorical Prediction**: When you have a dataset and want to predict a categorical outcome (e.g., "yes/no", "spam/not spam", "positive/negative sentiment", "disease A/disease B/no disease").
2.  **High-Dimensional Data**: It performs well even with a large number of features (dimensions), making it suitable for tasks like text classification where each word can be a feature.
3.  **Probabilistic Classification**: It not only predicts a class but also provides the probability of a data point belonging to each class, which can be useful for understanding the model's confidence.
4.  **Handling Noise and Irrelevant Features**: Due to its probabilistic nature and the independence assumption, it can sometimes be robust to noisy data and irrelevant features, as they don't heavily influence the probabilities of other features.
5.  **Computational Efficiency**: It's very fast to train and predict, making it a good choice for large datasets or real-time applications where speed is critical.

It's needed in machine learning because it offers a straightforward, interpretable, and computationally efficient baseline for classification tasks, especially when dealing with text or other forms of discrete data where the "naïve" independence assumption might not be a severe handicap.

## How It Works
The Naïve Bayes Classifier works by applying Bayes' Theorem with a strong (naïve) independence assumption between the features. Here's a step-by-step breakdown:

1.  **Training Phase (Learning from Data):**
    *   **Calculate Prior Probabilities:** For each class, the algorithm calculates its prior probability. This is simply the frequency of that class in the training dataset. For example, if 30% of emails in the training data are spam, then $P(\text{Spam}) = 0.3$.
    *   **Calculate Likelihoods:** For each feature and each class, the algorithm calculates the likelihood. This is the probability of a specific feature value occurring, given that the data point belongs to a particular class. For example, $P(\text{word 'discount' present} | \text{Spam})$ would be the probability that the word "discount" appears in an email, given that the email is spam. This is calculated by counting how many spam emails contain "discount" and dividing by the total number of spam emails.
    *   **Handle Different Feature Types:**
        *   **Categorical Features:** For discrete or categorical features (like "color: red", "size: large"), likelihoods are calculated by counting occurrences.
        *   **Continuous Features:** For continuous features (like "height", "temperature"), a common approach is to assume they follow a specific probability distribution, most often a Gaussian (normal) distribution. The algorithm then estimates the mean and variance of the feature for each class.

2.  **Prediction Phase (Classifying New Data):**
    *   When a new data point (e.g., a new email) arrives, the algorithm needs to predict its class. It does this by calculating the **posterior probability** for each possible class.
    *   **Apply Bayes' Theorem:** For each class, it uses the prior probabilities and likelihoods learned during training to compute the probability that the new data point belongs to that class, given its observed features.
    *   **The "Naïve" Assumption:** This is the crucial part. Instead of calculating the joint probability of all features given the class (which would be complex), Naïve Bayes assumes that all features are conditionally independent of each other given the class. This means:
        $P(\text{feature}_1, \text{feature}_2, \dots, \text{feature}_n | \text{Class}) = P(\text{feature}_1 | \text{Class}) \times P(\text{feature}_2 | \text{Class}) \times \dots \times P(\text{feature}_n | \text{Class})$
    *   **Select the Best Class:** After calculating the posterior probability for each class, the algorithm assigns the new data point to the class that has the highest posterior probability. This is often called the "Maximum A Posteriori" (MAP) decision rule.

In essence, Naïve Bayes "learns" the statistical relationships between features and classes from the training data and then uses these relationships to make educated guesses about the class of new, unseen data.

## Mathematical Intuition
The Naïve Bayes Classifier is built upon **Bayes' Theorem**, which describes the probability of an event, based on prior knowledge of conditions that might be related to the event.

Bayes' Theorem states:
$$P(A|B) = \frac{P(B|A)P(A)}{P(B)}$$

Where:
*   $P(A|B)$ is the **posterior probability**: the probability of event $A$ occurring given that event $B$ has occurred. This is what we want to find in classification (e.g., probability of an email being spam given its words).
*   $P(B|A)$ is the **likelihood**: the probability of event $B$ occurring given that event $A$ has occurred. (e.g., probability of seeing certain words given the email is spam).
*   $P(A)$ is the **prior probability**: the probability of event $A$ occurring independently of $B$. (e.g., overall probability of any email being spam).
*   $P(B)$ is the **evidence**: the probability of event $B$ occurring independently of $A$. (e.g., overall probability of seeing those words in any email).

Now, let's adapt this for classification. We want to find the probability of a class $C_k$ (e.g., "spam", "not spam") given a set of features $X = (x_1, x_2, \dots, x_n)$ (e.g., words in an email).

So, Bayes' Theorem becomes:
$$P(C_k | X) = \frac{P(X | C_k)P(C_k)}{P(X)}$$

Here:
*   $P(C_k | X)$ is the **posterior probability**: the probability that a data point belongs to class $C_k$ given its features $X$. This is what we want to maximize to make a prediction.
*   $P(X | C_k)$ is the **likelihood**: the probability of observing features $X$ given that the data point belongs to class $C_k$.
*   $P(C_k)$ is the **prior probability**: the probability of class $C_k$ occurring in the dataset.
*   $P(X)$ is the **evidence**: the probability of observing features $X$ (this term is constant for all classes, so we can ignore it when comparing probabilities between classes).

Since $P(X)$ is constant for all classes, we are essentially interested in finding the class $C_k$ that maximizes the numerator:
$$\text{predict}(C_k) = \underset{C_k}{\operatorname{argmax}} \ P(X | C_k)P(C_k)$$

Now, here comes the "naïve" assumption. It assumes that all features $x_i$ are conditionally independent of each other given the class $C_k$. This means:
$$P(X | C_k) = P(x_1, x_2, \dots, x_n | C_k) = P(x_1 | C_k) \times P(x_2 | C_k) \times \dots \times P(x_n | C_k)$$

Substituting this back into our prediction formula, we get the final Naïve Bayes classification rule:
$$\text{predict}(C_k) = \underset{C_k}{\operatorname{argmax}} \ P(C_k) \prod_{i=1}^{n} P(x_i | C_k)$$

Let's break down the terms for a beginner:

1.  **$P(C_k)$ (Prior Probability of Class $C_k$)**:
    *   This is simply the proportion of training examples that belong to class $C_k$.
    *   Calculated as: $\frac{\text{Number of training examples in class } C_k}{\text{Total number of training examples}}$.

2.  **$P(x_i | C_k)$ (Likelihood of feature $x_i$ given Class $C_k$)**:
    *   This is the probability of observing a specific value for feature $x_i$, given that the data point is already known to be in class $C_k$.
    *   **For Categorical Features**:
        *   Calculated as: $\frac{\text{Number of training examples in class } C_k \text{ with feature } x_i \text{ value}}{\text{Total number of training examples in class } C_k}$.
        *   To avoid the "zero-frequency problem" (where a feature value not seen in training for a class would make the entire product zero), **Laplace Smoothing** (or additive smoothing) is often applied:
            $$P(x_i | C_k) = \frac{\text{Count}(x_i, C_k) + \alpha}{\text{Count}(C_k) + \alpha \times \text{Number of possible values for } x_i}$$
            where $\alpha$ is typically 1.
    *   **For Continuous Features (e.g., Gaussian Naïve Bayes)**:
        *   It's assumed that the continuous values for each feature $x_i$ are distributed according to a Gaussian (normal) distribution within each class $C_k$.
        *   The likelihood $P(x_i | C_k)$ is then calculated using the probability density function (PDF) of the Gaussian distribution:
            $$P(x_i | C_k) = \frac{1}{\sqrt{2\pi\sigma_{k,i}^2}} \exp\left(-\frac{(x_i - \mu_{k,i})^2}{2\sigma_{k,i}^2}\right)$$
            where $\mu_{k,i}$ is the mean of feature $x_i$ for class $C_k$, and $\sigma_{k,i}^2$ is the variance of feature $x_i$ for class $C_k$. These mean and variance values are estimated from the training data.

By calculating these probabilities for each class and multiplying them together, the Naïve Bayes classifier determines which class is most probable for a given set of features.

## Advantages
*   **Simplicity and Ease of Implementation**: It's a straightforward algorithm to understand and implement.
*   **Fast Training and Prediction**: Due to its simple probabilistic calculations, it's very efficient computationally, making it suitable for large datasets and real-time predictions.
*   **Good Performance with High-Dimensional Data**: It performs surprisingly well with a large number of features, especially in text classification tasks where the number of words (features) can be enormous.
*   **Requires Less Training Data**: It can perform reasonably well even with a relatively small amount of training data compared to more complex models.
*   **Handles Both Continuous and Discrete Data**: Different variants (Gaussian, Multinomial, Bernoulli) allow it to work with various data types.
*   **Provides Probabilistic Predictions**: It outputs the probability of a data point belonging to each class, which can be useful for decision-making and understanding model confidence.
*   **Robust to Irrelevant Features**: If a feature is truly independent of the class, it won't significantly impact the overall probability calculation.

## Disadvantages
*   **The "Naïve" Independence Assumption**: This is its biggest limitation. The assumption that all features are conditionally independent given the class is rarely true in real-world data (e.g., in text, words are often correlated). If features are highly correlated, the model's performance can degrade.
*   **Zero-Frequency Problem**: If a categorical feature value (or a word in text classification) is not observed in the training data for a particular class, its likelihood $P(x_i | C_k)$ will be zero. This will cause the entire posterior probability for that class to become zero, regardless of other strong evidence. This is typically mitigated using smoothing techniques like Laplace smoothing.
*   **Sensitivity to Feature Scaling (for Gaussian NB)**: While not directly sensitive to scaling in the same way distance-based algorithms are, the assumption of Gaussian distribution for continuous features means that the estimated mean and variance are sensitive to the scale of the data.
*   **Poor Estimator of Probabilities**: While it's a good classifier (predicts the correct class), the actual probability values it outputs might not be well-calibrated. For example, it might say there's a 99% chance of spam, but the true probability might be closer to 80%.
*   **Cannot Learn Interactions Between Features**: Because of the independence assumption, it cannot capture complex relationships or interactions between different features.

## Real World Applications
1.  **Spam Filtering**: One of the most classic and effective applications. Naïve Bayes classifiers are widely used to identify and filter out spam emails by analyzing the words and phrases within the email content. For example, words like "free," "money," "viagra," or specific sender addresses can be strong indicators of spam.
2.  **Sentiment Analysis**: Used to determine the sentiment (positive, negative, neutral) of a piece of text, such as product reviews, social media posts, or customer feedback. By analyzing the presence of certain words or phrases, the classifier can infer the emotional tone.
3.  **Document Classification/Categorization**: Assigning documents (e.g., news articles, research papers, legal documents) to predefined categories or topics. For instance, classifying news articles into "sports," "politics," "technology," etc., based on their content.
4.  **Medical Diagnosis**: In some medical applications, Naïve Bayes can be used to predict the likelihood of a patient having a certain disease based on their symptoms, medical history, and test results. The "naïve" assumption might be a limitation here, but it can serve as a quick initial screening tool.
5.  **Recommendation Systems**: While more complex models are often used, Naïve Bayes can form a basic component of recommendation engines. For example, it can predict whether a user will like a certain item (movie, product) based on their past preferences and the features of the item.

## Python Example
This example demonstrates how to use `GaussianNB` from `scikit-learn` for a simple classification task. We'll generate a synthetic dataset, train the model, make predictions, and evaluate its performance.

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Generate a dummy dataset
# We'll create a dataset with 2 features and 2 classes for easy visualization.
X, y = make_classification(n_samples=300, n_features=2, n_informative=2,
                           n_redundant=0, n_clusters_per_class=1, random_state=42)

print(f"Shape of features (X): {X.shape}")
print(f"Shape of target (y): {y.shape}")
print(f"First 5 samples of X:\n{X[:5]}")
print(f"First 5 samples of y: {y[:5]}\n")

# Visualize the dataset
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=y, palette='viridis', s=100, alpha=0.7)
plt.title('Generated Dataset for Classification')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 2. Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"Training set size: {len(X_train)} samples")
print(f"Testing set size: {len(X_test)} samples\n")

# 3. Initialize the Naïve Bayes Classifier (Gaussian Naïve Bayes for continuous features)
# GaussianNB assumes that the likelihood of the features is Gaussian.
model = GaussianNB()

# 4. Train the model using the training data
print("Training the Naïve Bayes model...")
model.fit(X_train, y_train)
print("Model training complete.\n")

# 5. Make predictions on the test data
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test) # Get probability estimates

print(f"First 10 actual labels (y_test):     {y_test[:10]}")
print(f"First 10 predicted labels (y_pred): {y_pred[:10]}")
print(f"First 5 predicted probabilities (y_pred_proba):\n{y_pred_proba[:5]}\n")

# 6. Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")
print("\nClassification Report:\n", report)

# Optional: Visualize the decision boundary (for 2 features)
def plot_decision_boundary(X, y, model, title):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.8, cmap='viridis')
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=y, palette='viridis', s=100, alpha=0.7, edgecolor='k')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

plot_decision_boundary(X_test, y_test, model, 'Naïve Bayes Decision Boundary on Test Data')
```

**Explanation of the Code:**

1.  **Generate Data**: `make_classification` creates a synthetic binary classification dataset with 300 samples and 2 features. This makes it easy to visualize.
2.  **Split Data**: `train_test_split` divides the dataset into training and testing sets. The model learns from the training set and is evaluated on the unseen test set.
3.  **Initialize Model**: `GaussianNB()` is instantiated. This specific variant of Naïve Bayes assumes that the continuous features follow a Gaussian (normal) distribution within each class.
4.  **Train Model**: `model.fit(X_train, y_train)` trains the Naïve Bayes classifier. During this step, the model calculates the prior probabilities for each class and the mean and variance of each feature for each class (to estimate the likelihoods based on the Gaussian assumption).
5.  **Make Predictions**:
    *   `model.predict(X_test)` generates the predicted class labels for the test set.
    *   `model.predict_proba(X_test)` outputs the probability of each sample belonging to each class.
6.  **Evaluate Model**:
    *   `accuracy_score` calculates the proportion of correctly classified samples.
    *   `classification_report` provides a more detailed breakdown of precision, recall, and F1-score for each class.
7.  **Visualize Decision Boundary (Optional)**: For 2D data, this function helps visualize how the Naïve Bayes model separates the classes. The colored regions represent the areas where the model would predict a certain class.

## Interview Questions

1.  **What is the core idea behind the Naïve Bayes Classifier?**
    *   **Answer:** Naïve Bayes is a probabilistic classification algorithm based on Bayes' Theorem. Its core idea is to calculate the probability of a data point belonging to each class given its features, and then assign it to the class with the highest probability. It does this by learning the prior probabilities of classes and the likelihood of features given each class from the training data.

2.  **What does the "naïve" in Naïve Bayes refer to?**
    *   **Answer:** The "naïve" refers to the strong assumption that all features are conditionally independent of each other given the class. This means that the presence or absence of one feature does not affect the presence or absence of any other feature, assuming the class is known. Mathematically, $P(x_1, x_2, \dots, x_n | C_k) = P(x_1 | C_k) \times P(x_2 | C_k) \times \dots \times P(x_n | C_k)$.

3.  **Explain Bayes' Theorem and how it's applied in Naïve Bayes.**
    *   **Answer:** Bayes' Theorem states $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$. In Naïve Bayes, we want to find $P(\text{Class} | \text{Features})$. So, it becomes $P(\text{Class} | \text{Features}) = \frac{P(\text{Features} | \text{Class})P(\text{Class})}{P(\text{Features})}$. The classifier calculates this posterior probability for each class and predicts the class with the highest value. The "naïve" assumption simplifies $P(\text{Features} | \text{Class})$ into a product of individual feature likelihoods.

4.  **What are the main types of Naïve Bayes classifiers and when would you use each?**
    *   **Answer:**
        *   **Gaussian Naïve Bayes:** Used when features are continuous and assumed to follow a Gaussian (normal) distribution within each class. It estimates the mean and variance for each feature per class.
        *   **Multinomial Naïve Bayes:** Suitable for discrete features representing counts, such as word counts in text classification. It's commonly used for document classification.
        *   **Bernoulli Naïve Bayes:** Designed for binary/boolean features (e.g., presence or absence of a word). It explicitly models the absence of a feature, unlike Multinomial NB.

5.  **What is the "zero-frequency problem" in Naïve Bayes and how is it typically handled?**
    *   **Answer:** The zero-frequency problem occurs when a particular feature value (e.g., a word) is not present in the training data for a specific class. If this happens, the likelihood $P(\text{feature value} | \text{class})$ becomes zero. Since the Naïve Bayes formula multiplies all likelihoods, this zero term will cause the entire posterior probability for that class to become zero, regardless of other strong evidence. This is typically handled using **Laplace smoothing** (or additive smoothing), where a small constant (e.g., 1) is added to all counts, ensuring no probability becomes exactly zero.

6.  **List some advantages of using Naïve Bayes.**
    *   **Answer:** It's simple and easy to implement, computationally efficient (fast training and prediction), performs well with high-dimensional data (like text), requires less training data than some other models, and provides probabilistic predictions. It's also robust to irrelevant features.

7.  **List some disadvantages of using Naïve Bayes.**
    *   **Answer:** The primary disadvantage is the "naïve" independence assumption, which is rarely true in real-world data and can lead to suboptimal performance if features are highly correlated. It also suffers from the zero-frequency problem (though mitigated by smoothing) and can be a poor estimator of actual probabilities, even if it's a good classifier. It cannot capture complex feature interactions.

8.  **Is Naïve Bayes a generative or discriminative model? Explain the difference.**
    *   **Answer:** Naïve Bayes is a **generative model**.
        *   **Generative models** learn the joint probability distribution $P(X, Y)$ (features and labels) or $P(X|Y)$ and $P(Y)$. They model how the data is generated within each class. Naïve Bayes explicitly models $P(X|C_k)$ (likelihood) and $P(C_k)$ (prior).
        *   **Discriminative models** directly learn the decision boundary between classes or the conditional probability $P(Y|X)$ without modeling the distribution of the features. Examples include Logistic Regression and Support Vector Machines.

9.  **How does Naïve Bayes handle numerical features?**
    *   **Answer:** For numerical features, Naïve Bayes typically assumes a specific probability distribution for the feature values within each class. The most common assumption is the **Gaussian (Normal) distribution**. For each class, the model estimates the mean and variance of the numerical feature from the training data. Then, for a new data point, the likelihood $P(x_i | C_k)$ is calculated using the probability density function (PDF) of the estimated Gaussian distribution.

10. **When would you choose Naïve Bayes over more complex models like SVMs or Neural Networks?**
    *   **Answer:** You might choose Naïve Bayes when:
        *   You need a very fast and computationally efficient model for large datasets or real-time applications.
        *   The "naïve" independence assumption holds reasonably well, or its impact is not severe (e.g., text classification where many words are somewhat independent).
        *   You have limited training data.
        *   Interpretability is important, as its probabilistic nature can be easier to understand.
        *   You need a strong baseline model to compare against more complex algorithms.
        *   The features are predominantly categorical or count-based.

## Quiz

1.  Which of the following is the core assumption of the Naïve Bayes classifier?
    A) Features are linearly separable.
    B) Features are conditionally independent given the class.
    C) Features follow a uniform distribution.
    D) Features are highly correlated.

2.  In the Naïve Bayes formula, $P(C_k | X) = \frac{P(X | C_k)P(C_k)}{P(X)}$, what does $P(C_k)$ represent?
    A) The likelihood of features given the class.
    B) The posterior probability of the class.
    C) The prior probability of the class.
    D) The evidence.

3.  What problem does Laplace smoothing primarily address in Naïve Bayes?
    A) Overfitting to the training data.
    B) Underfitting due to too few features.
    C) The zero-frequency problem, where unseen feature values lead to zero probabilities.
    D) Slow training times for large datasets.

4.  Which type of Naïve Bayes classifier is most suitable for text classification where features are word counts?
    A) Gaussian Naïve Bayes
    B) Bernoulli Naïve Bayes
    C) Multinomial Naïve Bayes
    D) Complement Naïve Bayes

5.  Which of the following is a significant advantage of Naïve Bayes?
    A) It can model complex interactions between features.
    B) It is highly accurate even when the independence assumption is severely violated.
    C) It is computationally efficient and performs well with high-dimensional data.
    D) It is robust to outliers and noisy data without any special handling.

### Answer Key

1.  **B) Features are conditionally independent given the class.**
    *   **Explanation:** This is the defining "naïve" assumption that simplifies the calculation of the likelihood term $P(X | C_k)$.

2.  **C) The prior probability of the class.**
    *   **Explanation:** $P(C_k)$ represents the overall probability of observing class $C_k$ in the dataset, before considering any specific features.

3.  **C) The zero-frequency problem, where unseen feature values lead to zero probabilities.**
    *   **Explanation:** Laplace smoothing adds a small constant to counts, preventing any likelihood from becoming zero and thus avoiding the entire posterior probability for a class from becoming zero.

4.  **C) Multinomial Naïve Bayes**
    *   **Explanation:** Multinomial Naïve Bayes is specifically designed for discrete features that represent counts, making it ideal for text classification where features are typically word counts or frequencies.

5.  **C) It is computationally efficient and performs well with high-dimensional data.**
    *   **Explanation:** Naïve Bayes is known for its speed and ability to handle many features, making it a good choice for tasks like text classification. Options A and B are generally false, and D is not a primary advantage without specific modifications.

## Further Reading

1.  **Scikit-learn Documentation - Naïve Bayes**: The official documentation provides a clear overview of different Naïve Bayes models available in scikit-learn, their parameters, and usage examples.
    *   [https://scikit-learn.org/stable/modules/naive_bayes.html](https://scikit-learn.org/stable/modules/naive_bayes.html)

2.  **Stanford CS229 Lecture Notes - Generative Learning Algorithms (Naïve Bayes)**: A more theoretical and in-depth look at Naïve Bayes as a generative learning algorithm, including its mathematical derivation.
    *   [http://cs229.stanford.edu/notes2020fall/cs229-notes1.pdf](http://cs229.stanford.edu/notes2020fall/cs229-notes1.pdf) (Refer to Section 3.1: Naive Bayes)

3.  **"Pattern Recognition and Machine Learning" by Christopher Bishop**: Chapter 4 (Linear Models for Classification) and Chapter 8 (Graphical Models) provide excellent context and detailed mathematical treatment of probabilistic classifiers, including Naïve Bayes. This is a classic textbook for a deeper understanding.
    *   (Available in most university libraries or online through academic subscriptions)