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
        try:
            # 确保文件名是UTF-8编码
            filename = filename.encode('cp437').decode('utf-8')
        except UnicodeEncodeError:
            # 如果已经是UTF-8编码，则直接使用
            pass
        except Exception as e:
            st.error(f"文件名编码转换错误: {str(e)}")
            return None

        # 修改为12位时间戳格式：yyyyMMddhhmm
        pattern = r"^(\d{12})(.*?)(\.html?)$"
        match = re.match(pattern, filename)
        if match:
            timestamp, title, ext = match.groups()
            try:
                # 解析12位时间戳，添加00秒
                date_str = timestamp + "00"  # 添加秒数
                date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
                
                # 清理标题中的特殊字符
                title = title.strip()
                title = re.sub(r'[_\|｜]', ' ', title)  # 替换下划线和竖线为空格
                title = re.sub(r'\s+', ' ', title)      # 合并多个空格
                
                return {
                    'timestamp': timestamp,
                    'date': date,
                    'title': title,
                    'extension': 'html',
                    'filename': filename
                }
            except ValueError as e:
                st.error(f"日期解析错误 {filename}: {str(e)}")
                return None
        return None

    def analyze_files(files_data):
        """分析文件数据"""
        df = pd.DataFrame(files_data)
        
        # 基础统计
        st.header("📊 基础统计")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("文章总数", len(df))
        with col2:
            if len(df) > 0:
                date_range = (df['date'].max() - df['date'].min()).days
                st.metric("时间跨度", f"{date_range} 天")
        with col3:
            if len(df) > 0:
                years = df['date'].dt.year.nunique()
                st.metric("跨越年份", f"{years} 年")

        if len(df) > 0:
            # 年度文章统计
            st.header("📈 年度文章统计")
            yearly_counts = df.groupby(df['date'].dt.year).size()
            fig = px.bar(x=yearly_counts.index, 
                         y=yearly_counts.values,
                         title="年度发文数量",
                         labels={'x': '年份', 'y': '文章数量'})
            st.plotly_chart(fig)

            # 月度趋势分析
            st.header("📊 月度发文趋势")
            df['month'] = df['date'].dt.strftime('%Y-%m')  # 使用更友好的月份格式
            monthly_counts = df.groupby('month').size().reset_index()
            fig = px.line(monthly_counts, 
                          x='month',
                          y=0,
                          title="月度发文趋势",
                          labels={'month': '月份', '0': '文章数量'})
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig)

            # 文章列表
            st.header("📝 文章列表")
            articles_df = df[['date', 'title']].copy()
            articles_df['date'] = articles_df['date'].dt.strftime('%Y-%m-%d %H:%M')  # 只显示到分钟
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
        2. 文件名格式要求：yyyyMMddhhmm文章标题.html
        3. 上传ZIP文件后系统将自动分析文章发布时间和标题
        """)

        uploaded_file = st.file_uploader("选择文章文件夹的ZIP压缩包", type="zip")

        if uploaded_file is not None:
            try:
                with zipfile.ZipFile(uploaded_file) as z:
                    files_data = []
                    for filename in z.namelist():
                        if filename.endswith('.html'):
                            # 获取文件名（去除路径）
                            base_filename = filename.split('/')[-1]
                            info = extract_info_from_filename(base_filename)
                            if info:
                                files_data.append(info)
                                
                    # 调试信息
                    if not files_data:
                        st.warning("文件列表：")
                        for filename in z.namelist():
                            if filename.endswith('.html'):
                                st.text(filename)

                    if files_data:
                        df = analyze_files(files_data)
                        
                        # 提供下载分析结果的功能
                        st.header("💾 导出分析结果")
                        # 使用 utf-8-sig 编码确保Excel正确显示中文
                        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
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
                # 显示详细错误信息
                import traceback
                st.error(traceback.format_exc())

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
