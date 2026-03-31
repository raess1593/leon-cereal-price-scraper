import re

def clean_price(price: list) -> float:
    """Convert the latest scraped cell value into a numeric float."""

    try:
        clean_value = price.pop()
        # Accept comma decimals and drop any non-numeric marker characters.
        clean_value = re.sub(r'[^0-9.]', '', clean_value.replace(',', '.'))
        return float(clean_value)
    except:
        # Keep ingestion resilient when a row is malformed or missing.
        return 0.0


def clean_data(raw_data: dict) -> dict:
    """Normalize scraped cereal labels so downstream mapping is consistent."""

    # Drop the multi-column table header row captured during scraping.
    try:
        raw_data.pop('CEREALES')
        raw_data.pop('\\xa0')
        raw_data.pop('€/t')
    except:
        pass

    # Remove marker symbols and standardize names for deterministic keys.
    for k in list(raw_data.keys()):
        cleaned_key = k.replace("*", "").strip().title()
        raw_data[cleaned_key] = raw_data.pop(k)
    
    # Remove units row and normalize accented key variant.
    try:
        raw_data.pop('')
    except:
        pass

    mapping = {
        "Trigo Pienso": "feed_wheat",
        "Cebada": "barley",
        "Triticale": "triticale",
        "Centeno": "rye",
        "Avena": "oats",
        "Maíz": "corn",
        "Maiz": "corn",
    }
    
    cleaned_data = {}

    for spa, eng in mapping.items():
        try:
            # Keep only the mapped cereal set expected by the database schema.
            cleaned_data[eng] = raw_data[spa]
        except KeyError:
            pass
    
    for k, v in cleaned_data.items():
        cleaned_data[k] = clean_price(v)
    return cleaned_data

if __name__ == "__main__":
    print(clean_data({'CEREALES': [' ', 'ANTERIOR', 'COTIZACION', ' ', 'ACTUAL'], '\xa0': ['€/t'], 'Trigo Pienso': ['200,00'], 'Cebada **': ['193,00'], 'Triticale': ['190,00'], 'Centeno': ['176,00'], 'Avena': ['145,00'], 'Maíz *': ['\xa0 213,00*']}
    ))
    print(clean_data({'CEREALES': ['ANTERIOR', 'COTIZACION', 'ACTUAL'], '\xa0': ['€/t'], 'Trigo Pienso': ['255,00'], 'Cebada **': ['238,00'], 'Triticale': ['240,00'], 'Centeno': ['240,00'], 'Avena': ['255,00'], 'Maíz': ['244,00']}))