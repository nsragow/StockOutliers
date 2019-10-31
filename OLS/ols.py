import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.api import OLS,add_constant

def run(df,target,predictors,cutoff=.05):
    target_df = df[target]
    predictors_df = df[predictors]
    model = get_model(target_df,predictors_df)
    bad_predictors = get_high_p(model)
    for bad_pred in bad_predictors:
        predictors.remove(bad_pred)
    target_df = df[target]
    predictors_df = df[predictors]
    model = get_model(target_df,predictors_df)

    resid_df,std = predictions(df,target,predictors,model)
    outliers = get_outliers(resid_df,cutoff)
    graph_residuals(resid_df,model.rsquared,cutoff)

    return model,outliers,resid_df

def get_high_p(model):
    bads = []
    for pval in model.pvalues.index:

        if model.pvalues[pval] > .05:
            bads.append(pval)
    return bads

def get_model(target, predictors):
    model = OLS(target,add_constant(predictors)).fit()
    return model

#predictors must be in correct order
def predictions(df,target,predictors,model):
    predictors = add_constant(df.loc[:,predictors].values)
    predictions = model.predict(predictors)
    target = df.loc[:,target]
    resids = target - predictions
    z_resids = (resids-resids.mean())/resids.std()

    culmative = list(map(stats.norm.cdf,z_resids))
    resid_df = df.copy()
    resid_df["cdf"] = culmative
    resid_df["resid"] = resids
    resid_df = resid_df.loc[:,["cdf","resid"]]



    return resid_df,resids.std()
def get_outliers(resid_df,cutoff = .05):
    return resid_df[(resid_df.cdf > (1-cutoff)) | (resid_df.cdf < cutoff)]
def graph_residuals(resid_df,rsquared,cutoff = .05):
    outliers = get_outliers(resid_df,cutoff).index
    colors = resid_df.apply(lambda row : "red" if row.name in outliers else "blue",axis=1)
    fig,ax = plt.subplots()

    ax.set_title(f"rsquared:{rsquared}")
    ax.set_ylabel("Residual")

    sns.lineplot(y=[0]*resid_df.shape[0],x=range(resid_df.shape[0]),color="black",ax=ax)
    ax.scatter(y=resid_df.resid,x=range(resid_df.shape[0]),color=colors)


    plt.show()

#what is the formula for rsquared? How can I relate it to if a stock is an outlier?


























def how_many_tens(int_list):
    count = 0
    for i in range(len(int_list)):
        for j in range(len(int_list)):
            if int_list[i]+int_list[j] == 10:
                if i != j:
                    count+=1
    return count/2
