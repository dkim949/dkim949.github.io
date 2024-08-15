---
layout: post
title:  "Practical Applications of Regression Models in B2C Services"
date:   2023-12-30
categories: [Statistics, Regression]
tags: [Python, Scikit-learn, Statsmodels, Regression]
---

In the world of Business-to-Consumer (B2C) services, data-driven decision-making is crucial for optimizing operations, understanding customer behavior, and improving service delivery. Various regression models, including Poisson and Logistic Regression, can help achieve these goals. In this blog post, we’ll explore practical applications of these regression methods using real-world examples.

# What is Generalized Linear Regression?
Generalized Linear Regression (GLM) is an extension of traditional linear regression that allows for the modeling of non-normally distributed data and relationships that may not be strictly linear. It is particularly useful when dealing with response variables that follow non-Gaussian distributions, such as Poisson or Logistic.

# Poisson Data Generation (Number of Deliveries)
To illustrate the concept of GLM, let’s start by generating synthetic data relevant to each regression model. 
Poisson Regression is used to model count data, particularly the number of times an event occurs within a fixed interval of time or space.  Let’s generate synthetic data where the response variable represents the number of customer orders generated per day based on promotional activities and advertising costs.

**Data Description**
We have generated synthetic data for 100 days, including the following variables:
- Day: The day of observation (1 to 100).
- Is_Promotion: Binary indicator of whether a promotion is active (1) or not (0).
- Num_Orders: The number of customer orders on that day.
- Advertising_Cost: The cost of advertising on that day (non-zero during promotion days).


```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Generate synthetic data
days = np.arange(1, 101)  # 100 days
is_promotion = np.concatenate([np.zeros(30), np.ones(40), np.zeros(30)])  # Promotion for 40 days in the middle
num_orders = np.random.poisson(lam=10000 + 500 * is_promotion + np.random.normal(scale=300, size=100))
advertising_cost = 10000 * is_promotion  # Advertising cost during promotion

data_poisson = pd.DataFrame({
    "Day": days,
    "Is_Promotion": is_promotion,
    "Num_Orders": num_orders,
    "Advertising_Cost": advertising_cost,
})
```

# Poisson Regression Model
The Poisson Regression model is used to predict the number of orders based on whether a promotion is active and the advertising cost.
```python
# Fit the Poisson regression model
poisson_model = smf.glm('Num_Orders ~ Is_Promotion + Advertising_Cost', data=data_poisson, family=sm.families.Poisson()).fit()

# Print the summary
print(poisson_model.summary())
```

