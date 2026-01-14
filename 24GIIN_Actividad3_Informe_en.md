# Robustness Analysis and Semantic Convergence in Food Image Classification

**Author:** Jesús Navarro Cuquejo  
**University:** International University of Valencia  
**Location/Date:** Murcia, January 2026

## Abstract

This study investigates the relationship between training data volume and accuracy in food image classification models. Five instances of convolutional neural networks were trained varying the sample size (10, 20 and 30 images per category) to discriminate among five classes: soup, main course, salad, dessert and no-food. Experimental results show that increasing the dataset from 10 to 20 samples significantly reduces variance and improves overall accuracy from 88% to 92%. However, a further increase to 30 samples yields diminishing returns, stagnating at 92% overall accuracy. Error analysis reveals persistent semantic confusion between the "main course" and "dessert" classes, suggesting that visual similarity is a limiting factor beyond sample size in small-data regimes.

## I. Introduction

Visual recognition of food is a challenging domain within computer vision, characterized by deformable objects and a lack of rigid structure [1]. Unlike industrial object classification, food dishes show significant variation in presentation, lighting and composition, hindering model generalization to unseen data. This generalization challenge from limited data is a central problem addressed in modern Artificial Intelligence theory [2].

A critical obstacle for deploying these systems is the dependence on large volumes of labeled data. This work focuses on quantifying performance under low-data regimes, aiming to determine the minimum sample size required for robust predictions and to analyze the nature of persistent errors.

## II. Experimental Methodology

### A. Dataset Description

The study used a balanced dataset composed of RGB images resized to 224 x 224 pixels. The dataset taxonomy includes five disjoint classes:

1. **Soup**
2. **Main Course**
3. **Salad**
4. **Dessert**
5. **No Food**

### B. Experimental Design

An incremental experimental protocol was designed to evaluate model sensitivity to training-set size (k-shot):

- **Model 10 (A, B, C) (k=10):** Three independent models were trained with random initialization to evaluate variance and learning stability under minimal data. Subsets were created from the 30 available samples, producing 3 disjoint training sets.
- **Model 20_samples (k=20):** Model trained with a 100% increase in data volume.
- **Model 30_samples (k=30):** Model trained with the maximum available volume.

### C. Validation Protocol

Evaluation was performed on a static test set of 50 images (10 samples per class), fully independent from the training sets. To ensure external validity, test samples were selected to maximize diversity in color, viewpoint and scene composition; the same test set was used across evaluations so accuracy metrics are directly comparable [3].

## III. Quantitative Results

Table I summarizes quantitative performance. Standard supervised classification metrics were used, focusing primarily on accuracy as an indicator of model generalization capability [4].

An asymptotic behavior is observed: the jump from n=10 to n=20 yields a significant improvement, while the increase to n=30 does not report additional quantitative gains.

**Table I. Overall Performance by Model Configuration**

| Model            | Samples (n) | Correct Predictions (out of 50) | Accuracy |
|:------------------|:-----------:|:-------------------------------:|:--------:|
| Model 10_A       |     10      |               45                |  90.00%  |
| Model 10_B       |     10      |               44                |  88.00%  |
| Model 10_C       |     10      |               43                |  86.00%  |
| Model 20_samples |     20      |               46                |  92.00%  |
| Model 30_samples |     30      |               46                |  92.00%  |

Table I shows how performance gains level off after 20 samples. This indicates that the extra 10 samples in the 30-sample model did not provide sufficient informative variance to resolve remaining edge cases, a common phenomenon in deep learning when a model reaches its generalization capacity for a given dataset [2].

## IV. Discussion

### A. Analysis of models with different samples (n=10)

Results from the three 10-sample models demonstrate high sensitivity to training initial conditions. This instability aligns with fundamental machine learning theory [2], where approximating complex functions from scarce observations (k=10) leads to high variance and poor out-of-sample performance.

Volatility in the "No Food" category is notable (**Table II**). While Models A and C correctly classified 100% of samples, Model B showed a 20% drop. This disparity confirms that with n=10 the models fail to converge to a robust, generalizable solution.

**Table II. Inter-Model Variability Matrix (n=10)**

| Category        | Model A | Model B | Model C | Dispersion Range (Delta) |
|:----------------|--------:|--------:|--------:|-------------------------:|
| Soup            |    80%  |    90%  |    90%  | 10%                      |
| Main Course     |    90%  |    80%  |    70%  | 20% (Critical)           |
| Salad           |   100%  |   100%  |    90%  | 10%                      |
| Dessert         |    80%  |    90%  |    80%  | 10%                      |
| No Food         |   100%  |    80%  |   100%  | 20% (Critical)           |

Analyzing accumulated errors in the "Main Course" category, 66% of false negatives were misclassified as "Dessert". This suggests the network captures complex structures but lacks resolution to disambiguate semantically close classes.

### B. Semantic barrier in more robust models (n=20, 30)

A qualitative limitation is identified when evaluating the models. **Table III** shows that 75% of total errors concentrate in binary confusion between "Main Course" and "Dessert". Persistence of this error regardless of increased data points to a visual homography that requires more sophisticated attention mechanisms.

**Table III. Error Distribution in Converging Models (n = 20, 30)**

| Ground Truth Category | Failures (n=20) | Failures (n=30) | Cumulative Total | Primary Error Etiology |
|:----------------------|:---------------:|:---------------:|:----------------:|:----------------------:|
| Main Course           |        2        |        1        |        3         | Confusion with Dessert (66%) |
| Dessert               |        1        |        2        |        3         | Confusion with Main Course (66%) |
| Soup                  |        1        |        1        |        2         | Main Course / Salad confusion |
| Salad                 |        0        |        0        |        0         | -                      |
| No Food               |        0        |        0        |        0         | -                      |
| **TOTAL**             |     **4**       |     **4**       |     **8**        | Predominance of semantic error |

## V. Conclusions

This study supports two conclusions about deep neural networks [2]:

1. **Stability Threshold:** Empirically, n=20 samples per class appears to be the minimum threshold to eliminate critical variance observed in n=10 models.
2. **Semantic Complexity:** Increasing data to n=30 did not resolve confusion between "Main Course" and "Dessert". This indicates the problem is not purely quantitative but related to visual representation. Most errors in this study stem from confusion between these two classes, likely because both share low-level visual features (round plates, centered food, adjacent objects…), a problem residual architectures [1] may struggle to disambiguate without additional data. Increasing the dataset to 30 samples did not solve this issue.

To address these problems, prioritizing quality over quantity for conflicting classes is recommended, or implementing visual attention mechanisms capable of detecting discriminative features (e.g., sugar textures, cutlery types) that differentiate a dessert from a main course.

## References

[1] K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770–778.

[2] S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. Hoboken, NJ: Pearson, 2020.

[3] O. Russakovsky et al., "ImageNet Large Scale Visual Recognition Challenge," *International Journal of Computer Vision (IJCV)*, vol. 115, no. 3, pp. 211–252, 2015.

[4] Fayrix, "Machine Learning Model Evaluation Metrics," [Online]. Available: https://fayrix.com/machine-learning-metrics_es.
