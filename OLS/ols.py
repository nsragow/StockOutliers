import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.api import OLS,add_constant


def get_outliers(target, predictors):
    model = OLS(target,add_constant(predictors)).fit()
    return model

#predictors must be in correct order
def predictions(df,predictors,target,model):

    predictors = add_constant(df.loc[:,predictors].values)
    predictions = model.predict(predictors)
    target = df.loc[:,target]
    resids = target - predictions
    z_resids = (resids-resids.mean())/resids.std()

    culmative = list(map(stats.norm.cdf,z_resids))
    to_return = df.copy()
    to_return["cdf"] = culmative
    to_return["resid"] = resids
    to_return = to_return.loc[:,["cdf","resid"]]
    to_return = to_return.sort_values(by="cdf")



    return to_return,resids.std(),model
def get_outliers(resid_df,cutoff = .05):
    return resid_df[(resid_df.cdf > (1-cutoff)) | (resid_df.cdf < cutoff)]
def graph_residuals(resid_df,cutoff = .05):
    outliers = get_outliers(resid_df,cutoff)
    norm = resid_df.drop(outliers.index)
    plt.scatter(y=norm.resid,x=range(norm.shape[0]))
    plt.scatter(y=outliers.resid,x=range(outliers.shape[0]),color="red")

#what is the formula for rsquared? How can I relate it to if a stock is an outlier?
