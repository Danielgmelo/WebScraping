import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

c_bw = 'purple'
c_sep = 'dimgray'
c_ep = 'lightsalmon'

def box_amplitude(df):
    plt.figure(figsize=(20,5))
    sns.boxplot(data=df, x='player-sku', y='price', hue='player')
    plt.xticks(rotation=90)
    plt.title('Amplitude de preços de produtos com variação diária');
    

def hist_precos(df, bins, lim_price=None, subplot=None, xlim=None):
    if lim_price: df=df.query(f"price < {lim_price}")
    plt.subplot(subplot)
    plt.hist(df.query("player == 'sephora'")['price'], label='sephora', bins=bins, color='dimgray', alpha=0.5)
    plt.hist(df.query("player == 'belezanaweb'")['price'], label='bw', bins=bins, color='purple', alpha=0.5)
    plt.hist(df.query("player == 'epoca'")['price'], label='epoca', bins=bins, color='lightsalmon', alpha=0.5)
    plt.ylabel('frequência')
    plt.xlabel('preços')
    plt.legend(loc='upper right')
    plt.title('Distribuição dos preços (preço medio/dia)')
    

def hist_amplitude(df):
    plt.figure(figsize=(6,3))
    plt.hist(df.query("player == 'belezanaweb'")['amplitude'], label='bw', color=c_bw, alpha=0.7)
    plt.hist(df.query("player == 'sephora'")['amplitude'], label='sephora', color=c_sep, alpha=0.7)
    plt.hist(df.query("player == 'epoca'")['amplitude'], label='epoca', color=c_ep, alpha=0.7)
    plt.legend(loc='upper right')
    plt.xlabel('amplitude de preço');
    plt.title('histograma distribuição da amplitude')
    

def part_desc(df):
    (df
     .assign(part=(df['sku_com_desc']/df['sku_total'])
             .multiply(100)
             .round(2))['part']
     .plot
     .bar(title='% de produtos com desconto', figsize=(6,3)));
    plt.xticks(rotation=0)
    plt.ylabel('porcentual')
    
    
def dist_descontos(df, column, subplot):
    plt.subplot(subplot)
    plt.hist(df.query("player == 'belezanaweb'")[column], label='bw', color=c_bw, alpha=0.6)
    plt.hist(df.query("player == 'epoca'")[column], label='epoca', color=c_ep, alpha=0.6)
    plt.hist(df.query("player == 'sephora'")[column], label='sephora', color=c_sep, alpha=0.6)
    plt.legend(loc='upper right')
    plt.xlabel(column)
    plt.title('histograma distribuição de descontos');
    
    
def scatter_price_desc(df, player, subplot, color):
    df=df.query(f"player == '{player}'")
    plt.subplot(subplot)
    sns.scatterplot(data=df,x='valor_des',y='gross_price', color=color)
    plt.title(player)
    plt.ylim(0,2000);
    