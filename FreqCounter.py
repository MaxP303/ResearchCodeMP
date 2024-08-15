import pandas as pd
import multiprocessing
from tqdm import tqdm
from nltk.stem import PorterStemmer
import re
import logging

# Configure logging
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Specify the input and output file paths
input_csv = r'D:\Documents\ThesisD\full_datafinal.csv'
output_csv = r'D:\Documents\ThesisD\counted_datafinal2.csv'

# Specify the column that contains the text
text_column = 'text'

# Define the predefined words and their translations
predefined_words = {
    'campaign': ['campaign', 'Kampagne', 'Campagne', 'Campagne'],
    'platform': ['platform', 'Plattform', 'Plateforme', 'Platform'],
    'third-party': ['third-party', 'third party', 'Drittpartei', 'Tiers', 'derde partij'],
    'custom': ['custom', 'individuell angefertigt', 'personnalisé', 'aangepast'],
    'engage': ['engage', 'engagieren', 'engager', 'betrokkenheid'],
    'property': ['property', 'Eigentum', 'propriété', 'eigendom'],
    'partnership': ['partnership', 'Partnerschaft', 'partenariat', 'partnerschap'],
    'joint venture': ['joint venture', 'Joint Venture', 'joint-venture', 'joint ventur'],
    'partner': ['partner', 'Partner', 'partenaire', 'partner'],
    'institute': ['institute', 'Institut', 'institut', 'instituut'],
    'education': ['education', 'Bildung', 'éducation', 'onderwijs'],
    'author': ['author', 'Autor', 'auteur', 'auteur'],
    'education program': ['education program', 'Bildungsprogramm', 'programme d\'éducation', 'onderwijsprogramma'],
    'license': ['license', 'Lizenz', 'licence', 'licentie'],
    'agreement': ['agreement', 'Vereinbarung', 'accord', 'overeenkomst'],
    'patent': ['patent', 'Patent', 'brevet', 'octrooi'],
    'collaborate': ['collaborate', 'zusammenarbeiten', 'collaborer', 'samenwerken'],
    'grant': ['grant', 'Gewährung', 'subvention', 'subsidie'],
    'franchise': ['franchise', 'Franchise', 'franchise', 'franchise'],
    'franchisee': ['franchisee', 'Franchisenehmer', 'franchisé', 'franchisenemer'],
    'refuse': ['refuse', 'ablehnen', 'refuser', 'weigeren'],
    'rethink': ['rethink', 'überdenken', 'repenser', 'heroverwegen'],
    'reduce': ['reduce', 'reduzieren', 'réduire', 'verminderen'],
    're-use': ['re-use', 'reuse', 'wiederverwenden', 'réutiliser', 'hergebruiken'],
    'repair': ['repair', 'reparieren', 'réparer', 'repareren'],
    'refurbish': ['refurbish', 'aufarbeiten', 'réhabiliter', 'opknappen'],
    'remanufacture': ['remanufacture', 'remanufacturieren', 'remanufacturer', 'remanufactureren'],
    'repurpose': ['repurpose', 'umfunktionieren', 'réaffecter', 'herbestemmen'],
    'recycle': ['recycle', 'recyceln', 'recycler', 'recyclen'],
    'recover': ['recover', 'wiederherstellen', 'récupérer', 'herstellen']
}

# Define the categories and map predefined words to their categories
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

# Define exclusion patterns for specific words
exclusion_patterns = {
    'reduce': ['reduce cost', 'reduce costs', 'reduce value', 'reduce time', 'Kosten senken', 'réduire les coûts', 'kosten verlagen', 'Wert mindern', 'réduire la valeur', 'waarde verminderen', 'Zeit reduzieren', 'réduire le temps', 'tijd verminderen']  # Add more exclusions as needed
}

# Initialize the Porter stemmer
stemmer = PorterStemmer()

# Function to stem words using Porter stemmer
def stem_word(word):
    return stemmer.stem(word)

# Create a dictionary of stemmed predefined words with duplicate removal
flat_predefined_words = {}
for word, translations in predefined_words.items():
    stemmed_translations = list(set(stem_word(translation) for translation in translations))
    flat_predefined_words[word] = stemmed_translations

# Function to remove excluded phrases from text
def remove_exclusions(text, exclusions):
    for word, phrases in exclusions.items():
        for phrase in phrases:
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            text = pattern.sub('', text)
    return text

# Function to analyze word frequencies for all predefined words
def word_frequencies(text, word_list, exclusions):
    if isinstance(text, str):  # Check if text is a string
        text = remove_exclusions(text, exclusions)  # Remove excluded phrases
        frequencies = {word: 0 for word in word_list}
        for word, translations in word_list.items():
            for translation in translations:
                pattern = re.compile(r'\b' + re.escape(translation) + r'\b', re.IGNORECASE)
                frequencies[word] += len(pattern.findall(text))
        return frequencies
    else:
        return {word: 0 for word in word_list}  # Return zero count for each word if text is not a string

# Define a function to process rows
def process_row(row_dict, word_list, exclusions):
    return word_frequencies(row_dict[text_column], word_list, exclusions)

if __name__ == '__main__':
    # Allow the user to specify the number of CPU cores to use
    num_cores = multiprocessing.cpu_count()
    num_processes = min(9, num_cores)  # Limit to 9 processes or CPU count, whichever is lower

    # Batch size for processing
    chunk_size = 1000  # Adjust based on memory and performance testing

    with multiprocessing.Pool(num_processes) as pool, open(output_csv, 'w', newline='', encoding='utf-8') as f_out:
        # Write the header to the output CSV
        header = 'ID,total_oi,total_ce,' + ','.join(categories.keys()) + ',' + ','.join(predefined_words.keys()) + '\n'
        f_out.write(header)

        # Get the total number of rows to provide an accurate progress bar
        total_rows = sum(1 for _ in open(input_csv, encoding='utf-8')) - 1  # Specify the encoding

        chunk_iter = pd.read_csv(input_csv, usecols=['ID', 'text'], chunksize=chunk_size, encoding='utf-8')
        for chunk in tqdm(chunk_iter, total=total_rows//chunk_size, desc="Processing chunks"):
                row_dicts = chunk.to_dict('records')
                ids = chunk['ID'].tolist()

                # Process each chunk
                chunk_frequencies = list(pool.starmap(process_row, [(row_dict, flat_predefined_words, exclusion_patterns) for row_dict in row_dicts]))

                # Write the frequencies for the current chunk to the output file
                for i, freq_dict in enumerate(chunk_frequencies):
                    total_oi = sum(freq_dict.get(word, 0) for category in list(categories.values())[:6] for word in category)
                    total_ce = sum(freq_dict.get(word, 0) for category in list(categories.values())[6:] for word in category)

                    # Skip writing the row if both total_oi and total_ce are zero
                    if total_oi == 0 and total_ce == 0:
                        continue

                    # Prepare the line to write to output CSV
                    line = f"{ids[i]},{total_oi},{total_ce},"

                    # Iterate through categories and calculate sum of frequencies
                    for category in categories.values():
                        category_freq = sum(freq_dict.get(word, 0) for word in category)
                        line += f"{category_freq},"

                    # Append frequencies for predefined words
                    for word in predefined_words.keys():
                        word_freq = freq_dict.get(word, 0)
                        line += f"{word_freq},"

                    # Remove the trailing comma and add a newline character
                    line = line.rstrip(',') + '\n'

                    # Write the line to the output file
                    f_out.write(line)

        # Log the completion of processing
        logging.info("Processing completed successfully.")
        print('Completed!')

