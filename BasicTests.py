import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from sklearn.preprocessing import StandardScaler

# Load the data
file_path = r"D:\Documents\ThesisD\Cronbach_trimmed_datafinal.csv"
data = pd.read_csv(file_path)

# Open a file to save the results
with open(r"D:\Documents\ThesisD\BasicTests.txt", 'w') as file:

    # 1. General Descriptives
    descriptives = data.describe()
    file.write("General Descriptives:\n")
    file.write(descriptives.to_string())
    file.write("\n\n")

    # 2. Reliability (Cronbach’s Alpha for OI and CE separately)
    def cronbach_alpha(df):
        df_standardized = StandardScaler().fit_transform(df)  # standardize data
        n_items = df.shape[1]
        variances = np.var(df_standardized, axis=0, ddof=1)
        total_variance = np.var(df_standardized.sum(axis=1), ddof=1)
        alpha = n_items / (n_items - 1) * (1 - variances.sum() / total_variance)
        return alpha

    oi_columns = ['Network & Community', 'Customer Engagement', 'Partnership & Joint Venture Activities',
                  'Industry-Academia Collaboration', 'Contracts & IP Licensing',
                  'Bilateral Transactional Activities']

    ce_columns = ['Smarter Use and Make', 'Extend Lifespan', 'Useful Materials']

    #cronbach_alpha_oi = cronbach_alpha(data[oi_columns])
    #cronbach_alpha_ce = cronbach_alpha(data[ce_columns])

    #file.write(f"Cronbach's Alpha for OI: {cronbach_alpha_oi}\n")
    #file.write(f"Cronbach's Alpha for CE: {cronbach_alpha_ce}\n\n")

    # 3. Spearman's Rank Correlation
    # Between total_OI and total_CE
    spearman_total = spearmanr(data['total_oi'], data['total_ce'])
    file.write(f"Spearman's Rank Correlation between total_OI and total_CE: {spearman_total}\n\n")

    # Between OI categories and CE categories, as well as their respective constructs
    spearman_categories = data[oi_columns + ce_columns].corr(method='spearman')
    file.write("Spearman's Rank Correlation between OI categories and CE categories:\n")
    file.write(spearman_categories.to_string())
    file.write("\n\n")

    # 4. Regression using robust errors (total_oi predicting total_ce)
    X_single = data[['total_oi']]
    X_single = sm.add_constant(X_single)
    y_single = data['total_ce']

    model_robust = sm.OLS(y_single, X_single).fit(cov_type='HC3')
    file.write("Regression with Robust Errors:\n")
    file.write(model_robust.summary().as_text())
    file.write("\n\n")

    # Save the QQ plot as an image file
    sm.qqplot(model_robust.resid, line='s')
    plt.title('QQ Plot of Residuals')
    plt.savefig(r'D:\Documents\ThesisD\qq_plot_residuals.png')
    plt.close()

    file.write("QQ Plot of Residuals saved as 'qq_plot_residuals.png'.\n\n")

    # 5. Multicollinearity test (VIF)
    vif_single = pd.DataFrame()
    vif_single["VIF"] = [variance_inflation_factor(X_single.values, i) for i in range(X_single.shape[1])]
    vif_single["Variable"] = X_single.columns
    file.write("VIF Results:\n")
    file.write(vif_single.to_string())
    file.write("\n\n")

    # 6. Homoscedasticity test (Breusch-Pagan test)
    bp_test_single = het_breuschpagan(model_robust.resid, model_robust.model.exog)
    file.write("Breusch-Pagan Test Results (Chi-sq, p-value, F-value, F p-value):\n")
    file.write(f"{bp_test_single}\n\n")

    # 7. Autocorrelation test (Durbin-Watson test)
    dw_test_single = durbin_watson(model_robust.resid)
    file.write(f"Durbin-Watson Test Result: {dw_test_single}\n\n")

print("Analysis complete. Results saved")
