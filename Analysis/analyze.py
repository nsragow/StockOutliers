import pandas as pd

def remove_dups(df):
    df.drop(df[df.duplicated(df.columns)].index,axis=0,inplace=True)
def drop_not_found(df):
    df.drop(df[df.company_stock_symbol_according_to_yahoo== "Requested symbol wasn't found"].index,axis=0,inplace=True)

def get_dups(rows,df):
    return df.duplicated(subset=rows)
def get_multiples(col_name,df):
    return new_df[col_name].value_counts()[new_df[col_name].value_counts()>1]
def clean(df):
    for col in df.columns:
        if df[df[col].isna()==False].shape[0] == 0:
            df.drop(col,axis=1,inplace=True)
def not_full(df):
    full = df.shape[0]
    cols = []

    for col in df.columns:
        if df[df[col].isna()==False].shape[0] != full:
            cols.append(col)
    return cols
def zero_out(df,inplace=True):
    cols = not_full(df)
    for col in cols:
        if inplace:
            df[col].fillna(0,inplace=inplace)
        else:
            df = df[col].fillna(0,inplace=inplace)
    return df
def zeroes(df):
    cols = []

    for col in df.columns:
        if df[df[col]==0].shape[0]>0:
            cols.append(col)
    return cols
def process(df):
    clean(df)
    zero_out(df)
    remove_dups(df)
    drop_not_found(df)
    df.set_index("company_stock_symbol_according_to_yahoo",inplace=True)
    df.drop("interest_expense",axis=1,inplace=True)
    return df
def clean_corrs(corrs):
    indices = set()
    for ind in corrs.index:
        if ind[0] != ind[1]:
            toadd = (ind[0],ind[1]) if ind[0]>ind[1] else (ind[1],ind[0])
            indices.add(toadd)
    new_corrs = corrs[list(indices)].sort_values()
    neg = corrs<-0.7
    pos = corrs > .7
    return new_corrs[neg | pos]




df = process(pd.read_csv("../stock_data.csv"))
new_df = process(pd.read_csv("../new_stock_data.csv"))
