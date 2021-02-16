# apparel-search-engine-Elasticsearch

A Simple search engine for products.

## Why Elasticsearch?

Elasticsearch is widely used in many Companies because of it's simplicity and speed in searching. It stores the data in the form of documents(files) in a Index (similar to table in SQL).
Searching is done with the method of Inverted Indices which makes elasticsearch fast.

## Dataset:
Dataset can be obtained from [here](https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset).

## Docker
Note : keep the docker installed and running before the next steps.

Steps to set Elasticsearch container

 -docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.0
 
 -docker run --name CONTAINER_NAME -d -p 9200:9200 IMAGE_NAME

Steps to run the Flask application.

 -Execute the commands where the Dockerfile is present.
 
 -docker build -t IMAGE_NAME .
 
 -docker run --name CONTAINER_NAME -d -p 5000:5000 IMAGE_NAEME

Run the command to check the containers are up and running
###### docker ps

Go to the browser and hit http://localhost:5000 you will see the home page of the application and search for the products
Results :

![plot](https://github.com/sunilbelde/apparel-search-engine-Elasticsearch/blob/main/Results/Blueshirts.JPG)

Architecture of the environment:

![plot](https://github.com/sunilbelde/apparel-search-engine-Elasticsearch/blob/main/Results/Architecture.JPG)

Tools Used:

![plot](https://github.com/sunilbelde/apparel-search-engine-Elasticsearch/blob/main/Results/Tools.JPG)

