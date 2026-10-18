---
layout: default
title: 만든 것
nav: works
permalink: /works/
---
<section class="section-page">
  <p class="eyebrow">SELECTED WORK</p>
  <h1>그동안 만든 것.</h1>
  <div class="archive-list">
    {% for project in site.data.projects %}
    <a class="project" href="{{ project.url | relative_url }}"><div><h3>{{ project.title | escape }}</h3><p>{{ project.summary | escape }}</p></div><span class="arrow" aria-hidden="true">↗</span></a>
    {% endfor %}
  </div>
</section>
