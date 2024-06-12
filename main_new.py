import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from uniter import remote_call

def get_page_data(url):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(10)  # Увеличение времени ожидания для полной загрузки страницы

        title = driver.title

        try:
            meta_description = driver.find_element(By.NAME, "description").get_attribute("content")
        except:
            meta_description = ''
        
        try:
            meta_keywords = driver.find_element(By.NAME, "keywords").get_attribute("content")
        except:
            meta_keywords = ''
        
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for element in elements:
                headings.append(element.text)
        
    except WebDriverException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        title = "Ошибка при загрузке страницы"
        meta_description = ""
        meta_keywords = ""
        headings = ""
    finally:
        driver.quit()
    
    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "meta_keywords": meta_keywords,
        "headings": " ".join(headings)
    }

def main(urls):
    data = []
    counter = 0
    for url in urls:
        print(counter, "/", len(urls))
        page_data = get_page_data(url)
        data.append(page_data)
        counter+=1
    print(counter, "/", len(urls))
    
    with open('parsed_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    remote_call()

if __name__ == "__main__":
    urls = [
        "https://colizeumarena.com/blog/club/colizeum-irkutsk/",
        "https://cyberxcommunity.ru/clubs/",
    ]
    
    main(urls)
