# Crawliexpress

## Presentation

Allows to fetch various resources from Aliexpress, such as category, text search, product, feedbacks.

It does not use official API nor a headless browser, but parses page source.

Obviously, it is very vulnerable to DOM changes.

### Module classes

- **Client** : exposes methods to fetch various resources
- **Item**: A product
- **FeedbackPage**: A product feedback page, contains user feedbacks
- **Feedback**: A user feedback on a product
- **SearchPage**: A list of items from a category or a text search

## Usage

### Install

```bash
pip install crawliexpress
```

### Item

```python
from crawliexpress import Client

client = Client("https://fr.aliexpress.com")
client.get_item("4000505787173")
```

### Feedbacks

```python
from crawliexpress import Client

from pprint import pprint
from time import sleep

client = Client("https://fr.aliexpress.com")
item = client.get_item("20000001708485")

page_no = 1
pages = list()
while True:
    page = client.get_feedbacks(
        item.product_id,
        item.owner_member_id,
        item.company_id,
        with_picture=True,
        page=page_no,
    )
    if page.has_next_page() is False:
        break
    page_no += 1
    sleep(1)
```

### Search / Category

```python
rom crawliexpress import Client

from time import sleep

client = Client(
    "https://fr.aliexpress.com",
    xman_t="k++kIGjVqO0lCuOTMhKQUevJCW3sdIn4iNmwfMA7Pj/OqiTgTOYZUJ73JKhAufD1QMqkx8WKpiBq82niJM+AAPFH5pDadbfbs6bo6blWmTKXGATIXt6U19wbWEXrsyXkWREZmTQA0hE6fR6VsvMksQGjgbMHw1OuTKykAN7V+1SGr2lSDxZrWHTVjiQr5KHW+B3J5tfdUL/kD3x0Cks99EIJk3DASJUHTm5JXFbWZk6mAENwoMKA7UcNIa2qJ9L9svSVh913O4YHrv8fE7g1MR2OCMucyISEDhE4oocRZOr20AiPnA7K0saIrCL1YlTsdYrfrT3NvQsosnRJ5kcK6wCNCN2Mb1+RNe7YYEvW9owYF4zr/+Wlgf3bdAsknBq/X2JP8mOnjmMRaHXMk0NI2HrMejliPvsSRUixBHuzLoQgNjpZlzf6PdHD4qfSZAmGTpemKlvm3sU02GbahHPYLe4EU050PJOfdcki/EFV2lp3tZpMP5OkKRzZykcZ2zuicjnPUQM/FFkztEAQEjiWHYcL0vA9/4DTd47mz8tXL2wq0s8HdJ3mWPpyazZAKSb8EDauOLgifNs5cl8VPDV8SIPBfW7mAYw7Fi2zMzAgUdO28+o2zTYszr8rjzNhtOgqybvMH8bao5xTXIzjbcLbQ600vPzdYO0",
    x5sec="b2261652d676c6f7365617263682d7765623b32223a226164326232393838396239363337363335333865353262623839616339633365434f43787a507346454c364b682f4b626973755264526f4d4d546b334d4451304e5467324d547378227d",
    aep_usuc_f="site=fra&c_tp=EUR&x_alimid=1970445861&isb=y&ups_u_t=1635073090737&region=FR&b_locale=fr_FR&ae_u_p_s=0",
)

page_no = 1
while True:

    # category
    page = client.get_search(page_no, category_id=205000314)

    # text search
    # page = client.get_search(page_no, search_text="allo le monde")
    if page.has_next_page() is False:
        break
    page_no += 1
    sleep(1)
```

- **xman_t**, **x5sec**, **aep_usuc_f**: must be taken from your browser cookies, to avoid captcha and empty result pages

## API doc

### Crawliexpress.Client

Exposes methods to fetch various resources

#### method \__init__(base_url, xman_t=None, x5sec=None, aep_usuc_f=None)

- **base_url**: allows to change locale (not sure about this one)
- **xman_t**, **x5sec**, **aep_usuc_f**: must be taken from your browser cookies, to avoid captcha and empty result pages on get_search() calls

#### method get_item(item_id)

Returns an instance of Item

#### method get_feedbacks(product_id, owner_member_id, company_id=None, v=2, member_type="seller", page=1, with_picture=False)

- **owner_member_id**: found in an Item instance

Returns an instance of FeedbackPage

#### method get_search(page_no, category_id=0, search_text=None, sort_by="default")

- **page_no**: page number
- **category_id**: useful to browse a category page
- **search_text**: useful to browse a text search result page
- **sort_by**
  - **default**: best match
  - **total_tranpro_desc**: number of orders

Returns an instance of SearchPage

### Crawliexpress.Item

#### property product_id

#### property owner_member_id

#### property company_id

### Crawliexpress.FeedbackPage

#### property feedbacks

List of Feedback objects

#### property page

Page number

#### property known_pages

sibling pages

#### method has_next_page

Returns True if it's not the last page, useful to crawl feedbacks

### Crawliexpress.Feedback

#### property user

User name

#### property profile

User profile link

#### property country

User country

#### property rating

User rating percent

#### property datetime

Raw feedback date time

#### property comment

User comment

#### property images

List of image links

### Crawliexpress.SearchPage

#### property items

List of raw items as returned by Aliexpress API

#### property page

Page number

#### property result_count

Number of results for the search

#### property size_per_page

Number of results per page

#### method has_next_page

Returns True if it's not the last page, useful to crawl feedbacks

### Crawliexpress.CrawliexpressException

Raised on various source parsing fails

### Crawliexpress.CrawliexpressCaptchaException

Raised when a captcha is detected
