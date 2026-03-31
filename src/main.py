from scraper import ScraperBot
from process import clean_data

from database import Base, SessionLocal, engine
from models import CropPrice

import datetime

def look_for_valid_day(current_date, bot, dom, limit):
    """Find the nearest previous date with a valid table response."""

    for i in range(limit):
        day = current_date - datetime.timedelta(days=i)
        day_str = day.strftime("%d-%m-%Y")
        url = f"{dom}{day_str}"
        
        try:
            raw_data = bot.extract_raw(url)
            if raw_data:
                return day
        except:
            continue 
    raise TimeoutError         

def scrap_day(current_date, bot, dom):
    """Scrape and normalize a single market day payload."""

    day_str = current_date.strftime("%d-%m-%Y")
    url = dom + day_str
        
    try:
        raw_data = bot.extract_raw(url)
        cleaned_data = clean_data(raw_data)
        cleaned_data['date'] = current_date
        return cleaned_data
    
    except:
        raise KeyError

def save_data(db, all_scraped_data):
    """Persist a batch of normalized rows into SQLite."""

    try:
        for row in all_scraped_data:
            new_item = CropPrice(
                date = row.get('date'),
                feed_wheat = row.get("feed_wheat", 0),
                barley = row.get("barley", 0),
                triticale = row.get("triticale", 0),
                rye = row.get("rye", 0),
                oats = row.get("oats", 0),
                corn = row.get("corn", 0)
            )
            db.add(new_item)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == "__main__":
    print("Initializing bot...")

    # Ensure schema exists before ingesting new observations.
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    current_date = db.query(CropPrice.date).all()[0][0] - datetime.timedelta(days=1)
    
    bot = ScraperBot()
    doms = {1: "https://www.lonjadeleon.es/lonja-de-cereal-",
            2: "https://www.lonjadeleon.es/lonja-de-cereales-",
            3: "https://www.lonjadeleon.es/lonja-cereales-",}
    dom = doms[2]

    # Incremental backfill target for this execution.
    all_scraped_data = []
    new_items = 200

    while len(all_scraped_data) < new_items:
        try:
            all_scraped_data.append(scrap_day(current_date, bot, dom))
            print(f"Bot scrapped: {current_date}")
            print(f"\tTotal new items scrapped: {len(all_scraped_data)}")
            print()
            
            current_date -= datetime.timedelta(days=7)

        except:
            found = False
            # Prioritize current working domain, then test alternatives.
            ordered_doms = [dom] + [doms[i] for i in [1, 2, 3] if dom != doms[i]]

            # Search first in a short local window, then widen the lookback.
            for start, end in zip([0, 8], [9, 25]):
                for d in ordered_doms:
                    try:
                        current_date = look_for_valid_day(current_date - datetime.timedelta(days=start), bot, d, end)
                        dom = d
                        found = True
                        break
                    except Exception:
                        continue
                if found: break
            if not found: break

    bot.close()
    
    if all_scraped_data:
        save_data(db, all_scraped_data)
        
    db.close()