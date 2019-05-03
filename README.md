# Test task solution
## Test task
[Original Test task](https://github.com/Swich1987/TestAppFollow/blob/master/TestTask.md)
## Russian:
[Russian README](https://github.com/Swich1987/TestAppFollow/blob/master/README_RU.md)

[Russian test task](https://github.com/Swich1987/TestAppFollow/blob/master/TestTaskRU.md)
## Selected Stacks
Django with PostgreSQL (starts in a separate container, port 5432 should be available)

## Running the application
To start the local server:

    git clone https://github.com/Swich1987/TestAppFollow.git
    cd TestAppFollow
    docker-compose up

At startup a task will be created to download news from hackernews, which will be executed 1 time per minute. You can adjust the update interval in the `loop_parsing.py`.
Also, internal Django tests are launched before starting the server

After the launch local server is available at the link:

    http://127.0.0.1:8000/posts


To launch remote server, which should be available publicly, you need to add the address of this server to the parameter `ALLOWED_HOSTS`, located in the file `settings.py`.


## Public server
The public server is available at the link:

    http://ec2-18-218-151-219.us-east-2.compute.amazonaws.com:8000/posts


## Parsing and updating news from [Hacker News](https://news.ycombinator.com)
News is loaded first at the start of the container and then once every minute. They can be started manually when the container is running using next command:

    docker exec -it testappfollow_web_1 python3 ./parse_hackernews/parse_hackernews.py

where `testappfollow_web_1` is the name of running container.


## Integration API test
To run the integration API tests of all endpoints, run the next command:

    python3 -m unittest -v test_all_api.py

These tests check all possible types of requests. Include those mentioned in questions to the task.
In the file `test_all_api.pu` is located URL parameter, with which you can set the server address for testing.


## Answers for questions
- Client requests a non-existent attribute in sorting
- Will be returned error 404 with given wrong attribute


- The limit is too big
- Will be cut to maximum allowed


- The limit is negative
- Will be set to minimum


A hyphen "-" in front of given attribute indicates descending sorting order. For example:

    curl -X GET http://localhost:8000/posts?order=-title

If you enter a non-existent address, for example http://127.0.0.1:8000/, will be returned error 404.
