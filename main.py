import os
import sys
from datetime import datetime
from tqdm import tqdm
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)

logging.debug(f"Current directory: {current_dir}")
logging.debug(f"Python path: {sys.path}")

# 直接导入模块，然后从模块中获取类
try:
    from modules.processor import ContentProcessor
    logging.debug("Successfully imported ContentProcessor")
except ImportError as e:
    logging.error(f"Import error: {str(e)}")
    logging.error(f"Current working directory: {os.getcwd()}")
    raise

from modules.crawler import WeChatCrawler
from modules.analyzer import ContentAnalyzer
from modules.reporter import ReportGenerator

def main():
    logging.debug("程序开始运行")
    print("开始君乐宝公众号文章分析系统...")
    
    try:
        # 1. 爬取数据
        print("\n1. 开始爬取文章...")
        crawler = WeChatCrawler()
        try:
            articles = crawler.crawl_articles("君乐宝")
            print(f"共爬取到 {len(articles)} 篇文章")
        except Exception as e:
            print(f"爬取文章失败: {str(e)}")
            raise
        
        if not articles:
            print("未获取到任何文章，程序退出")
            return
            
        # 2. 处理内容
        print("\n2. 处理文章内容...")
        processor = ContentProcessor()
        processed_articles = []
        for article in tqdm(articles, desc="处理文章"):
            processed = processor.process_article(article)
            processed_articles.append(processed)
        
        # 3. 分析内容
        print("\n3. 分析文章...")
        analyzer = ContentAnalyzer()
        analysis_results = analyzer.analyze_content(processed_articles)
        
        # 4. 生成报告
        print("\n4. 生成分析报告...")
        reporter = ReportGenerator()
        output_dir = 'output'
        reporter.generate_report(analysis_results, output_dir)
        
        print(f"\n分析完成！报告已保存到: {output_dir}")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        logging.exception("程序执行出错")
        raise

if __name__ == "__main__":
    main()
