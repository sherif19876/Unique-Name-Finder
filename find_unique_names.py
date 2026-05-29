import pandas as pd

# ----------------------------------------------------------------------
# Configuration - adjust file paths and column names as needed
# ----------------------------------------------------------------------
CLASSIFIED_FILE = "names_unique_to_each_file.csv"   # Reference set of known names
UNCLASSIFIED_FILE = "unknown_names_new.csv"         # Set of names to filter
OUTPUT_FILE = "missingWA.csv"                       # Names in unclassified but not in classified

# Column name containing names in both input files (can be changed)
NAME_COLUMN = "Mohamed"
# ----------------------------------------------------------------------

def clean_name(name):
    """
    Standardize a name string for comparison:
    - Convert to string (handles NaN)
    - Lowercase
    - Strip leading/trailing whitespace
    - Replace multiple internal spaces with a single space
    """
    if pd.isna(name):
        return ""
    # Convert to string, lowercase, strip, then split/join to normalize spaces
    return ' '.join(str(name).strip().lower().split())

def main():
    print("Loading classified names file...")
    # Read only the first column (assumed to contain names)
    classified_df = pd.read_csv(CLASSIFIED_FILE, usecols=[0])
    print(f"  Loaded {len(classified_df)} rows from {CLASSIFIED_FILE}")

    print("Loading unclassified names file...")
    unclassified_df = pd.read_csv(UNCLASSIFIED_FILE, usecols=[0])
    print(f"  Loaded {len(unclassified_df)} rows from {UNCLASSIFIED_FILE}")

    # Standardize column names to a known value for easy reference
    classified_df.columns = [NAME_COLUMN]
    unclassified_df.columns = [NAME_COLUMN]

    # Apply cleaning to both DataFrames
    classified_df['clean_name'] = classified_df[NAME_COLUMN].apply(clean_name)
    unclassified_df['clean_name'] = unclassified_df[NAME_COLUMN].apply(clean_name)

    # Create sets of cleaned names for efficient set difference
    classified_set = set(classified_df['clean_name'])
    unclassified_set = set(unclassified_df['clean_name'])

    # Find cleaned names that appear only in the unclassified set
    unique_clean_names = unclassified_set - classified_set
    print(f"Found {len(unique_clean_names)} unique cleaned names not in classified set")

    # Recover the original (uncleaned) names from the unclassified DataFrame
    # that correspond to those unique cleaned names
    unique_original = unclassified_df[unclassified_df['clean_name'].isin(unique_clean_names)]

    # Drop duplicate original names (in case multiple rows had same cleaned name)
    unique_original = unique_original[[NAME_COLUMN]].drop_duplicates()

    # Save to output CSV
    unique_original.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(unique_original)} unique original names to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
