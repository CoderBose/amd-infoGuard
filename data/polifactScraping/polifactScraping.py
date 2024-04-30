import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

class PolitiFactArticleScraper:
    base_url = "https://www.politifact.com/article/"

    def __init__(self):
        self.session = requests.Session()

    def generate_page_url(self, page):
        return f"{self.base_url}?page={page}"

    def get_articles_info(self, page=1):
        page_url = self.generate_page_url(page)
        response = self.session.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('div', class_='m-teaser')
            articles_info = []
            for article in articles:
                title = article.find('h3', class_='m-teaser__title').text.strip()
                date = article.find('div', class_='m-teaser__meta').text.strip().split('•')[1].strip()
                author = article.find('div', class_='m-teaser__meta').text.strip().split('•')[0].strip()
                if author.startswith("By "):
                    author = author[3:] 
                article_url = article.find('a')['href']
                full_article_url = urljoin(self.base_url, article_url)  # Each page has 20 articles, so we need to construct urls by modifying the page number param
                # getting the author from the main page, because inside the articles they are placed in a different div - easier from main page
                articles_info.append({'title': title, 'date': date, 'author': author, 'url': full_article_url})
            return articles_info
        else:
            print("Failed to retrieve article information. Status code:", response.status_code)
            return []

    def scrape_article_data(self, article_url):
        response = self.session.get(article_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_title = soup.find('h1', class_='m-statement__quote').text.strip()
            tags = [tag.text.strip() for tag in soup.find_all('a', class_='c-tag')]
            author = soup.find('div', class_='m-author__wrap').find('a').text.strip() if soup.find('div', class_='m-author__wrap') else ""
            paragraphs = soup.find('article', class_='m-textblock').find_all('p')
            text = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
            return {'title': article_title, 'author': author, 'tags': tags, 'text': text}
        else:
            print("Failed to retrieve article data from URL:", article_url)
            return {}

    def scrape_and_save_articles(self, filename, start_page=1, end_page=None):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Date', 'Author', 'Tags', 'Text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for page in range(start_page, end_page+1) if end_page else range(start_page, float('inf')):
                articles_info = self.get_articles_info(page)
                if not articles_info:
                    break
                for article in articles_info:
                    article_data = self.scrape_article_data(article['url'])
                    writer.writerow({'Title': article['title'], 'Date': article['date'],
                                     'Author': article.get('author', ''), 'Tags': ", ".join(article_data.get('tags', [])),
                                     'Text': article_data.get('text', '')})
                    print("Article scraped from page", page, ":", article['title'])
        print("Articles scraped and saved to", filename)


scraper = PolitiFactArticleScraper()
scraper.scrape_and_save_articles("politifact_articles.csv", start_page=1, end_page=5)
