import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_distribution(df: pd.DataFrame, y: str, title: str, plt_type: str='box'):
    if plt_type not in ('violin', 'box', 'both'):
        raise ValueError('plt can only be box, violin or both')
    
    plots = 2 if plt_type != 'both' else 3
    
    plt.figure(figsize=(14, 7))
    plt.subplot(1, plots, 1)
    df[y].hist()
    plt.title(title)
    plt.ylabel(y)
    plot_pos = 2

    if plt_type in {'box', 'both'}:
        plt.subplot(1, plots, plot_pos)
        sns.boxplot(y=y, data=df)
        plt.ylabel(title)
        plt.title(f'{title} distribution')
        plot_pos = 3
    
    if plt_type in {'violin', 'both'}:
        plt.subplot(1, plots, plot_pos)
        sns.violinplot(y=y, data=df)
        plt.ylabel(title)
        plt.title(f'{title} distribution')

    plt.tight_layout()
    plt.show()

    print(f'Skew: {df[y].skew()}')
    print(f'Kurtosis: {df[y].kurt()}')