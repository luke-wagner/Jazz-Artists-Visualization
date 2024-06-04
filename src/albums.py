# For each artist's wiki, get the list of their albums and links to their respective pages
import csv
import requests
from bs4 import BeautifulSoup


with open('data/artists.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)

    with open('data/albums.csv', 'w') as out_file:
        out_file.write('Artist,Header,Relative Link,Full Link\n')
        for row in reader:
            print(row['Artist'], row['Link'])

            page = requests.get(row['Link'])
            soup = BeautifulSoup(page.content, "html.parser")

            headers = soup.find_all('h2')
            headers += soup.find_all('h3')

            album_headers = []

            for header in headers:
                if 'album' in header.text.lower():
                    album_headers.append(header)
            
            if album_headers == []:
                for header in headers:
                    if 'as leader' in header.text.lower():
                        album_headers.append(header)

            if album_headers == []:
                for header in headers:
                    if 'discography' in header.text.lower():
                        album_headers.append(header)

            #----------------------------------------------------------------------------
            # Get HTML blocks following each album header

            followingHTMLs = []
            
            for album_header in album_headers:
                html = u""
                for element in album_header.next_siblings:
                    if element.name == "h2" or element.name == "h3":
                        break
                    else:
                        html += str(element)

                followingHTMLs.append(html)

            #----------------------------------------------------------------------------
            # Get all links in each album header

            followingLinks = [] # 2 dimensional array

            for html in followingHTMLs:
                links = [] # 1 dimensional array, all the links associated with this html block
                childSoup = BeautifulSoup(html, "html.parser")
                for link_item in childSoup.find_all('a'):
                    link = link_item.get('href').replace(',', '®')
                    full_link = "https://en.wikipedia.org" + link

                    if "/wiki" not in link: # we only want wiki links
                        continue

                    try:
                        link_page = requests.get(full_link)
                    except:
                        print("ERROR reading link: " + full_link)
                        continue

                    link_soup = BeautifulSoup(link_page.content, "html.parser")
                    headers = link_soup.find_all('h2')
                    headers += link_soup.find_all('h3')
                    for header in headers:
                        if 'personnel' in header.text.lower():
                            links.append(link)
                    
                followingLinks.append(links)

            for i in range(len(album_headers)):
                for j in range(len(followingLinks[i])):
                    headerText = album_headers[i].text.replace(',', '') # remove commas
                    out_file.write(f'{row["Artist"]},{headerText},{followingLinks[i][j]},https://en.wikipedia.org{followingLinks[i][j]}\n')


