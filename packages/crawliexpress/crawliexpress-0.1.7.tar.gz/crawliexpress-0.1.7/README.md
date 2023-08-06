# Crawliexpress

- [Crawliexpress](#crawliexpress)
  - [Description](#description)
  - [Usage](#usage)
    - [Install](#install)
    - [Item](#item)
    - [Feedbacks](#feedbacks)
    - [Search / Category](#search--category)
  - [API](#api)

## Description

Allows to fetch various resources from Aliexpress, such as category, text search, product, feedbacks.

It does not use official API nor a headless browser, but parses page source.

Obviously, it is very vulnerable to DOM changes.

## Usage

### Install

```bash
pip install crawliexpress
```

### Item

```python
from crawliexpress import Client

client = Client("https://www.aliexpress.com")
client.get_item("4000505787173")
```

### Feedbacks

```python
from crawliexpress import Client

from pprint import pprint
from time import sleep

client = Client("https://www.aliexpress.com")
item = client.get_item("20000001708485")

page = 1
pages = list()
while True:
    feedback_page = client.get_feedbacks(
        item.product_id,
        item.owner_member_id,
        item.company_id,
        with_picture=True,
        page=page,
    )
    print(feedback_page.page)
    if feedback_page.has_next_page() is False:
        break
    page += 1
    sleep(1)
```

### Category

```python
from crawliexpress import Client

from time import sleep

client = Client(
    "https://www.aliexpress.com",
    # copy it from your browser cookies
    "xxxx",
)

page = 1
while True:
    search_page = client.get_category(205000314, "t-shirts", page=page)
    print(search_page.page)
    if search_page.has_next_page() is False:
        break
    page += 1
    sleep(1)
```

- Cookies must be taken from your browser cookies, to avoid captcha and empty results. I usually login then copy as cURL a request made by my browser on a category or a text search. Make sure to remove the `Cookie: ` prefix to keep only cookie values.

### Search

```python
from crawliexpress import Client

from time import sleep

client = Client(
    "https://www.aliexpress.com",
    # copy it from your browser cookies
    "xxxx",
)

page = 1
while True:
    search_page = client.get_search("akame ga kill", page=page)
    print(search_page.page)
    if search_page.has_next_page() is False:
        break
    page += 1
    sleep(1)
```

- Cookies must be taken from your browser cookies, to avoid captcha and empty results. I usually login then copy as cURL a request made by my browser on a category or a text search. Make sure to remove the `Cookie: ` prefix to keep only cookie values.

## API

### class crawliexpress.Category(client, category_id, category_name, sort_by='default')
A category


* **Parameters**


    * **category_id** – id of the category, category id of [https://www.aliexpress.com/category/205000221/t-shirts.html](https://www.aliexpress.com/category/205000221/t-shirts.html) is 205000220


    * **category_name** – name of the category, category name of [https://www.aliexpress.com/category/205000221/t-shirts.html](https://www.aliexpress.com/category/205000221/t-shirts.html) is t-shirts


    * **sort_by** (**default**: best match
    **total_tranpro_desc**: number of orders) – indeed



### class crawliexpress.Client(base_url, cookies=None)
Exposes methods to fetch various resources.


* **Parameters**


    * **base_url** – allows to change locale (not sure about this one)


    * **cookies** – must be taken from your browser cookies, to avoid captcha and empty results. I usually login then copy as cURL a request made by my browser on a category or a text search. Make sure to remove the **Cookie:** prefix to keep only cookie values.



#### get_category(category_id, category_name, page=1, sort_by='default')
Fetches a category page


* **Parameters**


    * **category_id** – id of the category, category id of [https://www.aliexpress.com/category/205000221/t-shirts.html](https://www.aliexpress.com/category/205000221/t-shirts.html) is 205000220


    * **category_name** – name of the category, category name of [https://www.aliexpress.com/category/205000221/t-shirts.html](https://www.aliexpress.com/category/205000221/t-shirts.html) is t-shirts


    * **page** – page number


    * **sort_by** (**default**: best match
    **total_tranpro_desc**: number of orders) – indeed



* **Returns**

    a search page



* **Return type**

    Crawliexpress.SearchPage



* **Raises**


    * **CrawliexpressException** – if there was an error fetching the dataz


    * **CrawliexpressCaptchaException** – if there is a captcha, make sure to use valid cookies to avoid this



#### get_feedbacks(product_id, owner_member_id, company_id=None, v=2, member_type='seller', page=1, with_picture=False)
Fetches a product feedback page


* **Parameters**


    * **product_id** – id of the product, item id of [https://www.aliexpress.com/item/20000001708485.html](https://www.aliexpress.com/item/20000001708485.html) is 20000001708485


    * **owner_member_id** – member id of the product owner, as stored in **Crawliexpress.Item.owner_member_id**


    * **page** – page number


    * **with_picture** – limit to feedbacks with a picture



* **Returns**

    a feedback page



* **Return type**

    Crawliexpress.FeedbackPage



* **Raises**

    **CrawliexpressException** – if there was an error fetching the dataz



#### get_item(item_id)
Fetches a product informations from its id


* **Parameters**

    **item_id** – id of the product to fetch, item id of [https://www.aliexpress.com/item/20000001708485.html](https://www.aliexpress.com/item/20000001708485.html) is 20000001708485



* **Returns**

    a product



* **Return type**

    Crawliexpress.Item



* **Raises**

    **CrawliexpressException** – if there was an error fetching the dataz



#### get_search(text, page=1, sort_by='default')
Fetches a search page


* **Parameters**


    * **text** – text search


    * **page** – page number


    * **sort_by** (**default**: best match
    **total_tranpro_desc**: number of orders) – indeed



* **Returns**

    a search page



* **Return type**

    Crawliexpress.SearchPage



* **Raises**


    * **CrawliexpressException** – if there was an error fetching the dataz


    * **CrawliexpressCaptchaException** – if there is a captcha, make sure to use valid cookies to avoid this



### exception crawliexpress.CrawliexpressCaptchaException()

### exception crawliexpress.CrawliexpressException()

### class crawliexpress.Feedback()
A user feedback


#### comment( = None)
Review


#### country( = None)
Country code


#### datetime( = None)
Raw datetime from DOM


#### images( = None)
List of image links


#### profile( = None)
Profile link


#### rating( = None)
Rating out of 100


#### user( = None)
Name


### class crawliexpress.FeedbackPage()
A feedback page


#### feedbacks( = None)
List of **Crawliexpress.Feedback** objects


#### has_next_page()
Returns true if there is a following page, useful for crawling


* **Return type**

    bool



#### known_pages( = None)
Sibling pages


#### page( = None)
Page number


### class crawliexpress.Search(client, text, sort_by='default')
A search


* **Parameters**


    * **text** – text search


    * **sort_by** (**default**: best match
    **total_tranpro_desc**: number of orders) – indeed



### class crawliexpress.SearchPage()
A search page


#### has_next_page()
Returns true if there is a following page, useful for crawling


* **Return type**

    bool



#### items( = None)
List of products, raw from JS parsing


#### page( = None)
page number


#### result_count( = None)
Number of result for the whole search


#### size_per_page( = None)
Number of result per page
