# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import jieba
import jieba.analyse
from snownlp import SnowNLP
import re
import os
import requests
from PIL import Image
from io import BytesIO
import hashlib
from datetime import datetime

class ContentProcessor:
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.image_dir = 'output/images'
        os.makedirs(self.image_dir, exist_ok=True)
        
    def _load_stop_words(self):
        """加载停用词"""
        stop_words = set()
        try:
            with open('data/stop_words.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    stop_words.add(line.strip())
        except FileNotFoundError:
            # 如果文件不存在，使用基本停用词
            stop_words = {'的', '了', '和', '是', '就', '都', '而', '及', '与', '这', '也', '在'}
        return stop_words

    def process_article(self, article):
        """处理单篇文章"""
        processed = article.copy()
        
        # 1. 内容清洗
        cleaned_content = self._clean_content(article['content'])
        
        # 2. 内容增强
        processed.update({
            'cleaned_content': cleaned_content,
            'word_count': len(cleaned_content),
            'keywords': self._extract_keywords(cleaned_content),
            'summary': self._generate_summary(cleaned_content),
            'sentiment': self._analyze_sentiment(cleaned_content),
            'readability': self._calculate_readability(cleaned_content),
            'topic_category': self._categorize_topic(cleaned_content),
            'content_structure': self._analyze_structure(cleaned_content),
            'processed_images': self._process_images(article['images'])
        })
        
        return processed

    # ... 其他方法保持不变 ...
