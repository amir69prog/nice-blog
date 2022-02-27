# nice-blog
A Blog app written by django/python 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) or [pipenv](https://pipenv.pypa.io/en/latest/) to install the **nice-blog**'s packages


### `pip` package manager
```bash
python3 -m venv venv
```
then activate the virtual enviroment
```bash
source venv/bin/activate
```

finally install the packages
```bash
pip install -r requirements.txt
```


### `pipenv` package manager
if you don't have `pipenv` you should install it at the first 
```bash
pip install pipenv
```
then creating a `Pipfile` and `Pipfile.lock` in your directory
```bash
pipenv shell
```

finally install the packages
```bash
pipenv install -r requirements.txt
```

## Usage
after you activate `virtual enviroment` and install `dependencies`

open your terminal and write the following code to create `Database` as **`sqlite.db`**

```bash
python3 manage.py migrate
```


## Technologies
OK! for this sample project i've used these following technologies
- [Python](https://www.python.org/)
- [Django version ~4.0](https://www.djangoproject.com/)
- [Django-Rest-Framework](https://www.django-rest-framework.org/) for building **APIs**
- [JWT](https://github.com/jazzband/djangorestframework-simplejwt) for auth with **tokens**
- [OTP](https://github.com/pyauth/pyotp) as **OneTimePassword**
- [Redis](https://github.com/jazzband/django-redis) for **caching** system
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) for **rendering** the forms in UI
- [Markdown](https://pypi.org/project/Markdown/) for convert **Text > HTML**

## Features
So this is a simple blog that you go register then verify your account with `OTP` that sending to your phone_number
> NOTE:  becouse this is a local develpment project actually i am not going to send **OTP**  by **SMS** to the phone number i just sent it to the console so for verifying your account the **OTP** will print in the console or if you give an email i will send it to your email in the console as well :)

and then you will paste the password and your account will  be verified as well as quick

and after this process you can go directly use the app 

for example: 
- **CREATE** : your own posts
- **READ** : all posts
- **UPDATE** : your own posts
- **DELETE** : your own posts

posts as well as possible

and another feature is the ***API*** 

so if you go to the documention session of the site you can see the API Document to work with that as easy
