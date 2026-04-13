"""
College Data Science Generator
Covers: Data Handling & Processing, Data Visualization,
        Machine Learning, Deep Learning, Tools & Best Practices
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=13):
    return ('Computer Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_data_handling(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is data cleaning?",
         "The process of fixing or removing incorrect, duplicate, or incomplete data",
         ["Deleting a database", "Sorting data alphabetically",
          "Adding more data to a dataset"],
         "Data cleaning ensures quality: handle missing values, fix types, remove duplicates.", 'easy', 13),
        ("What is 'missing data imputation'?",
         "Filling in missing values using statistical methods (mean, median, model-based)",
         ["Deleting rows with missing values", "Ignoring missing values",
          "Replacing all values with zeros"],
         "Common imputation: mean/median fill, forward fill (time series), model-based (KNN, MICE).", 'medium', 14),
        ("What is the difference between structured and unstructured data?",
         "Structured has predefined schema (tables); unstructured has no fixed format (text, images)",
         ["Structured data is larger", "Unstructured data is always numerical",
          "They are the same in machine learning contexts"],
         "Structured: SQL databases, CSV. Unstructured: emails, social media, video, audio.", 'easy', 13),
        ("What is feature engineering?",
         "Creating or transforming features to improve model performance",
         ["Selecting a machine learning algorithm",
          "Collecting new data",
          "Evaluating model accuracy"],
         "Feature engineering: creating interaction terms, log transforms, binning, encoding categoricals.", 'medium', 14),
        ("What is one-hot encoding?",
         "Converting categorical variables into binary indicator columns",
         ["Normalizing numerical features",
          "Encoding data with a cipher",
          "Converting text to numbers by rank"],
         "One-hot encoding: 'Color={Red,Blue,Green}' → 3 binary columns (is_Red, is_Blue, is_Green).", 'medium', 13),
        ("What is the curse of dimensionality?",
         "As dimensions increase, data becomes sparse and distances lose meaning",
         ["Having too few features", "High-dimensional data is always easier to work with",
          "The difficulty of visualizing 3D data"],
         "High-dimensional spaces require exponentially more data; distances become uninformative.", 'hard', 15),
        ("What is data normalization/standardization?",
         "Scaling features to a common range to prevent any feature from dominating",
         ["Converting all values to integers",
          "Removing outliers",
          "Sorting data in ascending order"],
         "Min-max scaling → [0,1]. Z-score standardization → mean=0, std=1.", 'medium', 13),
        ("What is a train-test split?",
         "Dividing data into training and testing sets to evaluate model generalization",
         ["Splitting data by date", "Dividing data by type",
          "Creating two copies of the dataset"],
         "Test set (held out) evaluates how well a model generalizes to unseen data.", 'easy', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Data Handling', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_machine_learning(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the difference between supervised and unsupervised learning?",
         "Supervised uses labeled data; unsupervised finds patterns in unlabeled data",
         ["Supervised is slower", "Unsupervised uses labeled data",
          "They are the same approach"],
         "Supervised: classification, regression. Unsupervised: clustering, dimensionality reduction.", 'easy', 13),
        ("What is overfitting?",
         "When a model learns the training data too well, including noise, and performs poorly on new data",
         ["When a model is too simple", "When a model has too few parameters",
          "When training accuracy is low"],
         "Overfitting: high training accuracy, low test accuracy. Fixed by regularization, more data, simpler model.", 'medium', 13),
        ("What is cross-validation?",
         "Evaluating a model by training and testing on multiple data splits",
         ["Validating data quality", "Testing a model on the training data",
          "Comparing two different models"],
         "k-fold CV: split data into k folds, train on k-1, test on 1, repeat k times, average results.", 'medium', 14),
        ("What is regularization in machine learning?",
         "Adding a penalty for model complexity to reduce overfitting",
         ["Normalizing the training data", "Removing outliers",
          "Increasing the learning rate"],
         "L1 (Lasso) adds |w| penalty → sparsity. L2 (Ridge) adds w² → shrinks weights.", 'hard', 14),
        ("What is a decision tree?",
         "A tree-structured model making decisions based on feature thresholds",
         ["A neural network", "A type of clustering algorithm",
          "A linear regression model"],
         "Decision trees split data recursively; interpretable but prone to overfitting.", 'easy', 13),
        ("What is a random forest?",
         "An ensemble of decision trees trained on random subsets of data and features",
         ["A single deep decision tree", "A type of neural network",
          "A model for time series data only"],
         "Random forests reduce overfitting via bagging and feature randomness. Generally more accurate than single trees.", 'medium', 14),
        ("What is gradient descent?",
         "An optimization algorithm that iteratively adjusts parameters to minimize loss",
         ["A method for cleaning data",
          "An algorithm for sorting data",
          "A technique for feature selection"],
         "Gradient descent: θ = θ − α∇J(θ). Learning rate α controls step size.", 'medium', 14),
        ("What is the bias-variance tradeoff?",
         "High bias (underfitting) vs high variance (overfitting) — finding the right model complexity",
         ["The tradeoff between accuracy and speed",
          "The tradeoff between features and samples",
          "The relationship between training and test loss"],
         "Simple models have high bias. Complex models have high variance. Optimal = low total error.", 'hard', 14),
        ("What is k-means clustering?",
         "An algorithm that partitions data into k clusters by minimizing within-cluster variance",
         ["A supervised classification algorithm",
          "An algorithm for regression",
          "A type of neural network layer"],
         "k-means: assign points to nearest centroid, update centroids, repeat until convergence.", 'medium', 14),
        ("What is PCA (Principal Component Analysis)?",
         "A dimensionality reduction technique that finds directions of maximum variance",
         ["A clustering algorithm", "A type of regression",
          "A method for handling missing data"],
         "PCA projects data onto orthogonal principal components ordered by variance explained.", 'hard', 15),
        ("What is the ROC curve used for?",
         "Visualizing the tradeoff between true positive rate and false positive rate at various thresholds",
         ["Measuring regression model accuracy",
          "Comparing feature importances",
          "Plotting the learning curve"],
         "AUC-ROC: Area under the ROC curve. AUC = 1 is perfect; AUC = 0.5 is random.", 'hard', 15),
        ("What is transfer learning?",
         "Using a model trained on one task as a starting point for a different task",
         ["Moving a model between servers",
          "Training a model on multiple datasets simultaneously",
          "Copying training data between models"],
         "Transfer learning (common in NLP/CV): pretrain on large dataset, fine-tune on specific task.", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Machine Learning', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_deep_learning(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a neural network?",
         "A computational model with layers of interconnected neurons that learn from data",
         ["A type of decision tree", "A graph database",
          "A statistical regression model"],
         "Neural networks: input layer → hidden layers → output layer, connected by weights.", 'easy', 14),
        ("What is backpropagation?",
         "An algorithm that computes gradients by propagating error backward through the network",
         ["A method for initializing weights",
          "The forward pass through a neural network",
          "A regularization technique"],
         "Backprop uses the chain rule to compute ∂Loss/∂w for each weight.", 'hard', 14),
        ("What is an activation function?",
         "A function that introduces nonlinearity into a neural network",
         ["A function that initializes weights",
          "A method for normalizing inputs",
          "A function that selects training examples"],
         "Without activation functions, neural networks would be equivalent to linear regression.", 'medium', 14),
        ("What is ReLU?",
         "Rectified Linear Unit: f(x) = max(0, x) — the most common activation function",
         ["Random Learning Unit", "A type of recurrent layer",
          "f(x) = 1/(1+e⁻ˣ)"],
         "ReLU is computationally efficient and avoids vanishing gradient for positive values.", 'medium', 14),
        ("What is a convolutional neural network (CNN) used for?",
         "Image recognition and processing, detecting spatial patterns",
         ["Natural language processing", "Time series prediction",
          "Tabular data classification"],
         "CNNs use convolutional filters to detect edges, textures, and higher-level features.", 'medium', 14),
        ("What is a recurrent neural network (RNN) used for?",
         "Sequence data such as text, speech, and time series",
         ["Image classification", "Graph data",
          "Static tabular data"],
         "RNNs have feedback connections that allow them to maintain state over sequences.", 'medium', 14),
        ("What is dropout regularization?",
         "Randomly deactivating neurons during training to reduce overfitting",
         ["Removing features from the dataset",
          "Reducing the learning rate",
          "Removing layers from the network"],
         "Dropout forces the network to learn redundant representations, improving generalization.", 'hard', 15),
        ("What is the vanishing gradient problem?",
         "Gradients become extremely small in deep networks, preventing early layers from learning",
         ["The network becomes too large",
          "Gradients explode to very large values",
          "The loss function becomes zero"],
         "Solved by: ReLU activations, batch normalization, skip connections (ResNet).", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Deep Learning', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Data Handling':    [(gen_data_handling, {})],
    'Machine Learning': [(gen_machine_learning, {})],
    'Deep Learning':    [(gen_deep_learning, {})],
}

_DIFF_WEIGHTS = {t: {'easy': [fn], 'medium': [fn], 'hard': [fn]}
                 for t, [(fn, _)] in _TOPIC_GENERATORS.items()}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
    import random as _r
    rng = _r.Random(seed)
    fns = (_DIFF_WEIGHTS.get(topic, {}).get(difficulty)
           or [fn for fn, _ in _TOPIC_GENERATORS.get(topic, [])])
    if not fns:
        return []
    pool = []
    for fn in fns:
        pool.extend(fn(seed=rng.randint(0, 999999), n=max(count * 3, 30)))
    rng.shuffle(pool)
    return [{'id': -(i+1), 'subject': row[0], 'topic': row[1], 'difficulty': row[2],
             'question': row[3], 'choices': json.loads(row[4]), 'answer': row[5],
             'explanation': row[6]} for i, row in enumerate(pool[:count])]


def generate_all(seed=42):
    r = random.Random(seed)
    all_qs = []
    for fns in _TOPIC_GENERATORS.values():
        for fn, kwargs in fns:
            all_qs.extend(fn(seed=r.randint(0, 999999), n=30))
    return all_qs
