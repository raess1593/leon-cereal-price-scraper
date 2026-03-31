"""Post-processing utilities for scraped cereal prices stored in SQLite."""

import pandas as pd
import numpy as np
from database import engine

def clean_impute_db():
    """Create a cleaned table by replacing zeros and interpolating missing values."""

    df = pd.read_sql("SELECT * FROM crop_prices", engine)
    # Skip date column and process only numeric price features.
    for c in df.columns[1:]:
        na_cond = df[c] == 0
        # In this dataset, zero is treated as missing for price columns.
        df[c] = np.where(na_cond, np.nan, df[c])
        # Apply polynomial interpolation to preserve smooth market trends.
        df[c] = df[c].interpolate(method='polynomial', order=3).round(0)

    # Persist cleaned output as a separate table to keep raw data untouched.
    df.to_sql('crop_prices_clean', engine, if_exists='replace', index=False)


if __name__ == "__main__":
    clean_impute_db()