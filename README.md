## Shurl
*An MVP based DRF applicaton of url shortening service*

## Setup
- clone the repo `git clone https://github.com/khixar/Shurl.git`
- CMD `cp .env.example shurl/.env` and set the env variables accordingly
- CMD `docker-compose up`

## API utilization
*Please find the attached postman collection for*:
- Creates the `short url` by sending POST request to `http://0.0.0.0:8000//shorturl/create_short_url`
- Click on the short url in postman from last request and hit enter. It'd redirect to the orignal url
