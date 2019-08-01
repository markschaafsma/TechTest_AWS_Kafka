# TechTest_AWS_Kafka

### AWS Managed Streaming for Kafka Challenge - 15/04/2019

Original challenge comes from:   https://github.com/sarojdongol/event_2/wiki/3:-Challenge


### Challenge Summary

1. Setup a Kafka cluster with 2 nodes (manually, i.e. via EC2, not via AWS MSK).
2. Create a Kafka topic "learnkafka" with 1 parition and replication factor of 3.
3. Use producer sample code from github to write into kafka topic "learnkafka".
4. Then subscribe to the "learnkafka" topic and filter records with TICKER symbol "AMZN" and publish it to another topic "transformedrecord".
5. Send your command history from both the broker nodes and screenshot of the same to syd-ana-l2h@amazon.com


### Information Sources Found

   Simplest:       https://www.sohamkamani.com/blog/2017/11/22/how-to-install-and-run-kafka
   Simplest:       https://dzone.com/articles/kafka-setup
   Simple:         https://dzone.com/articles/installing-and-running-kafka-on-an-aws-instance
   More detailed:  https://labs.sogeti.com/wp-content/uploads/2018/07/PES-Apache-KAFKA-Cluster-SetupAdministrationAWS-V1.0.pdf 


### Solution

1. Setup a Kafka cluster with 2 broker nodes.

    Setup manually (i.e. via EC2, not via AWS MSK) 

    Key Configuration Items
   
        Instance Type = t2.xlarge                       # Configuration item in EC2 setup  
        Kafka version = 2.1.1                           # Download this version onto the EC2 instance  
        log-directory use = /home/ec2-user/kafka-log    # set log.dirs= in Kafka config/server.properties file
                                                        #   e.g. log.dirs=/home/ec2-user/kafka-log   
        broker port = 9092                              # set advertised.listeners= in Kafka config/server.properties file 
                                                        #   e.g. advertised.listeners=PLAINTEXT://0.0.0.0:9092  or
                                                        #   e.g. advertised.listeners=PLAINTEXT://ec2-xxx-xxx-xxx.xx.amazonaws.com:9092

    Broker 1:

        a) Setup EC2 instance.
            Instance Id:            i-08e0c485527879127
            Tag Name:               Kafka Node 1 - ZooKeeper + 1 broker
            Region:                 US East (N. Virgina)
            AMI:                    Amazon Linux 2 AMI 2.0.20190313 x86_64 HVM gp2
            Storage Size:           8GB SSD
            Instance Type:          t2.xlarge (Variable ECUs, 4 vCPUs, 2.3 GHz, Intel Broadwell E5-2686v4, 16GiB memory, EBS only)
            Public DNS (IPv4):      ec2-3-82-26-109.compute-1.amazonaws.com
            IPv4 Public IP:         3.82.26.109   
            Private DNS:            ip-172-31-39-71.ec2.internal   
            Private IPs:            172.31.39.71
            Key Pair name:          MSK-01
            Private Key:            C:\Users\Mark\Documents\Career\..\Technical Tests\AWS\Kafka Challenge\MSK-01.pem 
            Putty Private Key:      C:\Users\Mark\Documents\Career\..\Technical Tests\AWS\Kafka Challenge\MSK-01-Private.ppk
                Security Group:     sg-6672fd20
                    Inbound:        Type: All TCP; Protocol: TCP; Port Range: 0-65535; Source: 0.0.0.0/0
                    Inbound:        Type: SSH; Protocol: TCP; Port Range: 22; Source: 0.0.0.0/0

        b) Launch/Start instance.
			
        c) SSH (Putty) to instance.
            See doco:               https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
            Linux AMI User name:    ec2-user
            Host name model:        user_name@public_dns_name
            Host name:              ec2-user@ec2-3-82-26-109.compute-1.amazonaws.com

        d) Install Java.
            Overview:               Kafka client API is written in Java. Kafka server code is written in Scala. Both run inside a JVM.
            Install:                $sudo yum install java-1.8.0     # From 2.2.1 Installation of Client Packages and Phython Modules doco.
            Verify:                 $java -version 

        e) Download Kafka.
            Overview:               Find appropriate binary (not source) to download from Apache.
            Goto:                   https://kafka.apache.org/downloads
            Then goto:              https://www.apache.org/dyn/closer.cgi?path=/kafka/2.1.1/kafka_2.12-2.1.1.tgz
            Download:               $wget http://apache.mirror.serversaustralia.com.au/kafka/2.1.1/kafka_2.12-2.1.1.tgz

        f) Install Kafka.
            Install:                $tar -xzf kafka_2.12-2.1.1.tgz
            Remove zip:             $rm kafka_2.12-2.1.1.tgz

        g) Start Zookeeper server.
            Overview:               Use the convenience script packaged with Kafka to start a single-node Zookeeper instance.
            Chg directory:          $cd kafka_2.12-2.1.1
            Start ZK                $nohup bin/zookeeper-server-start.sh config/zookeeper.properties > ~/zookeeper-logs &  
                                        # "> ~/kafka-logs" redirects stdout to the named file in the users home directory 
                                        # "&"              directs the shell to run the command in the background.
            Verify ZK started:      $telnet localhost 2181
				
        h) Configure Broker server.
            Edit properties file:   $vi config/server.properties 		
            Set broker-id:          i set broker.id=0 <esc>
            Set listeners:          uncomment listeners=PLAINTEXT://:9092 
                                    or insert listeners=PLAINTEXT://ec2-3-82-26-109.compute-1.amazonaws.com:9092 <esc>
            Set log-directory:      i log.dirs=/home/ec2-user/kafka-log <esc>
            Set zookeeper.connect:  edit zookeeper.connect="ZookeeperConnectString"
                                    e.g.1 zookeeper.connect=localhost:2181,localhost:2182"
                                    e.g.2 zookeeper.connect=ec2-3-82-26-109.compute-1.amazonaws.com:2181
            Save changes:           :wq   # w =  write; q = quit
		
        i) Start Broker server.
            Overview:               Use the convenience script packaged with Kafka to start a single-node Zookeeper instance.
            Chg directory:          $cd kafka_2.12-2.1.1
            Start Broker (Opt1)     $nohup bin/kafka-server-start.sh config/server.properties > ~/kafka-logs & 
                                        # "> ~/kafka-logs" redirects stdout to the named file in the users home directory 
                                        # "&"              directs the shell to run the command in the background.
            Start Broker (Opt2)     $nohup bin/kafka-server-start.sh config/server.properties & 
                                        # "&" directs the shell to run the command in the background.
            Install Telnet          $sudo yum -y install telnet 
            Verify Broker started:  $telnet localhost 9092 ; quit
            Verify Broker started:  $telnet ec2-3-82-26-109.compute-1.amazonaws.com 9092 ; quit		

        j) Stop servers.
            Overview:               When finished, run the following scripts to stop the servers.
            Stop Kafka broker:      $bin/kafka-server-stop.sh
            Stop ZooKeeper:         $bin/zookeeper-server-stop.sh
			 
			 
    Broker 2:
   
        a) Setup another EC2 instance.
            Instance Id:            i-0b11695aec6703adb
            Tag Name:               Kafka Node 2 - 1 broker
            Region:                 US East (N. Virgina)
            AMI:                    Amazon Linux 2 AMI 2.0.20190313 x86_64 HVM gp2
            Storage Size:           8GB SSD
            Instance Type:          t2.xlarge (Variable ECUs, 4 vCPUs, 2.3 GHz, Intel Broadwell E5-2686v4, 16GiB memory, EBS only)
            Public DNS (IPv4):      ec2-18-207-229-227.compute-1.amazonaws.com
            IPv4 Public IP:         18.207.229.227 (old-3.89.42.105)   
            Private DNS:            ip-172-31-39-100.ec2.internal   
            Private IPs:            172.31.39.100
            Key Pair name:          MSK-01
            Private Key:            C:\Users\Mark\Development\AWS\MSK-01.pem 
            Putty Private Key:      C:\Users\Mark\Development\AWS\MSK-01-Private.ppk
                Security Group:     sg-6672fd20
                    Inbound:        Type: All TCP; Protocol: TCP; Port Range: 0-65535; Source: 0.0.0.0/0
                    Inbound:        Type: SSH; Protocol: TCP; Port Range: 22; Source: 0.0.0.0/0

        b) Launch/Start instance.
			
        c) SSH (Putty) to instance.
            See doco:               https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
            Linux AMI User name:    ec2-user
            Host name model:        user_name@public_dns_name
            Host name:              ec2-user@ec2-18-207-229-227.compute-1.amazonaws.com

        d) Install Java.
            Overview:               Kafka client API is written in Java. Kafka server code is written in Scala. Both run inside a JVM.
            Install:                $sudo yum install java-1.8.0     # From 2.2.1 Installation of Client Packages and Phython Modules doco.
            Verify:                 $java -version 

        e) Download Kafka.
            Overview:               Find appropriate binary (not source) to download from Apache.
            Goto:                   https://kafka.apache.org/downloads
            Then goto:              https://www.apache.org/dyn/closer.cgi?path=/kafka/2.1.1/kafka_2.12-2.1.1.tgz
            Download:               $wget http://apache.mirror.serversaustralia.com.au/kafka/2.1.1/kafka_2.12-2.1.1.tgz

        f) Install Kafka.
            Install:                $tar -xzf kafka_2.12-2.1.1.tgz
            Remove zip:             $rm kafka_2.12-2.1.1.tgz
				
        g) Configure Broker server.
            Overview:               Configure Kafka server including to use zookeeper server running in broker 1.
            Chg directory:          $cd kafka_2.12-2.1.1
            Edit properties file:   $vi config/server.properties
            Set broker-id:          i set broker.id=1 <esc>
            Set listeners:          uncomment listeners=PLAINTEXT://:9092 
                                    or insert listeners=PLAINTEXT://ec2-18-207-229-227.compute-1.amazonaws.com:9092
            Set log-directory:      i log.dirs=/home/ec2-user/kafka-log <esc>
            Set zookeeper.connect:  edit zookeeper.connect="ZookeeperConnectString"
                                    e.g.1 zookeeper.connect=localhost:2181,localhost:2182"
                                    e.g.2 zookeeper.connect=ec2-3-82-26-109.compute-1.amazonaws.com:2181
            Save changes:           :wq   # w =  write; q = quit
		
        h) Start Broker server.
            Overview:               Use the convenience script packaged with Kafka to start a single-node Zookeeper instance.
            Chg directory:          $cd kafka_2.12-2.1.1
            Start Broker (Opt1)     $nohup bin/kafka-server-start.sh config/server.properties > ~/kafka-logs & 
                                        # "> ~/kafka-logs" redirects stdout to the named file in the users home directory  
                                        # "&"              directs the shell to run the command in the background.
            Start Broker (Opt2)     $nohup bin/kafka-server-start.sh config/server.properties & 
                                        # "&" directs the shell to run the command in the background.
            Install Telnet          $sudo yum -y install telnet 
            Verify Broker started:  $telnet localhost 9092 ; quit
            Verify Broker started:  $telnet ec2-18-207-229-227.compute-1.amazonaws.com 9092 ; quit
		
        i) Stop servers.
            Overview:               When finished, run the following scripts to stop the servers.
            Stop Kafka broker:      $bin/kafka-server-stop.sh
  
    Results
	
        Provide output from the following commands and attach screenshot(must) in your email to us.
		
        a) Run Zookeeper shell and list broker ids.
            Goto Node-1 Kafka dir:  $cd  kafka_2.12-2.1.1 
            Run zookeeper shell:    ./bin/zookeeper-shell.sh "zookeeper-server-IP":2181
                                    ./bin/zookeeper-shell.sh localhost:2181
                                    ./bin/zookeeper-shell.sh ec2-3-82-26-109.compute-1.amazonaws.com:2181
            List Brokers:           ls /brokers/ids
            Quit command to quit:   quit 

   
   
2. Create Kafka topics "learnkafka" and "transformedrecord" with 1 partition and replication factor of 3.

    From either Node 1 or Node 2

        a) Create topic "learnkafka".
            Chg directory:           cd kafka_2.12-2.1.1
            Create topic:            ./bin/kafka-topics.sh --create --zookeeper ZookeeperConnectString --replication-factor 3 --partitions 1 --topic learnkafka
                                     ./bin/kafka-topics.sh --create --zookeeper "172.31.39.71:2181" --replication-factor 2 --partitions 1 --topic learnkafka 
                                         # Using internal IP
                                     ./bin/kafka-topics.sh --create --zookeeper "3.82.26.109:2181" --replication-factor 2 --partitions 1 --topic learnkafka 
                                         # Using external IP

        b) Create topic "transformedrecord".
            Chg directory:           cd kafka_2.12-2.1.1
            Create topic:            ./bin/kafka-topics.sh --create --zookeeper ZookeeperConnectString --replication-factor 3 --partitions 1 --topic transformedrecord
                                     ./bin/kafka-topics.sh --create --zookeeper "172.31.39.71:2181" --replication-factor 2 --partitions 1 --topic transformedrecord 
                                         # Using internal IP
                                     ./bin/kafka-topics.sh --create --zookeeper "3.82.26.109:2181" --replication-factor 2 --partitions 1 --topic transformedrecord 
                                         # Using external IP
									 

3. Use producer sample code from github to write into kafka topic "learnkafka".

    Client:
	
        a) Setup EC2 instance (or use existing EC2 client instance - which is what I did).
            Instance Id:            i-045759547c43d2db9
            Tag Name:               Client Machine
            Region:                 US East (N. Virgina)
            AMI:                    Amazon Linux 2 AMI 2.0.20190313 x86_64 HVM gp2
            Storage Size:           8GB
            Instance Type:          t2.xlarge
            Public DNS (IPv4):      ec2-34-238-52-132.compute-1.amazonaws.com
            IPv4 Public IP:         34.238.52.132  
            Private DNS:            ip-172-31-85-215.ec2.internal 
            Private IPs:            172.31.85.215
            Key Pair name:          MSK-01
            Private Key:            C:\Users\Mark\Development\AWS\MSK-01.pem 
            Putty Private Key:      C:\Users\Mark\Development\AWS\MSK-01-Private.ppk
                Security Group:     sg-6672fd20
                    Inbound:        Type: All TCP; Protocol: TCP; Port Range: 0-65535; Source: 0.0.0.0/0
                    Inbound:        Type: SSH; Protocol: TCP; Port Range: 22; Source: 0.0.0.0/0

        b) Launch/Start instance.
			
        c) SSH (Putty) to instance.
            See doco:               https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
            Linux AMI User name:    ec2-user
            Host name model:        user_name@public_dns_name
            Host name:              ec2-user@ec2-34-238-52-132.compute-1.amazonaws.com

        d) Install Java.
            Install:                $sudo yum install java-1.8.0     # From 2.2.1 Installation of Client Packages and Phython Modules doco.
            Verify:                 $java -version 

        e) Download Kafka.
            Find appropriate binary to download from Apache.
            Goto:                   https://kafka.apache.org/downloads
            Then goto:              https://www.apache.org/dyn/closer.cgi?path=/kafka/2.1.1/kafka_2.12-2.1.1.tgz
            Download:               $wget http://apache.mirror.serversaustralia.com.au/kafka/2.1.1/kafka_2.12-2.1.1.tgz  
                                        # Same version as brokers
            Download:               $wget https://archive.apache.org/dist/kafka/2.1.0/kafka_2.11-2.1.0.tgz 
                                        # Version initially setup as part of the demo 

        f) Install Kafka.
            Install:                $tar -xzf kafka_2.12-2.1.1.tgz    # Not done. Old version used instead.  
            Install:                $tar -xvf kafka_2.11-2.1.0.tgz    # Version initially setup as part of the demo 
            Remove zip:             $rm kafka_2.12-2.1.1.tgz

        g) Install pip (a package management system for installing and managing Python packages).
            Download:               $curl -O https://bootstrap.pypa.io/get-pip.py    # Download install script   
            Run script:             $python get-pip.py --user	 # Run python script to download and install pip and other required support packages. 	

    Producer Code:
			
        h) Copy producer code from code section of GitHub to a file "kakfa-producer-learnkafka.py" (use vi editor or similar)

            Create file:            vi kafka-producer-learnkafka.py
		
            Insert Code:

            import json
            import random
            import datetime
            import logging

            from kafka import KafkaProducer
            logging.basicConfig(level=logging.INFO)

            producer = KafkaProducer(bootstrap_servers="172.31.80.132:9092,172.31.39.5:9092,172.31.16.193:9092",key_serializer=str.encode,acks='all')

            def getReferrer():
                data = {}
                now = datetime.datetime.now()
                str_now = now.isoformat()
                data['EVENT_TIME'] = str_now
                data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
                price = random.random() * 100
                data['PRICE'] = round(price, 2)
                return data

            while True: 
                data = json.dumps(getReferrer())
                logging.info("Received Sample Data")
                try:
                    response = producer.send('demo',key='keyused',value=data)
                    logging.info("Sending Records to Kafka Topic demo")
                except Exception as e:
                    logging.error("Exception occurred", exc_info=True)

        i) Substitute relevant bootstrap_server and topic details in.

            bootstrap:       producer = KafkaProducer(bootstrap_servers="3.82.26.109:9092,3.89.42.105:9092",key_serializer=str.encode,acks='all')
            topic:           response = producer.send('learnkafka',key='keyused',value=data)
                             logging.info("Sending Records to Kafka Topic learnkafka")
		
        j) Execute code

            $python kafka-producer-learnkafka.py


4. Then subscribe to the "learnkafka" topic and filter records with TICKER symbol "AMZN" and publish it to another topic "transformedrecord".

    Consumer Code

        a) Copy consumer code from code section of GitHub to a file "kakfa-consumer-learnkafka.py" (use vi editor or similar)
		
            Create file:			vi kafka-consumer-learnkafka.py

            Insert Code:

            from kafka import KafkaConsumer,KafkaProducer
            import json
            import logging

            logging.basicConfig(level=logging.INFO)

            consumer = KafkaConsumer(bootstrap_servers="172.31.80.132:9092,172.31.39.5:9092,172.31.16.193:9092",auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda m: json.loads(m.decode('utf-8')))

            #subscribing the topic

            consumer.subscribe(['demo'])

            for msg in consumer:
                if(msg[6]["PRICE"] >= 60):
                    print("Consumed Records from demo",msg[6])

        b) Substitute relevant Bootstrap_server, topic and consumer details in.

            bootstrap:       consumer = KafkaConsumer(bootstrap_servers="3.82.26.109:9092,3.89.42.105:9092",auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
            topic:           consumer.subscribe(['learnkafka'])
            consumer:        for msg in consumer:
                                 if(msg[6]["TICKER"] = 'AMZN'):
                                     print("Consumed Records from learnkafka",msg[6])
                                     try:
                                         response = producer.send('transformedrecord',key='keyused',value=msg[6])
                                         logging.info("Sending Records to Kafka Topic transformedrecord")
                                     except Exception as e:
                                         logging.error("Exception occurred", exc_info=True)

        c) Execute code

            $python kakfa-consumer-learnkafka.py	


5. Send your command history from both the broker nodes and screenshot of the same to syd-ana-l2h@amazon.com

        a) List Node 1 Command History
		    Login node 1:           SSH (Putty) to instance as above. 
            List history:           $history	

        b) List Node 2 Command History
		    Login to node 2:        SSH (Putty) to instance as above.
            List history:           $history	

			
			


### Challenge Details

Copied from:   https://github.com/sarojdongol/event_2/wiki/3:-Challenge

Kafka version = 2.1.1
Instance Type = t2.xlarge

Use following configuration detail:
log-directory use = /home/ec2-user/kafka-log broker port = 9092

1. Setup Kafka cluster with 2 nodes.

   Broker 1 Install zookeeper server and kafka server. broker-id 0. Run the both services.
   Broker 2 Install kafka server configure it to use zookeeper server running in broker 1. Run the kafka server.

   Provide output of following command and attach screen shot(must) in your email.

   ./zookeeper-shell.sh zookeeper-server-IP:2181

   command to execute : ls /brokers/ids

2. Create a kafka topic "learnkafka" with 1 parition and replication factor 3

   Provide output of describe topic command:

3. Use producer sample from github to write into kafka topic "learnkafka"

4. Now subscribe the "learnkafka" topic and filter records with TICKER symbol "AMZN" and publish it to another topic "transformedrecord"

5. Send your command history from both the broker nodes and screenshot of the same.

   command:

   **$history **

   $ps -aux | egrep -i "zookeeper|kafka"

