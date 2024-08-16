import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.plotting import table

# Load the data
file_path = r"D:\Documents\ThesisD\Cronbach_trimmed_datafinal.csv"
data = pd.read_csv(file_path)

# Define the OI and CE columns
oi_columns = ['Network & Community', 'Customer Engagement', 'Partnership & Joint Venture Activities',
              'Industry-Academia Collaboration', 'Contracts & IP Licensing',
              'Bilateral Transactional Activities']

ce_columns = ['Smarter Use and Make', 'Extend Lifespan', 'Useful Materials']

# Add a constant to the OI columns
X_multi = sm.add_constant(data[oi_columns])

# Initialize a DataFrame to store the results in matrix format
results_matrix = pd.DataFrame(index=oi_columns, columns=ce_columns)  # Exclude "Constant"

# Loop over each CE category and run the regression
for ce_category in ce_columns:
    y_multi = data[ce_category]
    model_robust_multi = sm.OLS(y_multi, X_multi).fit(cov_type='HC3')
    
    # Extract the regression results and format them
    for var in oi_columns:  # Only include OI variables, not the constant
        coef = model_robust_multi.params[var]
        p_value = model_robust_multi.pvalues[var]
        if p_value < 0.05:
            results_matrix.at[var, ce_category] = f"{coef:.4f}***"
        else:
            results_matrix.at[var, ce_category] = f"{coef:.4f}"

# Save the summary as a PNG image
fig, ax = plt.subplots(figsize=(12, 8))  # Adjust size as needed
ax.axis('tight')
ax.axis('off')
tbl = table(ax, results_matrix, loc='center', cellLoc='center', colWidths=[0.15]*len(results_matrix.columns))
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)  # Increased font size
tbl.scale(1.5, 1.5)  # Increased scaling for better readability

plt.savefig(r"D:\Documents\ThesisD\MultipleRegressionMatrix.png", bbox_inches='tight', dpi=300)
plt.close()

print("Multiple regression summary matrix saved to 'MultipleRegressionMatrix.png'")
