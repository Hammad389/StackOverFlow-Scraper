# StackOverFlow Scraper
StackOverflow scraper that selectively extracts verified and highly voted questions and answers from the StackOverflow website and saves it in a sqlite3 database file in as title and code along with the source url of each question. 

# License
This project is licensed under the MIT License.

## Features

- Selectively scrapes verified and high voted questions and answers from StackOverflow.
- Maintains records of processed questions to avoid duplication.
- Keeps track of scraped pages for efficient resumption of scraping.
- Utilizes JSON files for storing records and data persistence.

## Screenshots
<a href="https://github.com/Hammad389/StackOverFlow-Scraper/blob/main/README_ASSETS/database.png">
<img src="https://github.com/Hammad389/StackOverFlow-Scraper/blob/main/README_ASSETS/database.png" />
</a>
<a href="https://github.com/Hammad389/StackOverFlow-Scraper/blob/main/README_ASSETS/scraped_questions_ids.png">
<img src="https://github.com/Hammad389/StackOverFlow-Scraper/blob/main/README_ASSETS/scraped_questions_ids.png" />
</a>


## Usage

1. Clone the repository:

```bash
git clone https://github.com/Hammad389/stackoverflow-scraper.git
```

2. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python scraper.py
```



