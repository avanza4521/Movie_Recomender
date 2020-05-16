from bs4 import BeautifulSoup
import requests
import re

try:
    response = requests.get('https://www.imdb.com/title/tt1266036/?ref_=nv_sr_srsg_0')
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post = soup.find('body')
    title = post.find('h1').contents[0]
    year = post.find('span', {'id': 'titleYear'}).find('a').contents[0]
    summary = post.find('div', {'class': 'summary_text'}).text
    summary = re.sub('\s\s+', ' ', summary)
    genre = post.find('div', {'class': 'subtext'}).select("a[href*=genres]")
    genre = [g.contents[0] for g in genre]

    image = post.find('div', {'class': 'poster'}).find('img').get('src').split('UX182')[0]
    release_date = post.find('div', {'class': 'subtext'}).find('a', href=re.compile("release")).contents[0]
    if post.find('div', {'class': 'ratingValue'}):
        rating = post.find('div', {'class': 'ratingValue'}).find('span', {'itemprop': 'ratingValue'}).text
    else:
        rating = 'N/A'
    image = image + "UY450_AL_.jpg"
    video_url = post.find('div', {'class': 'slate'}).find('a').get('data-video')
    video_url = "https://www.imdb.com/video/imdb/" + video_url + "/imdb/embed?autoplay=false&width=640"
    sim = "You are sim"
    if "Comedy" in genre:
        sim = "success"
    print(title)
    print(year)
    print(summary)
    print(image)
    print(genre)
    print(video_url)
    print(release_date)
    print(rating)
    print(sim)
except:
    print("Some Field Are Missing")

