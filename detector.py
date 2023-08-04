from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import math
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def sendPartition(iter):
    # ConnectionPool is a static, lazily initialized pool of connections
    var = iter.take(100)
    if len(var) > 0:
        event = "{" + f"'Falls':{str(var)}" + "}"
        producer.send('falls', json.dumps(event).encode())
        
ssc = SparkContext("local[2]", "Falls detector")
ssc = StreamingContext(ssc, 10)    # intervalos de datos cada 10 segundos
stream = KafkaUtils.createDirectStream(ssc, ['sensors'], 
                kafkaParams={"metadata.broker.list": "localhost:9092"})

dstream = stream.map(lambda x: json.loads(x[1]))
valuesX = dstream.map(lambda sensor: 'falls, ' + sensor["user"] + " " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") if math.sqrt((float(sensor['x'])**2 + float(sensor['y'])**2 + float(sensor['z'])**2)) > 5 else "")
pairs = valuesX.filter(lambda word: word != "")
result = pairs.map(lambda word: (word, 1))
groups = result.reduceByKey(lambda x, y: x + y)
groups.foreachRDD(lambda rdd: sendPartition(rdd))
groups.pprint()

ssc.start()
ssc.awaitTermination()


