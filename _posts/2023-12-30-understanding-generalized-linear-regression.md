---
layout: post
title:  "Understanding Generalized Linear Regression with Python"
date:   2023-12-30
categories: [Statistics, Regression]
tags: [Python, Scikit-learn, Statsmodels]
---

Linear regression is a powerful tool for modeling the relationship between variables, but what if your data doesn’t meet the assumptions of traditional linear regression? This is where generalized linear regression comes in handy. In this blog post, we’ll explore the basics of generalized linear regression, focusing on Poisson and Binomial models, and demonstrate how to implement them using Python.

# What is Generalized Linear Regression?
Generalized Linear Regression (GLM) is an extension of traditional linear regression that allows for the modeling of non-normally distributed data and relationships that may not be strictly linear. It is particularly useful when dealing with response variables that follow non-Gaussian distributions, such as Poisson or Binomial.

# Synthetic Data Generation
To illustrate the concept of GLM, let’s start by generating synthetic data relevant to delivery services. We’ll create datasets suitable for Poisson and Binomial regression models.

## Poisson Data Generation (Number of Deliveries)
Poisson regression is used for count data. Let’s generate synthetic data where the response variable represents the number of deliveries completed in an hour.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Generate synthetic data
hours = np.arange(1, 101)  # Hours from 1 to 100
# Simulate number of deliveries as a function of hour of the day and other noise factors
num_deliveries = np.random.poisson(lam=5 + 0.1 * hours + np.sin(hours / 5))

# Convert to pandas DataFrame
data_poisson = pd.DataFrame({'Hour': hours, 'Num_Deliveries': num_deliveries})

# Plot the data
plt.scatter(data_poisson['Hour'], data_poisson['Num_Deliveries'], color='blue')
plt.title('Synthetic Data: Number of Deliveries')
plt.xlabel('Hour')
plt.ylabel('Number of Deliveries')
plt.show()
```

## Binomial Data Generation (On-time Delivery)
Binomial regression (or logistic regression) is used for binary outcome variables. Let’s generate synthetic data where the response variable represents whether a delivery was on time or not.

```python
# Generate synthetic data
np.random.seed(42)
num_samples = 100
hours = np.random.normal(12, 3, num_samples)  # Delivery time (in hours)
traffic = np.random.randint(0, 2, num_samples)  # Traffic condition (0 = low, 1 = high)
is_rush_hour = (hours >= 17) & (hours <= 19)  # Rush hour indicator

# Create a binary response variable based on a logistic model
logit = 2 - 0.1 * hours - 0.5 * traffic + 0.5 * is_rush_hour
prob_on_time = 1 / (1 + np.exp(-logit))
on_time = np.random.binomial(1, p=prob_on_time, size=num_samples)

# Convert to pandas DataFrame
data_binomial = pd.DataFrame({'Hours': hours, 'Traffic': traffic, 'Rush_Hour': is_rush_hour, 'On_Time': on_time})

# Plot the data
plt.scatter(data_binomial['Hours'], data_binomial['On_Time'], c=data_binomial['Traffic'], cmap='bwr', label='On Time')
plt.title('Synthetic Data: On-time Delivery')
plt.xlabel('Hours')
plt.ylabel('On-time Delivery (1 = Yes, 0 = No)')
plt.show()
```

# Implementing Generalized Linear Regression

## Poisson Regression
Poisson regression is suitable for modeling count data. Let’s fit a Poisson regression model to predict the number of deliveries.
```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Fit the Poisson model
model_poisson = smf.glm('Num_Deliveries ~ Hour', data=data_poisson, family=sm.families.Poisson()).fit()

# Print the summary
print(model_poisson.summary())

# Predict and plot the fitted line
data_poisson['Predicted_Deliveries'] = model_poisson.predict(data_poisson['Hour'])

plt.scatter(data_poisson['Hour'], data_poisson['Num_Deliveries'], color='blue', label='Data')
plt.plot(data_poisson['Hour'], data_poisson['Predicted_Deliveries'], color='red', label='Fitted line')
plt.title('Generalized Linear Regression (Poisson Family)')
plt.xlabel('Hour')
plt.ylabel('Number of Deliveries')
plt.legend()
plt.show()
```
## Binomial Regression
Binomial regression (or logistic regression) is used for binary outcome variables. Let’s fit a Binomial regression model to predict on-time delivery.

```python
# Fit the Binomial model
model_binomial = smf.glm('On_Time ~ Hours + Traffic + Rush_Hour', data=data_binomial, family=sm.families.Binomial()).fit()

# Print the summary
print(model_binomial.summary())

# Predict and plot the fitted probabilities
data_binomial['Predicted_Probability'] = model_binomial.predict(data_binomial[['Hours', 'Traffic', 'Rush_Hour']])

plt.scatter(data_binomial['Hours'], data_binomial['On_Time'], c=data_binomial['Traffic'], cmap='bwr', label='On Time')
plt.scatter(data_binomial['Hours'], data_binomial['Predicted_Probability'], color='red', label='Predicted Probability')
plt.title('Generalized Linear Regression (Binomial Family)')
plt.xlabel('Hours')
plt.ylabel('Probability of On-time Delivery')
plt.legend()
plt.show()
```

# Comparison with Linear Models

## Poisson vs. Linear Regression

Linear regression assumes that the response variable is continuous and normally distributed. However, when the response variable represents counts, Poisson regression is more appropriate.

## Linear Regression Issues with Count Data:
- It can predict negative values, which are not possible for count data.
- The residuals are often not normally distributed.
- Variance of counts typically increases with the mean, violating the constant variance assumption of linear regression.

## Poisson Regression Advantages:
- It models the log of the expected counts, ensuring non-negative predictions.
- It naturally handles the variance-mean relationship of count data.

## Binomial vs. Linear Regression

Linear regression is not suitable for binary outcome variables as it can predict values outside the [0, 1] range, which are not meaningful probabilities.

## Linear Regression Issues with Binary Data:
- Predictions can fall outside the [0, 1] range.
- The assumption of normally distributed residuals is violated.
- It does not capture the probabilistic nature of binary outcomes.

## Binomial Regression Advantages:
- It models the log odds of the probability of the outcome, ensuring predictions are valid probabilities.
- It captures the binary nature of the response variable effectively.

# Conclusion

In this blog post, we’ve explored Poisson and Binomial generalized linear models and demonstrated their implementation using Python. We also compared these models with traditional linear regression, highlighting their advantages for specific types of data.

Understanding and applying generalized linear regression expands your analytical toolkit, enabling you to model relationships in diverse datasets beyond the scope of traditional linear regression.

Feel free to experiment with different datasets and GLM families to deepen your understanding of generalized linear regression in Python.