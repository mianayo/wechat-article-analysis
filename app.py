import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import re
import io
import zipfile

# 添加错误处理和日志
try:
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
        pattern = r"^(\d{14})(.*?)(\.html?)$"
        match = re.match(pattern, filename)
        if match:
            timestamp, title, ext = match.groups()
            try:
                date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
                title = title.strip().replace('_', ' ')
                return {
                    'timestamp': timestamp,
                    'date': date,
                    'title': title,
                    'extension': ext.lstrip('.'),
                    'filename': filename
                }
            except ValueError:
                return None
        return None

    def analyze_files(files_data):
        """分析文件数据"""
        df = pd.DataFrame(files_data)
        
        # 基础统计
        st.header("📊 基础统计")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("文章总数", len(df))
        with col2:
            date_range = (df['date'].max() - df['date'].min()).days
            st.metric("时间跨度", f"{date_range} 天")

        # 时间趋势分析
        st.header("📈 发文时间趋势")
        df['month'] = df['date'].dt.to_period('M')
        monthly_counts = df.groupby('month').size()
        fig = px.bar(x=[str(m) for m in monthly_counts.index], 
                     y=monthly_counts.values,
                     title="月度发文数量",
                     labels={'x': '月份', 'y': '文章数量'})
        st.plotly_chart(fig)

        # 文章列表
        st.header("📝 文章列表")
        articles_df = df[['date', 'title']].copy()
        articles_df['date'] = articles_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        articles_df = articles_df.sort_values('date', ascending=False)
        st.dataframe(
            articles_df.rename(columns={
                'date': '发布时间',
                'title': '文章标题'
            }),
            use_container_width=True
        )

        return df

    def main():
        st.title("📱 微信公众号文章分析系统")
        st.markdown("---")

        # 文件上传说明
        st.markdown("""
        ### 使用说明
        1. 准备公众号文章的ZIP压缩包（包含.html文件）
        2. 文件名格式要求：yyyyMMddHHmmss文章标题.html
        3. 上传ZIP文件后系统将自动分析文章发布时间和标题
        """)

        uploaded_file = st.file_uploader("选择文章文件夹的ZIP压缩包", type="zip")

        if uploaded_file is not None:
            try:
                with zipfile.ZipFile(uploaded_file) as z:
                    files_data = []
                    for filename in z.namelist():
                        if filename.endswith('.html'):
                            base_filename = filename.split('/')[-1]
                            info = extract_info_from_filename(base_filename)
                            if info:
                                files_data.append(info)

                if files_data:
                    df = analyze_files(files_data)
                    
                    # 提供下载分析结果的功能
                    st.header("💾 导出分析结果")
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="下载分析数据(CSV)",
                        data=csv,
                        file_name="wechat_articles_analysis.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("未找到有效的文章文件，请确保ZIP包中包含正确格式的.html文件")
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")

    # 添加基本异常处理
    @st.cache_data
    def load_data():
        try:
            # 您的数据加载代码
            pass
        except Exception as e:
            st.error(f"数据加载错误: {str(e)}")
            return None

    main()

except Exception as e:
    st.error(f"应用启动错误: {str(e)}")
