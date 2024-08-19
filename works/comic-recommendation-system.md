---
layout: page
title: Comic Book Recommendation System for Mobile Webtoon Users
---

# Comic Book Recommendation System for Mobile Webtoon Users

This project involved developing a recommendation system specifically for a newly launched mobile webtoon service. Given the novelty of the service, the system had to overcome significant challenges, particularly in providing accurate recommendations for new users with limited interaction data. To address these challenges, the LightFM library was leveraged to enhance the accuracy and relevance of the recommendations from the outset.

## Project Overview
- **Objective**: To successfully launch a new service by providing personalized comic book recommendations that increase user engagement and retention, even in the early stages of user interaction.

## Key Features
- **Recommendation Algorithm**:
  - **LightFM Hybrid Model**: Implemented using the LightFM library, which combines collaborative and content-based filtering. This hybrid approach was crucial in dealing with the cold start problem by using both user interaction data and comic book metadata.
  - **Cold Start Solutions**: To address the cold start problem inherent in a new service, the system utilized popularity-based recommendations and initial user preference surveys. This strategy helped in delivering relevant recommendations to new users with minimal data.

- **Data Sources**:
  - **User Interaction Data**: Despite limited initial data, the system analyzed reading history, favorites, and ratings to start building user profiles and refine recommendations as more data became available.
  - **Webtoon Metadata**: Incorporated detailed metadata like genre, author, and publication date to support the content-based filtering component, ensuring relevant suggestions from day one.
  - **Real-Time Adaptation**: The system dynamically adapted to real-time user behavior, ensuring that recommendations remained accurate and relevant as the service gained more users and data.

- **Challenges and Solutions**:
  - **Cold Start Problem**: The recommendation system was designed to cope with the challenges of a new service, where user interaction data was initially limited. LightFM’s hybrid model played a crucial role in mitigating the cold start problem by effectively using both collaborative and content-based filtering techniques.
  - **Scalability**: The system was built to scale as the user base grew, ensuring that recommendations remained responsive and relevant as more users and data were integrated into the platform.

- **Impact**:
  - **Successful Launch**: The recommendation system contributed to a successful launch by providing personalized recommendations that quickly engaged users, even with limited initial data.
  - **Increased User Engagement**: The personalized recommendations resulted in a significant increase in user engagement, with users spending more time on the platform.
  - **Improved User Retention**: The recommendation system contributed to higher user retention rates by keeping users engaged with content tailored to their preferences.

![Recommendation Workflow](../assets/images/comic-recommendation-workflow.png)

[Back to Home](../index.md)