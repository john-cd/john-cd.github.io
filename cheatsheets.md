---
title: Cheatsheets
layout: page
permalink: cheatsheets/
---

You will find here a collection of cheatsheets, code templates and snippets that I have collected over the years...

Given that they were created for my own use, these notes are often very terse and dense. Thank you for your patience, while I am slowly improving their readability. I also have hundreds more to move to GitHub Pages :-) 

In the meanwhile, feel free to use as you wish. Please email me suggestions and corrections. 

-------------------------------------------
{% assign items_grouped = site.cheatsheets | group_by: 'category'  %}
{% comment %} 
  Consider: | sort: 'name' | reverse

  The above returns, for example, which is why we sort by 'name'
  {"name"=>"category1_value", "items"=>[#, #, #, #, #]}{"name"=>"category2_value", "items"=>[#, #, #, #]}
{% endcomment %}

{% comment %} Loop through the groups {% endcomment %}
{% for group in items_grouped %}
### {{ group.name }}
    {% assign items = group.items | sort: 'date' %}
    {% for item in items  %}
- [{{ item.title }}]({{ item.url | relative_url }})
    {% endfor %}
{% endfor %}   

{% comment %} 

Alternatively, use http://stackoverflow.com/questions/17118551/generating-a-list-of-pages-not-posts-in-a-given-category

- add to _config.yml

category-list: [dotNET, python, java, databases, search, frontend, markup, cloud, devops, sourcecontrol]

- use the following loop:

{% for cat in site.category-list %}
### {{ cat }}
<ul > <!-- class="post-list" -->
  {% for sheet in site.cheatsheets %}
      {% for pc in sheet.categories %}
        {% if pc == cat %}
          <li>
              <a href="{{ sheet.url | relative_url }}">{{ sheet.title | escape }}</a> <!-- class="post-link" -->
          </li>
        {% endif %}   <!-- cat-match-p -->
      {% endfor %}  <!-- page-category -->
  {% endfor %}  <!-- sheet -->
</ul>
{% endfor %}  <!-- cat -->

{% endcomment %}