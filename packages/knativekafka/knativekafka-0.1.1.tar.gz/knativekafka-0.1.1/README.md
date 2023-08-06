## knativekafka

knativekafka is a wrapper around kafka-python package. This package is easy to use and can be used to test the Kafka Producer in kafka-python package.

Some important items to note.

* This package includes the basic testing only as of now.

*  Polling, parallelism etc. has not been included yet.

### Installation Instructions

The package is availble in PyPI which is an official repository for python package.
pip is a package management system and is used for installing Python packages from Python Package Index (also known as PyPI). It is the most common way to install Python packages.
Install the package in your environment from the terminal using the below pip command:

`pip3 install knativekafka`


### Pre-requisites

- Python 3.x

- pip3

- Set the environment variable - KAFKA_BOOTSTRAP_SERVERS

- Have the kafka server installed and configured with a topic


### How to Use?

* Import the Kafka Producer into your python code using the below import.

`from knativekafka.knativekafkaproducer import KNativeKafkaProducer`

To import the Kafka Consumer use the below import.
`from knativekafka.knativekafkaconsumer import KNativeKafkaConsumer`
    

#### Usage

Only few features are implemented in the package as of now. 

Additional features to be included later.

#### Test Producer

To test the producer, perform the below steps.

* Instantiate the KNativeKafkaProducer by passing the kafka topic.

* The init() method checks whether the os.environ() contains the KAFKA_BOOTSTRAP_SERVERS key. 

* If so, it fetches the value from the environment. If not, it sets the default value as localhost:9092. 

* The topic is passed as parameter. If topic is an empty string, then, the topic is set to a default value. To send data, use the send_binary_data() by passing the message as parameter. The send_binary_data() takes the message in binary format.

```
    kafka_producer = KNativeKafkaProducer(os.environ['python-topic')
    value = input('value:')
    value = bytes(value, encoding='utf8')            
    kafka_producer.send_binary_data(value)    
    print("Successfully sent data....") 

```

#### Test Consumer

To test the consumer, perform the below steps.

* Instantiate the KNativeKafkaConsumer and then, call getMessage(). The getMessage() prints the message value.
                                                                      

```
kafka_consumer =  KNativeKafkaConsumer("python-topic-dlq")
msg = kafka_consumer.getMessage()    
print(msg)

```
#### References

- [knativekafka in test.pypi.org](https://test.pypi.org/project/knativekafka/0.1.1/)

- [knativekafka in pypi.org](https://pypi.org/project/knativekafka/0.1.1/)

### License

```
Apache License

```
