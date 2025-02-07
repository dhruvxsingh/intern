# Scrapy and Flask Project


This project serves as an example of using **Scrapy** to scrape data from a website and then display the results using a **Flask** web application. In addition, there are various Python scripts to perform additional tasks, from data processing to interacting with APIs.

### Key Features

- **Scrapy** for scraping data from websites.
- **Flask** web application for displaying scraped data on the frontend.
- Python code for data analysis and processing.
- Easy-to-follow setup and deployment instructions.

## Installation

Follow these steps to get the project running:

### 1. Clone the repository:

   ```bash
   git clone https://github.com/dhruvxsingh/intern.git
   cd intern 
   ```


### 2. Install all package in window:

   ```bash
   pip install -r requirements.txt
```

### 3.  Run web scrapy:

   ```bash
  scrapy crawl properties -o output.json
  ```

  ### 5.  Run API:

   ```bash
  python .\api.py
  ```

The application will be available at http://127.0.0.1:8080.

 ### We have routes:
 1. http://127.0.0.1:8080/post :  
 2. http://127.0.0.1:8080/pdf :
 3. http://127.0.0.1:8080/brochure-data?property=xyz :
 4. http://127.0.0.1:8080/properties :
 5. http://127.0.0.1:8080/brochure-fulldata :
 6. http://127.0.0.1:8080/full-details?property=xyz :

### Render link:
1. https://intern-6noc.onrender.com/ :
2. https://intern-6noc.onrender.com/pdf :
3. https://intern-6noc.onrender.com/properties :


