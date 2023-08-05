from PyLetterB.getpage import get_page
import random
import logging

logger = logging.getLogger()


def get_users_by_film_per_page(film, page, order=''):
    random_orders = ['/', '/by/date-earliest/', '/by/member-rating/']
    possible_orders = {'newest': '/', 'oldest': '/by/date-earliest/', 'highest': '/by/member-rating/',
                       'lowest': '/by/member-rating-lowest/'}
    if order not in possible_orders.keys():
        order = random_orders[random.randrange(0, len(random_orders))]
    else:
        order = possible_orders[order]
    logger.info(f'Getting user likes for film: {film} order: {order}, page: {page}')
    url = f'https://letterboxd.com/film/{film}/likes{order}page/{page}'
    soup = get_page(url)
    text = soup.find_all(class_='name')
    users = []
    for i in text:
        raw = str(i)
        raw = raw.replace('<a class="name" href="', '')
        raw = raw.split('"')
        users.append(raw[0].split("/")[1])
    return users


def get_users_by_film_all(film, order='newest'):
    users = []
    userset = get_users_by_film_per_page(film, 1, order)
    i = 2
    while userset:
        users.extend(userset)
        userset = get_users_by_film_per_page(film, i, order)
        i += 1
    return users


def get_user_likes_per_page(user, page):
    logger.info(f'Getting likes for user: {user}, page: {page}')
    url = f'https://letterboxd.com/{user}/likes/films/page/{page}'
    soup = get_page(url)
    text = soup.find_all(class_='poster')
    films = []
    for i in text:
        raw = str(i)
        raw = raw.split('data-film-slug="/film/', 2)
        raw = raw[1].split('/')
        films.append(raw[0])
    return films

def get_user_likes_all(user):
    films = []
    filmset = get_user_likes_per_page(user, 1)
    i = 2
    while filmset:
        films.extend(filmset)
        filmset = get_user_likes_per_page(user, i)
        i += 1
    return films


