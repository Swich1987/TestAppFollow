# Python developer Test

You can use any of the next frameworks: (Django, Tornado, Flask, Pyramid, Falcon, AioHTTP, Sanic).

Specify all dependencies in a separate file. If you are familiar enough with Docker, you can write Dockerfile for your application, a docker-compose configuration file and pack everything you need into containers, where everything will be already installed, and your code will be assembled and ready to run. This is the perfect option.

## Description
Create an application that will periodically parse the main page of [Hacker News](https://news.ycombinator.com), pulling out a list of posts and saving it to the database.
The application must have HTTP API endpoint with only one method (GET /posts), with which you can get a list of all available (collected) news.
Every new should have a title, URL and datetime, when it was stored in the database.
It's enough to save only 30 news item and come after new ones at a certain time interval, or on demand.

API method to get a list of news on request: 

    curl -X GET http://localhost:8000/posts

The result is a news list in JSON:

    [
      {"id": 1, "title": "Announcing Rust 1.33.0", "url": "https://example.com", "created": "ISO 8601"},
      {"id": 2, "title": "Redesigning GitHub Repository Page", "url": "https://example.com", "created": "ISO 8601"}
    ]

Should work sorting by the given attribute, in ascending and descending order.

    curl -X GET http://localhost:8000/posts?order=title

Also, the client should be able to request a subset of data, specifying `offset` and `limit`. Let the default API return be 5 posts.

    curl -X GET http://localhost:8000/posts?offset=10&limit=10

Of course, the client can specify sorting and limits at the same time.

## Question
What happens in the following cases? What the API will do in each case?
- Client requests a non-existent attribute in sorting
- The limit is too big
- The limit is negative

## Requirements
- Instructions for running the application must be in README
- Link to the github repository with solution
- Link to the deployed application publicly available 
- The code should be covered with tests. You can use any library (unittest, nose, pytest)
