---
layout: post
title:  "Navigating Asymmetry in Delivery ETA Predictions: A Deep Dive into Custom Loss Functions with CatBoost and LightGBM"
date:   2024-04-25
categories: [ML]
tags: [Custom Loss, Asymmetric Loss, Ensemble Learning, LightGBM, CatBoost, XGBoost]
---

In the dynamic world of logistics and delivery services, the challenge of accurately predicting estimated time of arrival (ETA) is not just about achieving the lowest possible error. 

Often, the real-world business implications of these predictions dictate a need for strategic prioritization—particularly, the ability to manipulate and adjust predictions according to specific operational priorities. For instance, underestimating delivery times can be more costly than overestimating them, affecting customer satisfaction and operational efficiency.

![fig1]("../assets/images/2024-04-25-building-ensemble-models-with-an-asymmetric-loss/fig1.png")

This blog post explores my journey through the intricate process of developing and refining asymmetric loss functions to tackle these unique challenges. Traditional machine learning models excel at minimizing average errors but often fall short when it comes to aligning predictions with business objectives that require an asymmetric handling of prediction errors.

Here, I delve into how ensemble models, particularly CatBoost and LightGBM, can be adapted to prioritize business-critical outcomes over mere statistical accuracy. These powerful models are not only capable of handling vast amounts of data but also offer flexibility in crafting loss functions that can pivot towards business needs—such as emphasizing the cost of certain types of errors over others.

# Challenges with Conventional Loss Functions in Delivery ETA Prediction

In the pursuit of optimizing delivery ETA predictions, traditional loss functions such as Mean Squared Error (MSE) and Huber loss often fall short of addressing the asymmetric nature of business impacts associated with prediction errors. 

MSE, defined mathematically as `$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$`, heavily penalizes larger errors due to its quadratic nature. While this characteristic is beneficial for minimizing large deviations, it does not differentiate between overestimations and underestimations, treating all errors with uniform severity regardless of their direction. This symmetric treatment can be suboptimal in scenarios where underestimating delivery times is more detrimental than overestimating them, such as in logistics and customer satisfaction contexts.

Huber loss, on the other hand, attempts to bring a balance by combining the properties of MSE and Mean Absolute Error (MAE), defined as
`$L_\delta (a) = \begin{cases} 
  \frac{1}{2}(a)^2 & \text{for } |a| \leq \delta \\
  \delta (|a| - \frac{1}{2}\delta) & \text{otherwise}
\end{cases}$`, where $\delta$ is a hyperparameter that determines the threshold for switching from quadratic to linear loss. While Huber loss introduces a degree of robustness to outliers, it still lacks the flexibility to address the asymmetric nature of prediction errors that are prevalent in delivery ETA predictions.

This loss function is less sensitive to outliers than MSE by transitioning to linear behavior beyond a specified 
𝛿
δ value. However, like MSE, Huber loss inherently treats overestimations and underestimations equally, failing to incorporate the asymmetrical consequences that are often critical in operational decision-making. Neither MSE nor Huber loss allows for the customization needed to specifically penalize underpredictions more heavily than overpredictions, a feature that could be crucial for minimizing operational disruptions and enhancing customer experience.

By moving beyond these conventional loss functions and exploring custom asymmetric loss functions or leveraging advanced techniques like expectile regression, we can develop models that not only predict more accurately but also align more closely with strategic business objectives. This shift enables us to prioritize minimizing the most costly types of errors and adaptively tune our predictions to the unique demands and penalties specific to delivery services.

# Building Ensemble Models with Asymmetric Loss Functions

Exploring Custom Objectives with LightGBM and CatBoost

In my quest to fine-tune the prediction models for delivery ETAs, I initially leaned towards leveraging the flexibility of LightGBM and CatBoost's fobj and feval parameters. These parameters historically allowed for the specification of custom objective functions (fobj) and custom evaluation functions (feval), facilitating highly tailored modeling approaches. However, recent updates to both frameworks have streamlined their APIs, shifting the focus towards using the objective parameter directly with custom-defined functions for both training and evaluation purposes.

## Custom Objective Functions in LightGBM
```python
def asymmetric_mse(y_true, y_pred):
    """Custom asymmetric MSE where underestimations are penalized more."""
    residual = y_true - y_pred
    alpha = 2  # Penalty multiplier for underestimations
    grad = np.where(residual < 0, -2 * alpha * residual, -2 * residual)
    hess = np.where(residual < 0, 2 * alpha * np.ones_like(residual), 2 * np.ones_like(residual))
    return grad, hess
```

This function modifies the typical mean squared error loss to create
an asymmetric effect. The objective is to penalize underestimations more
heavily than overestimations to align with specific business needs where
underestimating can have worse consequences than overestimating.

## What are the grad and hess parameters?
- Gradient (grad): This is the first derivative of the loss function with respect to the model predictions. It indicates the direction and rate at which the loss function increases or decreases. LightGBM uses this information to decide how to adjust the model parameters to minimize the loss.
- Hessian (hess): This is the second derivative of the loss function with respect to the model predictions. It provides information about the curvature of the loss surface. Incorporating the Hessian allows LightGBM to optimize more efficiently and accurately because it has a better understanding of how quickly the gradient is changing. This is particularly important in Newton-based boosting approaches, where the Hessian is used to determine the optimal step size during each iteration of model updates.

And here's how you can use this custom objective function in LightGBM:

```python
import lightgbm as lgb

# Prepare datasets for LightGBM
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# Train the model with custom asymmetric MSE
params = {
    'objective': asymmetric_mse,
    'learning_rate': 0.1,
    'num_leaves': 31,
    'metric': 'None'  # Disable default metrics, use custom evaluation instead
}

model_lgbm = lgb.train(params,
                       train_data,
                       num_boost_round=1000,
                       valid_sets=[valid_data],
                       early_stopping_rounds=50,
                       verbose_eval=100)

# Predict and evaluate
lgbm_preds = model_lgbm.predict(X_test)
print(f"Custom Asymmetric MSE Evaluation: {np.mean((y_test - lgbm_preds)**2)}")

```



# Challenges and Considerations

Despite these enhancements simplifying the process on paper, integrating custom objective functions into broader machine learning pipelines presented significant challenges. Specifically, when extending the models to work with optimization and deployment frameworks such as Hyperopt for hyperparameter tuning and ONNX Runtime for model serialization and deployment, I encountered numerous compatibility issues. These frameworks often assume standard model configurations, and custom objectives introduced complexities that led to a range of errors and integration hurdles.

The necessity to work seamlessly across various tools for optimization, evaluation, and deployment meant reevaluating the use of custom objective functions. The integration difficulties underscored the need for a more universally compatible approach, particularly when dealing with sophisticated machine learning operations that extend beyond the training environment into production systems.

Going forward, I will shift to further exploring and implementing expectile and quantile regression. By integrating these techniques, we aim to refine our predictive models, reduce operational challenges, and improve the scalability and robustness of our delivery predictions, ensuring they meet our specific business objectives with greater efficiency.


