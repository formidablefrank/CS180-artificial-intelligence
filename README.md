# CS180 Machine Learning

I completed this coursework in my artificial intelligence course where I implemented classical machine learning algorithms from scratch using Python. This repository contains my solutions to problem sets that demonstrate my ability to implement search-based AI, probabilistic inference, and statistical learning.

## Learning Objectives

Through this coursework, I developed proficiency in:

- **Heuristic Search Algorithms**: I implemented A* search and greedy best-first search algorithms with admissible and consistent heuristics
- **Probabilistic Inference**: I built a Naive Bayes classifier with Laplace smoothing for text classification
- **Statistical Learning**: I used LIBSVM to apply Support Vector Machines with different kernel types for classification tasks
- **Algorithm Analysis**: I analyzed time complexity, space complexity, and algorithmic trade-offs
- **Data Structures**: I designed and implemented custom data structures including priority queues and nodes for graph traversal
- **Software Development**: I wrote clean, documented Python code with proper abstraction and separation of concerns

## Problem Sets

### Machine Exercise 1: Pathfinding and Heuristic Search
I implemented a pathfinding algorithm to solve a maze using search algorithms. I developed a `Node` class representing states in the search space and a `Map` class managing the problem environment. I compared greedy best-first search (using only the heuristic estimate) with A* search (combining cost and heuristic). I tested the algorithms on various maze configurations with different movement costs and evaluated their performance in finding optimal paths.

### Machine Exercise 2: Naive Bayes Classification
I built a spam detection system using Naive Bayes classification. I implemented probability estimation from training data and applied Laplace smoothing to handle unseen words. The filter processes text documents as binary feature vectors and classifies them as spam or legitimate mail based on word frequencies and conditional probabilities.

### Machine Exercise 3: Support Vector Machines
I applied SVMs to classification problems using the LIBSVM library. I experimented with linear and radial basis function kernels, tuned hyperparameters, and evaluated classification accuracy on test datasets. I developed utility functions to convert data formats and test the classifier on different problem sets.

## Software Stack

Python, LIBSVM

## References

- Russell, S. J., & Norvig, P. (2010). Artificial Intelligence: A Modern Approach (3rd ed.)
- Chang, C. C., & Lin, C. J. (2011). LIBSVM: A Library for Support Vector Machines
- Naive Bayes Classification tutorials and probabilistic inference resources
