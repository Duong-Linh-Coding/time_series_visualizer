import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Parse dates, set index column to 'date')
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col=["date"])

# Clean data as the requirement
df = df[ 
    (df["value"] >= df["value"].quantile(0.025)) & 
    (df["value"] <= df["value"].quantile(0.975))]

def draw_line_plot():
    # Create figure & axes
    fig, ax = plt.subplots(figsize=(30, 10))

    # Draw line plot using Matplotlib
    ax.plot(df.index, df['value'], 'r', linewidth=1) 

    # Set title & labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy data for monthly bar plot
    df_bar = df.copy()

    # 1. Create 'year' & 'month' column from 'date' column
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # 2. Group by 'year' & 'month', calculate average page views, reset index)
    df_bar.rename(columns={'value': 'page_views'}, inplace=True)
    df_bar_grouped = df_bar.groupby(['year', 'month'])['page_views'].mean().reset_index() 

    # 3. Create pivot table to create 'month' column
    df_pivot = df_bar_grouped.pivot(index='year', columns='month', values='page_views')

    # 4. Draw bar graph
    fig, ax = plt.subplots(figsize=(10, 6))
    df_pivot.plot(kind='bar', ax=ax)
    
    # 5. Set title & labels
    ax.set_title('Months')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # 6. Display legend for months
    ax.legend(title='Months', labels=[ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    # 7. Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots 
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Sort value in month order
    df_box['month_num']=df_box['date'].dt.month
    df_box=df_box.sort_values(by='month_num', ascending=True)
    
    # Create figure & axes (subplots) to display 2 boxplots next to each other: 1 row 2 cols
    fig, axes = plt.subplots(1, 2, figsize=(15, 6 ))
    
    # Draw box plots (using Seaborn), divide the fig into 2 plots (year, month plot)
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0], palette='husl', hue='year', legend=False)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
     
    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1], palette='Set2', hue='month', legend=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Adjust the layout for good looking
    plt.tight_layout()

    # Save image and return fig 
    fig.savefig('box_plot.png')
    return fig
