## Task 1: MongoDB and API Development Exercise

### Objective

Develop a pipeline that involves setting up a MongoDB database using Docker Compose, retrieving and storing data from an external API, and exposing the data through FastAPI.

1. Setup MongoDB with Docker Compose
    - Use Docker Compose to set up a MongoDB database.

2. Data Retrieval and Loading into MongoDB
    - Retrieve data from https://jsonplaceholder.typicode.com/
    - and store it in MongoDB using python.

3. Create a RESTful API with FastAPI
    - Develop a FastAPI application to provide access to the Mongo data.
    - Include endpoints to report the total number of posts from each user and comments for each post.
    - Include endpoints to add / modify / delete a user.


MongoDB docker image: docker pull topz2k480/json-placeholder-turbit