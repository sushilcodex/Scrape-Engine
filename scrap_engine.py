from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import csv


class ArticleScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._initialize_driver()
        self.post_links = []
        self.csv_path = "/home/codigo/Desktop/scrapping/post_links.csv"  # Absolute path to save CSV

    def _initialize_driver(self):
        options = Options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def _scroll_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)

    def _click_discover_more_until_done(self):
        while True:
            try:
                load_more_xpath = '//a[contains(@class, "rbc-more-posts-btn")]'
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, load_more_xpath))
                )
                load_more = self.driver.find_element(By.XPATH, load_more_xpath)
                self._scroll_to_element(load_more)
                self.driver.execute_script("arguments[0].click();", load_more)
                print("Clicked 'Discover More'")
                time.sleep(2)
            except (NoSuchElementException, TimeoutException):
                print("All posts loaded or no button found.")
                break

    def _collect_post_links(self):
        posts = self.driver.find_elements(By.XPATH, '//div[contains(@class, "rbc-media-card-col")]')
        print(f"Found {len(posts)} posts.")
        for post in posts:
            try:
                link = post.find_element(By.XPATH, './/a[contains(@class, "rbc-media-card-footer-link")]').get_attribute('href')
                self.post_links.append(link)
            except Exception as e:
                print(f"Failed to get link: {e}")

    def _save_all_links_to_csv(self):
        try:
            with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for link in self.post_links:
                    writer.writerow([link])
                print(f"Saved {len(self.post_links)} links to {self.csv_path}")
        except Exception as e:
            print(f"Failed to write CSV: {e}")

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            print("Driver closed.")

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(2)

        try:
            close_btn = self.driver.find_element(By.XPATH, '//button[contains(@class, "onetrust-close-btn-handler")]')
            close_btn.click()
            time.sleep(1)
        except Exception:
            pass

        self._click_discover_more_until_done()
        self._collect_post_links()
        self._save_all_links_to_csv()

    def process_post(self):
        if not os.path.exists(self.csv_path):
            print(f"CSV file not found at {self.csv_path}. Please run scrape() first.")
            return

        output_csv_path = os.path.join(os.getcwd(), "article_details.csv")

        try:
            with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file, \
                open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:

                reader = csv.reader(file)
                writer = csv.writer(output_file)
                writer.writerow(["Link", "Title", "Description", "Content"]) 

                for row in reader:
                    if not row:
                        continue
                    link = row[0]
                    print(f"\nProcessing article: {link}")
                    self.driver.get(link)
                    time.sleep(2)

                    try:
                        title = self.driver.find_element(By.XPATH, "//h1[@class='rbc-hero-title']").text
                    except:
                        title = "N/A"

                    try:
                        description = self.driver.find_element(By.XPATH, "//p[@class='rbc-hero-text']").text
                    except:
                        description = "N/A"

                    # Attempt to find the main content container
                    content_container = None
                    try:
                        content_container = self.driver.find_element(By.XPATH, "//div[@class='flex-grow-1']")
                    except:
                        try:
                            content_container = self.driver.find_element(By.XPATH, "//div[@class='col-lg-12']")
                        except:
                            print("No content container found.")

                    post_content = []

                    if content_container:
                        tags = content_container.find_elements(By.XPATH, ".//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6 | .//p | .//li")

                        for tag in tags:
                            tag_name = tag.tag_name

                            if tag_name == "li":
                                try:
                                    strong = tag.find_element(By.TAG_NAME, "strong")
                                    strong_text = strong.text.strip().rstrip(':')
                                    full_li_text = tag.text.strip()
                                    rest_text = full_li_text.replace(strong.text, '').strip(': ').strip()
                                    content = f"{strong_text}: {rest_text}" if rest_text else strong_text
                                    post_content.append(content)
                                except:
                                    text = tag.text.strip()
                                    if text:
                                        post_content.append(text)
                            else:
                                text = tag.text.strip()
                                if text:
                                    post_content.append(text)

                    full_text = "\n\n".join(post_content) if post_content else "N/A"

                    writer.writerow([link, title, description, full_text])
                    print("Article data saved.")

        except Exception as e:
            print(f"Error while reading CSV or processing posts: {e}")


            
if __name__ == "__main__":
    url = "https://www.brewin.co.uk/insights?topic=Market+news"
    scraper = ArticleScraper(url)
    try:
        scraper.scrape()
        scraper.process_post()
    finally:
        scraper.close_driver()
