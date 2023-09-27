from bs4 import BeautifulSoup
import concurrent.futures
import requests
import json


base_url = "https://domainsfast.applikuapp.com"
username, password = ('fastdatabasedseo', '@Fastdatabasedseo123')

headers = {"accept": "application/json", "Content-Type": "application/json"}
auth = (username, password)


def make_domainsfast_api_request(keyword, list_urls=None):
    
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the functions for execution
            topics_future = executor.submit(get_topics, keyword, list_urls)
            content_links_future = executor.submit(generate_content_links, keyword, list_urls)

            # Wait for both requests to complete
            concurrent.futures.wait([topics_future, content_links_future])

        # Get the results from the futures
        topics_result = topics_future.result()
        content_links_result = content_links_future.result()
        article = return_article(topics_result)  
        modified_article = modify_article(article, content_links_result)
        return modified_article
    except requests.RequestException as e:
        print(f"Request exception: {e}")


def get_topics(keyword, list_urls):
    response = requests.post(f"{base_url}/topics", headers=headers, json={"keyword": keyword}, auth=auth)
    return response.json()


def generate_content_links(keyword, list_urls):
    response = requests.post(f"{base_url}/generate_content_links", headers=headers, json={"keyword": keyword, "list_urls": list_urls}, auth=auth)
    return response.json()


def return_article(data):
    print(isinstance(data, dict))
    dataJson = {"data": json.dumps(data)} if isinstance(data, dict) else {"data": json.dumps(data, safe=False)}
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