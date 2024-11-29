class ContentAnalyzer:
    def __init__(self):
        pass
        
    def analyze_content(self, processed_articles):
        """分析处理后的文章内容"""
        analysis_results = {
            'total_articles': len(processed_articles),
            'article_analysis': [],
            'overall_stats': {
                'avg_word_count': 0,
                'avg_sentiment_score': 0,
                'topic_distribution': {},
                'keyword_frequency': {}
            }
        }
        
        # 分析每篇文章
        total_words = 0
        total_sentiment = 0
        
        for article in processed_articles:
            # 文章基本分析
            article_analysis = {
                'title': article['title'],
                'word_count': article['word_count'],
                'sentiment_score': article['sentiment']['score'],
                'topic': article['topic_category']['main_topic'],
                'keywords': article['keywords'],
                'readability': article['readability']
            }
            
            # 更新统计数据
            total_words += article['word_count']
            total_sentiment += article['sentiment']['score']
            
            # 更新主题分布
            topic = article['topic_category']['main_topic']
            analysis_results['overall_stats']['topic_distribution'][topic] = \
                analysis_results['overall_stats']['topic_distribution'].get(topic, 0) + 1
            
            # 添加到文章分析列表
            analysis_results['article_analysis'].append(article_analysis)
        
        # 计算平均值
        article_count = len(processed_articles)
        if article_count > 0:
            analysis_results['overall_stats']['avg_word_count'] = total_words / article_count
            analysis_results['overall_stats']['avg_sentiment_score'] = total_sentiment / article_count
        
        return analysis_results
