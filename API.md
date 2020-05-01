# REST API Docs

There is also a swagger docs [here](https://jotaviobiondo-library.herokuapp.com/docs).

## Authors

### List all authors
```
GET /api/authors/
```

URL query parameters:
- `name`: name of the author (doesn't need to be exact nor match case).
- `page`: the page number. 
    - Default: `1`.
- `page_size`: the maximum number of results of a page. 
    - Default: `10`.
- `ordering`: the field name to order the items.
    - Possible values: `name`. Use the '-' prefix for descending order, like so: `-name`.
    - Default: `name`.

All filters are optional.

Response example:

`HTTP 200 OK`
```jsonc
{
    "count": 1,         // Total number of items of the search (counting all pages)
    "next": null,       // A url to the next page
    "previous": null,   // A url to the previous page
    "results": [
        {
            "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
            "name": "Author Name"
        }
    ]
}
```

### Retrieve single author by id

```
GET /api/authors/{author_id}/
```

Parameters:
- `author_id`: The author id.


Response example:

`HTTP 200 OK`
```jsonc
{
    "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
    "name": "Author Name"
}
```


## Books

### List all books

```
GET /api/books/
```

URL query parameters:
- `name`: name of the book (doesn't need to be exact nor match case).
- `edition`: the edition of the book.
- `publication_year`: the publication year of the book.
- `author`: name of an author (doesn't need to be exact nor match case).
- `page`: the page number. 
    - Default: `1`.
- `page_size`: the maximum number of results of a page. 
    - Default: `10`.
- `ordering`: the field name to order the items.
    - Possible values: `name`, `edition`, `publication_year`, `authors__name`. Use the '-' prefix for descending order, like so: `-name`.
    - Default: `name`.

All filters are optional.

Response example:

`HTTP 200 OK`
```jsonc
{
    "count": 1,         // Total number of items of the search (counting all pages)
    "next": null,       // A url to the next page
    "previous": null,   // A url to the previous page
    "results": [
        {
            "id": "6e82ec62-9d0f-4486-ba2b-c131697b3084",
            "name": "Book Name",
            "edition": 1,
            "publication_year": 2020,
            "authors": [
                {
                    "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
                    "name": "Author Name"
                }
            ]
        }
    ]
}
```


### Retrieve single book by id
```
GET /api/books/{book_id}
```

Parameters:
- `book_id`: The book id.

Response example:

`HTTP 200 OK`
```jsonc
{
    "id": "6e82ec62-9d0f-4486-ba2b-c131697b3084",
    "name": "Book Name",
    "edition": 1,
    "publication_year": 2020,
    "authors": [
        {
            "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
            "name": "Author name"
        }
    ]
}
```

### Create book
`POST /api/books/`

Payload example:
```jsonc
{
    "name": "New Book",        // Required
    "edition": 1,              // Required
    "publication_year": 2020,  // Required
    "authors": [               // Required and not empty
        "f50eaf41-b940-4fa0-be67-f1e70c197d53" // Author id
    ]
}
```

Response example:

`HTTP 201 CREATED`
```jsonc
{
    "id": "293186ef-046d-4c39-bf47-9dba8b84a6e6",
    "name": "New Book",
    "edition": 1,
    "publication_year": 2020,
    "authors": [
        {
            "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
            "name": "Author Name"
        }
    ]
}
```

### Update book
```
PUT /api/books/{book_id}
```

Parameters:
- `book_id`: the id of the book to be updated.

Payload example:
```jsonc
{
    "name": "Updated Book",    // Required
    "edition": 2,              // Required
    "publication_year": 2020,  // Required
    "authors": [               // Required and not empty
        "f50eaf41-b940-4fa0-be67-f1e70c197d53" // Author id
    ]
}
```

Response example:

`HTTP 200 OK`
```jsonc
{
    "id": "293186ef-046d-4c39-bf47-9dba8b84a6e6",
    "name": "Updated Book",
    "edition": 2,
    "publication_year": 2020,
    "authors": [
        {
            "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
            "name": "Author Name"
        }
    ]
}
```

### Partial update book
```
PATCH /api/books/{book_id}
```

Parameters:
- `book_id`: the id of the book to be updated.

Payload example:
```jsonc
{
    "name": "Updated Book",    // Optional
    "edition": 2,              // Optional
    "publication_year": 2020,  // Optional
    "authors": [               // Optional (when specified, can not be empty)
        "f50eaf41-b940-4fa0-be67-f1e70c197d53"
    ]
}
```

All fields in the payload are optional, that is, it is not necessary to inform all fields to update the book.

Response example:

`HTTP 200 OK`
```jsonc
{
    "id": "293186ef-046d-4c39-bf47-9dba8b84a6e6",
    "name": "Updated Book",
    "edition": 2,
    "publication_year": 2020,
    "authors": [
        {
            "id": "f50eaf41-b940-4fa0-be67-f1e70c197d53",
            "name": "Author Name"
        }
    ]
}
```

### Delete book
```
DELETE /api/books/{book_id}
```

Parameters:
- `book_id`: the id of the book to be deleted.

Response:

`HTTP 204 NO CONTENT`