import requests
import json
import time
from datetime import datetime
import logging
import os
import re
from urllib.parse import urlencode

class WeChatCrawler:
    def __init__(self):
        self.data_dir = 'data/articles'
        os.makedirs(self.data_dir, exist_ok=True)
        
    def crawl_articles(self, account_name, num_articles=10):
        """一键爬取公众号文章"""
        try:
            print("\n===== 君乐宝公众号文章一键获取工具 =====")
            print("\n请输入任意一篇君乐宝公众号文章的链接")
            print("例如: https://mp.weixin.qq.com/s/Pm8OdiDf_vrnF-ClNB9HJg")
            
            url = input("\n请输入文章链接: ").strip()
            if not url:
                print("链接不能为空")
                return []
                
            print("\n正在分析链接...")
            # 从URL中提取参数
            biz = re.search(r'__biz=([^&]+)', url)
            if not biz:
                print("未找到 __biz 参数，请确认链接是否正确")
                return []
                
            biz = biz.group(1)
            print(f"找到公众号 ID: {biz}")
            
            # 构造历史消息链接
            history_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}&scene=124#wechat_redirect"
            print("\n请使用微信扫描以下链接访问历史文章页面：")
            print(history_url)
            
            print("\n操作步骤：")
            print("1. 使用手机微信扫描上面的链接")
            print("2. 在历史文章页面下拉加载更多文章")
            print("3. 复制看到的任意文章链接粘贴到下面")
            
            articles = []
            while True:
                article_url = input("\n请输入文章链接（直接回车结束）: ").strip()
                if not article_url:
                    break
                    
                try:
                    print(f"\n正在获取文章: {article_url}")
                    response = requests.get(article_url, headers={
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
                    })
                    response.encoding = 'utf-8'
                    
                    # 解析文章内容
                    title = re.search(r'var msg_title = "(.*?)";', response.text).group(1)
                    publish_time = re.search(r'var ct = "(.*?)";', response.text).group(1)
                    content = re.search(r'var content = \'(.*?)\';', response.text, re.S).group(1)
                    
                    article = {
                        'title': title,
                        'url': article_url,
                        'publish_time': publish_time,
                        'content': content,
                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    articles.append(article)
                    print(f"成功获取文章: {title}")
                    
                except Exception as e:
                    print(f"获取文章失败: {str(e)}")
                    continue
            
            # 保存文章数据
            if articles:
                self._save_articles(articles)
                print(f"\n成功保存 {len(articles)} 篇文章")
                print(f"文章保存在: {self.data_dir} 目录下")
                
            return articles
                
        except Exception as e:
            print(f"爬取失败: {str(e)}")
            raise
    
    def _save_articles(self, articles):
        """保存文章数据"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_dir, f'articles_{timestamp}.json')
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
