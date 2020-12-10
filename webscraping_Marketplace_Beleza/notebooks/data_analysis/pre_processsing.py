import pandas as pd

def change_price(df):
    df = df.sort_values(['sku','date'])
    atual = 0
    anterior = -1

    col = []
    while atual < len(df['price']):

        if df['sku'].iloc[atual] == df['sku'].iloc[anterior] and atual == 0:
            col.append(False)
            
        elif df['sku'].iloc[atual] == df['sku'].iloc[anterior] and atual > 0:

                if df['price'].iloc[atual] != df['price'].iloc[anterior]:
                    col.append(True)
                else:
                    col.append(False)
        else:
            col.append(False)

        atual += 1 
        anterior += 1
        
    return df.assign(change_price=col)