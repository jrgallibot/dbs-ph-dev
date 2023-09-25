from bs4 import BeautifulSoup
import requests
import json


def make_domainsfast_api_request(keyword, list_urls=None):
    base_url = "https://domainsfast.applikuapp.com"
    username, password = ('fastdatabasedseo', '@Fastdatabasedseo123')

    headers = {"accept": "application/json", "Content-Type": "application/json"}
    auth = (username, password)

    try:
        topics = requests.post(f"{base_url}/topics", headers=headers, json={"keyword": keyword}, auth=auth).json()
        content_links = requests.post(f"{base_url}/generate_content_links", headers=headers, json={"keyword": keyword, "list_urls": list_urls}, auth=auth).json()
        article = return_article(topics)
        modified_article = modify_article(article, content_links)
        return modified_article
        
    except requests.RequestException as e:
        print(f"Request exception: {e}")


def return_article(data):
    base_url = "https://domainsfast.applikuapp.com"
    username, password = ('fastdatabasedseo', '@Fastdatabasedseo123')

    headers = {"accept": "application/json", "Content-Type": "application/json"}
    auth = (username, password)
    dataJson = {"data": json.dumps(data)}
    article = requests.post(f"{base_url}/return_article", headers=headers, json=dataJson, auth=auth).json()
    return article


def modify_article(article, content_links):
    soup = BeautifulSoup(article, 'html.parser')
    existing_paragraphs = soup.find_all('p')
    new_paragraphs = BeautifulSoup(content_links, 'html.parser').find_all('p')
    
    num_new_paragraphs = len(new_paragraphs)
    
    if num_new_paragraphs == 1:
        middle_position = len(existing_paragraphs) // 2
        existing_paragraphs[middle_position].insert_before(new_paragraphs[0])
    elif num_new_paragraphs == 2:
        top_position = len(existing_paragraphs) // 4
        end_position = 3 * len(existing_paragraphs) // 4
        existing_paragraphs[top_position].insert_before(new_paragraphs[0])
        existing_paragraphs[end_position].insert_before(new_paragraphs[1])
    else:
        third = num_new_paragraphs // 3
        top_paragraphs = new_paragraphs[:third]
        middle_paragraphs = new_paragraphs[third:2*third]
        end_paragraphs = new_paragraphs[2*third:]
        if num_new_paragraphs % 3 != 0:
            middle_paragraphs.append(new_paragraphs[-1])

        def insert_paragraphs(existing_paragraphs, new_paragraphs, positions):
            for idx, new_p in enumerate(new_paragraphs):
                insert_position = positions[idx % len(positions)]
                existing_paragraphs[insert_position].insert_before(new_p)

        top_positions = list(range(1, len(existing_paragraphs) // 3))
        middle_positions = list(range(len(existing_paragraphs) // 3, 2 * len(existing_paragraphs) // 3))
        end_positions = list(range(2 * len(existing_paragraphs) // 3, len(existing_paragraphs)))

        insert_paragraphs(existing_paragraphs, top_paragraphs, top_positions)
        insert_paragraphs(existing_paragraphs, middle_paragraphs, middle_positions)
        insert_paragraphs(existing_paragraphs, end_paragraphs, end_positions)
    
    header = soup.find('h1').get_text()
    return {'header': header, 'body': soup.prettify()}