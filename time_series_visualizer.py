import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col=["date"])

# Clean data
df = df[ 
    (df["value"] >= df["value"].quantile(0.025)) & 
    (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    # Tạo figure và axes
    fig, ax = plt.subplots(figsize=(30, 10))  # Tạo figure và axes trước

    # Vẽ line plot với Matplotlib
    ax.plot(df.index, df['value'], 'r', linewidth=1) 

    # Đặt tiêu đề và các nhãn
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # 1. Tạo cột 'year' và 'month' từ cột 'date'
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # 2. Nhóm theo 'year' và 'month', tính trung bình lượt xem mỗi ngày
    df_bar.rename(columns={'value': 'page_views'}, inplace=True)
    df_bar_grouped = df_bar.groupby(['year', 'month'])['page_views'].mean().reset_index()

    # 3. Tạo pivot table để chuyển 'month' thành cột
    df_pivot = df_bar_grouped.pivot(index='year', columns='month', values='page_views')

    # 4. Vẽ biểu đồ cột
    fig, ax = plt.subplots(figsize=(10, 6))
    df_pivot.plot(kind='bar', ax=ax)
    
    # 5. Đặt tiêu đề và nhãn
    ax.set_title('Months')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # 6. Hiển thị legend cho các tháng
    ax.legend(title='Months', labels=[ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    # 7. Lưu hình ảnh
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #Sort value theo đúng thứ tự tháng
    df_box['month_num']=df_box['date'].dt.month
    df_box=df_box.sort_values(by='month_num', ascending=True)
    
    #Tạo Figure và các axes (subplots) để hiển thị 2 boxplots cạnh nhau: 1 row 2 cols
    fig, axes = plt.subplots(1, 2, figsize=(15, 6 ))
    
    # Draw box plots (using Seaborn)
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0], palette='husl', hue='year', legend=False)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1], palette='Set2', hue='month', legend=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Điều chỉnh khoảng cách giữa 2 biểu đồ để dễ nhìn
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig