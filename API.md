# **General API Information**

This API uses `POST` request to communicate and HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. All responses come in standard JSON. All requests must include a `content-type` of `application/json` and the body must be valid JSON.

---
### Response Codes
```
200: Success
400: Bad request
401: Unauthorized
404: Cannot be found
405: Method not allowed
422: Unprocessable Entity 
50X: Server Error
```
---

---

### The following base endpoints are available:
```
http://127.0.0.1:5000/api/v1
```
### The base endpoint http://127.0.0.1:5000/api/v1 can be used to access the following API endpoints:

```
1.
GET /countries
GET /countries/country_id
GET /countries/country_id/cities
GET /countries/country_id/cities/city_id

2.
GET /cities
GET /cities/city_id
POST /cities
PUT /cities/city_id
DELETE /cities/city_id
DELETE /cities

```

### 1.1. `/countries`
get all countries

**Request:**
```
GET /countries
GET /countries/?page=1
```

**Response:**
```

{
     "countries": [
          {
               "code": "IS",
               "description": "The flag of Iceland has a blue field with a large white-edged red cross that extends to the edges of the field. The vertical part of this cross is offset towards the hoist side.",
               "flag": "https://flagcdn.com/w320/is.png",
               "id": 1,
               "name": "Iceland"
          },
          {
               "code": "JO",
               "description": "The flag of Jordan is composed of three equal horizontal bands of black, white and green, with a red isosceles triangle superimposed on the hoist side of the field. This triangle has its base on the hoist end, spans about half the width of the field and bears a small seven-pointed white star at its center.",
               "flag": "https://flagcdn.com/w320/jo.png",
               "id": 5,
               "name": "Hashemite Kingdom of Jordan"
          },
     "next_page": "/api/v1/countries/?page=2",
     "prev_page": null,
     "total": 250
}

```
---

### 1.2. `/countries/country_id`
get one country by id

**Request:**
```
GET /countries/2
```

**Response:**
```

{
     "code": "JP",
     "description": "The flag of Japan features a crimson-red circle at the center of a white field.",
     "flag": "https://flagcdn.com/w320/jp.png",
     "id": 2,
     "name": "Japan"
}

```
---

### 1.3. `/countries/country_id/cities`
get cities in this country

**Request:**
```
GET /countries/2/cities
```

**Response:**
```

{
     "cities": [
          {
               "country_id": 2,
               "country_name": "Japan",
               "id": 2,
               "name": "Tokyo"
          },
          {
               "country_id": 2,
               "country_name": "Japan",
               "id": 3,
               "name": "Tokio"
          },
          {
               "country_id": 2,
               "country_name": "Japan",
               "id": 8,
               "name": "Osaka"
          },
          {
               "country_id": 2,
               "country_name": "Japan",
               "id": 9,
               "name": "Kyoto"
          }
     ],
     "next_page": null,
     "prev_page": null,
     "total": 9
}

```
---

### 1.4. `/countries/country_id/cities/city_id`
get information on a specific city

**Request:**
```
GET /countries/2/cities/8
```

**Response:**
```

{
     "country_id": 2,
     "country_name": "Japan",
     "id": 8,
     "name": "Osaka"
}

```

---

---

### 2.1. `/cities`
get all cities

**Request:**
```
GET /cities
```

**Response:**
```
{
     "cities": [
          {
               "country_id": 30,
               "country_name": "Kingdom of Spain",
               "id": 1,
               "name": "Barcelona"
          },
          {
               "country_id": 2,
               "country_name": "Japan",
               "id": 2,
               "name": "Tokyo"
          }
     ],
     "next_page": "/api/v1/cities/?page=2",
     "prev_page": null,
     "total": 9
}

```

---

### 2.2. `/cities/city_id`
getting information about the city by id

**Request:**
```
GET /cities/2
```

**Response:**
```
{
     "country_id": 2,
     "country_name": "Japan",
     "id": 2,
     "name": "Tokyo"
}

```

---

### 2.3. `/cities`
add city

**Request:**
```
POST  /cities

{
     "name": "odessa"
}

```

**Response:**
```
{
     "city": {
          "country_id": 196,
          "country_name": "Ukraine",
          "id": 10,
          "name": "Odessa"
     },
     "location": "/api/v1/cities/10"
}

```

---

### 2.4. `/cities/city_id`
update city information

**Request:**
```
PUT  /cities/7

{
     "name": "kiev"
}
```

**Response:**
```
{
     "country_id": 196,
     "country_name": "Ukraine",
     "id": 7,
     "name": "Kiev"
}

```

---

### 2.5. `/cities/city_id`
delete city by id

**Request:**
```
DELETE  /cities/2

{
     "name": "kiev"
}
```

**Response:**
```

```

---

### 2.6. `/cities`
delete all cities

**Request:**
```
DELETE  /cities
```

**Response:**
```
{
     "cities": [],
     "next_page": null,
     "prev_page": null,
     "total": 0
}

```

