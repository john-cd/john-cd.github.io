---
title: Test
layout: inner
published: false
---
{% comment %}
{% for post in paginator.posts %}
    {% include tile.html %}
{% endfor %}
{% endcomment %}

{% comment %}
Dynamic menu 
https://thinkshout.com/blog/2014/12/creating-dynamic-menus-in-jekyll/
{% endcomment %}

{% assign url_parts = page.url | split: '/' %}
{% assign url_parts_size = url_parts | size %}
{% assign rm = url_parts | last %}
{% assign base_url = page.url | replace: rm %}

<ul>
{% for node in site.cheatsheets %}
  {% if node.url contains base_url %}
    {% assign node_url_parts = node.url | split: '/' %}
    {% assign node_url_parts_size = node_url_parts | size %}
    {% assign filename = node_url_parts | last %}
	<li><a href='{{node.url}}'>{{node.title}}</a></li>
    {% if filename != 'index.html' %}
      <li><a href='{{node.url}}'>{{node.title}}</a></li>
    {% endif %}
  {% endif %}
{% endfor %}
</ul>

 
 



