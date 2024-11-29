import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import re
import io
import zipfile

# 设置页面配置
st.set_page_config(
    page_title="微信公众号文章分析",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def extract_info_from_filename(filename):
    """从文件名中提取信息"""
    pattern = r"(\d{14})(.*?)\.(.*?)$"
    match = re.match(pattern, filename)
    if match:
        timestamp, title, ext = match.groups()
        date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        return {
            'timestamp': timestamp,
            'date': date,
            'title': title.strip(),
            'extension': ext,
            'filename': filename
        }
    return None

def analyze_files(files_data):
    """分析文件数据"""
    df = pd.DataFrame(files_data)
    
    # 基础统计
    st.header("📊 基础统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("文章总数", len(df['title'].unique()))
    with col2:
        st.metric("文件总数", len(df))
    with col3:
        st.metric("文件格式数", len(df['extension'].unique()))

    # 文件格式分布
    st.header("📁 文件格式分布")
    format_dist = df['extension'].value_counts()
    fig = px.pie(values=format_dist.values, 
                 names=format_dist.index, 
                 title="文件格式分布")
    st.plotly_chart(fig)

    # 时间趋势分析
    st.header("📈 发文时间趋势")
    daily_counts = df.groupby(df['date'].dt.date)['title'].nunique()
    fig = px.line(x=daily_counts.index, 
                  y=daily_counts.values,
                  title="每日发文数量",
                  labels={'x': '日期', 'y': '文章数量'})
    st.plotly_chart(fig)

    # 文章列表
    st.header("📝 文章列表")
    articles = df[['date', 'title']].drop_duplicates()
    articles = articles.sort_values('date', ascending=False)
    st.dataframe(
        articles.rename(columns={
            'date': '发布时间',
            'title': '文章标题'
        })
    )

    return df

def main():
    st.title("📱 微信公众号文章分析系统")
    st.markdown("---")

    # 文件上传说明
    st.markdown("""
    ### 使用说明
    1. 准备公众号文章文件夹的压缩包（ZIP格式）
    2. 点击下方"上传文件"按钮上传压缩包
    3. 等待分析完成
    """)

    # 文件上传
    uploaded_file = st.file_uploader("选择文章文件夹的ZIP压缩包", type="zip")

    if uploaded_file is not None:
        # 读取ZIP文件
        with zipfile.ZipFile(uploaded_file) as z:
            # 收集文件信息
            files_data = []
            for filename in z.namelist():
                if filename.endswith(('.pdf', '.docx', '.md', '.html', '.mhtml')):
                    info = extract_info_from_filename(filename.split('/')[-1])
                    if info:
                        files_data.append(info)

        if files_data:
            # 分析数据
            df = analyze_files(files_data)

            # 提供下载分析结果的功能
            st.header("💾 导出分析结果")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="下载分析数据(CSV)",
                data=csv,
                file_name="wechat_articles_analysis.csv",
                mime="text/csv"
            )
        else:
            st.error("未找到有效的文章文件，请检查ZIP文件内容")

if __name__ == "__main__":
    main()
