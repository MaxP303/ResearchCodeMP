import pandas as pd
import numpy as np
from itertools import combinations

output_file = r'D:\Documents\ThesisD\Cronbach_trimmed_datafinal2.csv'

# Load the data
df = pd.read_csv(r"D:\Documents\ThesisD\Cronbach_trimmed_datafinal.csv")

# Define the categories and word columns
categories = {
    'Network & Community': ['campaign', 'platform', 'third-party'],
    'Customer Engagement': ['custom', 'engage', 'platform'],
    'Partnership & Joint Venture Activities': ['property', 'partnership', 'joint venture', 'partner'],
    'Industry-Academia Collaboration': ['institute', 'education', 'author', 'education program'],
    'Contracts & IP Licensing': ['license', 'agreement', 'patent', 'collaborate', 'grant'],
    'Bilateral Transactional Activities': ['franchise', 'agreement', 'franchisee', 'license'],
    'Smarter Use and Make': ['refuse', 'rethink', 'reduce'],
    'Extend Lifespan': ['re-use', 'repair', 'refurbish', 'remanufacture', 'repurpose'],
    'Useful Materials': ['recycle', 'recover']
}

# Categories contributing to total_oi and total_ce
total_oi_categories = [
    'Network & Community', 'Customer Engagement', 'Partnership & Joint Venture Activities', 
    'Industry-Academia Collaboration', 'Contracts & IP Licensing', 'Bilateral Transactional Activities'
]

total_ce_categories = [
    'Smarter Use and Make', 'Extend Lifespan', 'Useful Materials'
]

def cronbach_alpha(df, items):
    item_scores = df[items]
    item_variances = item_scores.var(axis=0, ddof=1)
    total_score_variance = item_scores.sum(axis=1).var(ddof=1)
    
    n_items = len(items)
    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_score_variance)
    
    return alpha

# Display initial Cronbach's Alpha scores for total_oi and total_ce
initial_alpha_oi = cronbach_alpha(df, total_oi_categories)
initial_alpha_ce = cronbach_alpha(df, total_ce_categories)

print(f"Initial Cronbach's Alpha for total_oi: {initial_alpha_oi:.4f}")
print(f"Initial Cronbach's Alpha for total_ce: {initial_alpha_ce:.4f}\n")

def optimize_cronbach_alpha(df, categories, word_columns):
    original_alpha = cronbach_alpha(df, categories)
    best_options = [(original_alpha, "Original categories", [])]

    # Iterate through each category
    for category in categories:
        words = word_columns[category]
        # Explore all possible combinations of word removals except removing all words
        for drop_count in range(1, len(words)):
            for word_comb in combinations(words, drop_count):
                temp_df = df.copy()
                for word in word_comb:
                    temp_df[category] -= df[word]
                current_alpha = cronbach_alpha(temp_df, categories)
                best_options.append((current_alpha, f"Drop {', '.join(word_comb)} from '{category}'", list(word_comb)))

    # Sort and return the best five options
    best_options = sorted(best_options, key=lambda x: x[0], reverse=True)[:5]
    
    return best_options

# Optimize for total_oi
best_options_oi = optimize_cronbach_alpha(df, total_oi_categories, categories)
print(f"Best five options for total_oi:")
for alpha, description, removed_words in best_options_oi:
    print(f"Alpha: {alpha:.4f}, Description: {description}")

# Optimize for total_ce
best_options_ce = optimize_cronbach_alpha(df, total_ce_categories, categories)
print(f"\nBest five options for total_ce:")
for alpha, description, removed_words in best_options_ce:
    print(f"Alpha: {alpha:.4f}, Description: {description}")

# Assuming you choose the best option (highest alpha) for both total_oi and total_ce
chosen_words_to_remove = {
    'total_oi': best_options_oi[0][2],
    'total_ce': best_options_ce[0][2]
}

# Remove the chosen words from the DataFrame
for word in chosen_words_to_remove['total_oi']:
    for category in total_oi_categories:
        if word in categories[category]:
            df[category] -= df[word]
            df.drop(columns=[word], inplace=True)

for word in chosen_words_to_remove['total_ce']:
    for category in total_ce_categories:
        if word in categories[category]:
            df[category] -= df[word]
            df.drop(columns=[word], inplace=True)

# Recalculate the total_oi and total_ce after word removal
df['total_oi'] = df[total_oi_categories].sum(axis=1)
df['total_ce'] = df[total_ce_categories].sum(axis=1)

# Save the modified DataFrame to a new CSV file

df.to_csv(output_file, index=False)
print(f"\nModified data saved to {output_file}")
