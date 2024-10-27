This is a data engineering project where i have utilized Kafka inorder to understand the user behaviours by their addclicking in the browser. 

This uses docke compose file that spins zookeeper and kafka. After that user can start flask application which displays some static contatin to the browser. 

As user clicks on any of the images and button, kafka producers triggers by the name click-topic. This message is then consumed by consumer and is stored in database.  