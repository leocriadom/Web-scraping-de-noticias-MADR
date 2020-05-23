#!/usr/bin/env python
# coding: utf-8

# Autor: Leonel Criado
# 
# Proyecto: Análisis de noticias del Ministerio de Agricultura y Desarrollo Rural de Colombia
# 
# Creado: 2020-05-18
# 
# Meta: Funciones de ayuda para web scraping de noticias

# ### Necesitamos:
# - Beautiful Soup

# In[1]:


# Librerías
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pickle
import time
import random


# In[2]:


def get_html(url):
    '''
    Scraping de las noticias
    '''
    resp = requests.get(url).text
    return BeautifulSoup(resp,"lxml")


# In[3]:


def get_news(soup):
    '''
    Retorna el texto de la noticia
    '''
    if str(soup.find_all(['p', 'div'], {"class": "pad"}))!="[]":
        soup = str(soup.find_all(['p', 'div'], {"class": "pad"}))
    elif str(soup.find_all(['p', 'div'], {"class": "article-content"}))!="[]":
        soup = str(soup.find_all(['p', 'div'], {"class": "article-content"}))
    else:
        soup = str(soup.find_all(['p', 'div'], {"class": "contenido grd9"}))
    return soup


# In[4]:


def get_title(soup):
    '''
    Returna el título de la noticia
    '''
    try:
        title = soup.title.text.strip()
    except AttributeError:
        title = "N.A"
    return title


# In[5]:


def get_date(soup):
    '''
    Retorna la fecha de la noticia
    '''
    date = str(soup.find_all("span",class_="fecha"))
    if len(re.findall('\xa0(.{10})', date)) != 0:
        date = re.findall('\xa0(.{10})', date)[0]
        date = date.split("/")
        dia = date[0]
        mes = date[1]
        año = date[2]
        año = re.findall('[0-9]+', año)
    else:
        dia = 'N.A.'
        mes = 'N.A.'
        año = 'N.A.'       
    return [dia, mes, año]


# In[6]:


def get_location(soup):
    '''
    Retorna la ubicación
    '''
    text = str(soup.find_all(['p', 'div'], {"class": "pad"}))
    if len(re.findall('strong>(.*)</strong', text)) != 0:
        ubicacion = re.findall('strong>(.*)</strong', text)[0]
        if len(re.findall("(\w+),", ubicacion)) != 0:
            ubicacion = re.findall("(\w+),", ubicacion)[0]
        else:
            ubicacion = 'N.A.'
    elif len(re.findall('div><div><br/></div><div>(.*) –\xa0', text)) != 0:
        ubicacion = re.findall('div><div><br/></div><div>(.*) –\xa0', text)[0]
        ubicacion = re.findall("(\w+),", ubicacion)[0]
    else:
        ubicacion = 'N.A.'
    return ubicacion


# In[7]:


def remove_tags(text):
    '''
    Limpia el texto de la noticia y obtiene la ubicación
    '''
    news = re.sub('<[^>]+>|\]|\[|\r|\t|\\n|\xa0|\\u200b', ' ', text) #•
    news = re.sub("Contenido de la página ","", news)
    news = re.sub("Red de Comunicaciones","\t", news)
    news = re.sub("Leyenda de imagen","\t", news)
    seccion = news.count("\t")
    if seccion==2:
        news = re.search('\t(.*)\t', news).group()
        news = re.sub('|\t', '', news)
    elif seccion==1:
        news = re.search('\t(.*)', news).group()
        news = re.sub('|\t', '', news)
    news = " ".join(news.split())
    return [news, seccion]


# In[8]:


def get_news_elements(news_url):
    '''
    Retorna los elementos de la noticia
    '''
    print('News url: ', news_url)
    soup = get_html(news_url)
    title = get_title(soup)
    dia, mes, año = get_date(soup)
    ubicacion = get_location(soup)
    news_MADR, seccion = remove_tags(get_news(soup))
    time.sleep(random.randint(1,5))
    return [dia, mes, año, ubicacion, title, news_url, news_MADR, seccion]

