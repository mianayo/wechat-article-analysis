from setuptools import setup, find_packages

setup(
    name="junlebao_analysis",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'scikit-learn>=0.24.0',
        'jieba>=0.42.1',
        'snownlp>=0.12.3',
        'wordcloud>=1.8.1',
        'requests>=2.26.0',
        'beautifulsoup4>=4.9.3',
        'fake-useragent>=0.1.11',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'plotly>=5.1.0',
        'networkx>=2.6.0',
        'python-docx>=0.8.11',
        'openpyxl>=3.0.7',
        'Pillow>=8.3.0',
        'tqdm>=4.62.0',
    ],
)
