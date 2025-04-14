import sys #for the argv
import os #for the path
import requests #for make http requests
from bs4 import BeautifulSoup #for parsing html if img div ..
import argparse 
#-r (boolean) for recursive exp: python3 Spider.py -r https://example.com also it can visit all the pages in this web
#-l (int) for limit exp: python3 Spider.py -l 5(defaul) https://example.com it is the limit of how much pages it can visit
#-p (string) let the user choose where to save the images deffault ./data/ 




def download(url, path):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            src = img.get('src')
            if src:
             
                if not src.startswith('http'):
                    src = requests.compat.urljoin(url, src)

             
                img_data = requests.get(src).content
                filename = os.path.join(path, os.path.basename(src))#path 

                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f"[+] Saved image: {filename}")
    except Exception as e:
        print(f"Error {url}: {e}")



def rec(url, path, visited, limit, current_depth=0):

    if url in visited or current_depth >= limit:
        return
    visited.add(url)

    download(url, path)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)

        for link in links:
            next_url = link['href']
            #if relative pass convert to absolute
            next_url = requests.compat.urljoin(url, next_url)
            if current_depth + 1 < limit:
                rec(next_url, path, visited, limit, current_depth + 1)

    except Exception as e:
        print(f" ERROR {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 Spider.py -r -l -p <url>")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Web Spider')
    parser.add_argument('-r', action='store_true', help='Recursive mode')
    parser.add_argument('-l', type=int, default=5, help='Limit of pages to visit')
    parser.add_argument('-p', type=str, default='./data/', help='Path to save images')
    parser.add_argument('url', type=str, help='URL to start the spider')

    args = parser.parse_args()
    url = args.url
    recursive = args.r
    limit = args.l
    path = args.p

    if not os.path.exists(path):
        os.makedirs(path)

    if not url.startswith('http'):
        print("Invalid URL")
        sys.exit(1)

    # print(f"URL: {url}")
    # print(f"Recursive mode: {recursive}")
    # print(f"Limit: {limit}")
    # print(f"Path: {path}")

    if recursive:
        visited = set() 
        rec(url, path, visited, limit)
    else:
        download(url, path)


if __name__ == "__main__":
    main()




