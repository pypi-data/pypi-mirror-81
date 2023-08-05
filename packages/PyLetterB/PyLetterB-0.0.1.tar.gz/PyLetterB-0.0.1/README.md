# PyLB

PYLB is an unofficial LetterBoxd API. Currently it only supports getting a list of Users who like a particular film, and getting a list of films liked by a particular user. It was made as a learning excercise and to meet the needs of another project. If there is interest or need, it may be expanded. It is not related to and does not use the Letterboxd official API, currently in beta. 


### Installation
```
$ pip install PyLB
```

### Example Usage

```
from PyLB import Users

#get list of all users who like the film Chungking Express
u = users.get_users_by_film_all('chungking-express') 

#get list of fiilms liked by a given user:
f = users.get_likes_by_user_all('fake-user-name')
