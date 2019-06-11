import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.api import OLS,add_constant

def run(df,target,predictors):
    target_df = df[target]
    predictors_df = df[predictors]
    model = get_model(target_df,predictors_df)
    resid_df,std = predictions(df,target,predictors,model)
    outliers = get_outliers(resid_df)
    graph_residuals(resid_df,model.rsquared)

    return model,outliers,resid_df



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

    ax.scatter(y=resid_df.resid,x=range(resid_df.shape[0]),color=colors)

    plt.show()

#what is the formula for rsquared? How can I relate it to if a stock is an outlier?
