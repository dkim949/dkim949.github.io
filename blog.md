---
layout: default
title: 글
nav: blog
permalink: /blog/
---
<section class="section-page">
  <p class="eyebrow">FROM THE ARCHIVE</p>
  <h1>조금 길게 써둔 글.</h1>
  <div class="archive-list">
    {% for article in site.data.articles %}
    <a class="project" href="{{ article.url | relative_url }}"><div><h3>{{ article.title | escape }}</h3><p>{{ article.summary | escape }}</p></div><span class="arrow" aria-hidden="true">↗</span></a>
    {% endfor %}
  </div>
</section>
