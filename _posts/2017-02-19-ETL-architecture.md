# Architecture – Batch Processing Subsystem



## Requirements

-	Design a batch processing subsystem that is responsible for daily ingesting data from a variety of data sources (an OLTP database, log data, and a variety of third party APIs), having a graph of processing tasks that operate on this data, and finally loading it into a variety of targets (a Data Warehouse, pushing to APIs, and publishing to an event broker).
-	The system will ingest at least a few data sources in the 10TB order of magnitude. 
-	An excellent developer experience is paramount - a new developer should feel comfortable creating a new job or modifying existing ones, and be as confident as possible that errors have not been introduced. For example, the developer should be able to test his or her changes.

## Design

In the following, I will describe two approaches to the problem, using the Amazon Web Services cloud platform. Using AWS would limit capital expenditures on the beefy and costly hardware that would be necessary to process tens of terabytes.

First, I should mention that AWS just announced last week at the re:invent conference three new services that are directly relevant to the problem at hand: 
-	AWS Glue is a managed ETL service that moves data between data stores. It automates data discovery, conversion, mapping, and job scheduling tasks. It works with Amazon S3 (object storage), Amazon RDS (OLTP databases), and Amazon Redshift (data warehouse), and can connect to any JDBC-compliant data store. https://aws.amazon.com/glue/ 

-	AWS Batch runs batch jobs (e.g. a shell script, a Linux executable, or a container image) as a containerized application on EC2 servers, using parameters provided in a job definition. Jobs can be dependent on the successful completion of other jobs. https://aws.amazon.com/blogs/aws/aws-batch-run-batch-computing-jobs-on-aws/

-	AWS Step Functions is a web service that coordinates the components of distributed applications and micro-services using visual workflows. The developer can literally drag and drop steps and transitions on a canvas or edit simple JSON to implement a workflow. https://aws.amazon.com/step-functions/   

In the coming months, it is should be possible to use these services to implement batch processing without need to provision, monitor, or maintain clusters of servers.

In the meanwhile, I will describe a more traditional batch processing system using AWS S3, AWS EMR, a scheduler running in a container, notifications via SNS, CloudWatch monitoring, and so forth. The architecture is illustrated in the attached diagram.

Input data sources could include 
1)	An OLTP database, for example a MySQL database hosted on AWS RDS;   
2)	Log data, typically stored as a series of compressed text files in AWS S3; alternatively, a log management system (such as Graylog or an ELK stack) would provide a REST API to retrieve a day’s worth of logs. 
3)	Third-party APIs, which may be called to directly retrieve data in XML or JSON format. Alternatively, third-party systems may be provided a callback, for example the URL of a public-facing API or the path to an AWS S3 bucket, in which to place the data.        

Output systems are depicted on the right of the diagram and include 
a)	a data warehouse such as AWS RedShift or perhaps Snowflake. Data is usually loaded in RedShift from a JSON or CSV file stored in AWS S3 (via the COPY command). 
b)	a queue, such as AWS SQS, or event broker like RabbitMQ. Messages may be queued into SQS by using a AWS SDK (boto3 in Python) or simply by calling the API endpoint.
c)	and finally internal APIs, in this example a HTTP endpoint on an Elastic Load Balancer, which then redistributes calls to one or more EC2 instances in an autoscaling group.        

The batch processing system proper includes 
-	a scheduler / workflow system, which is responsible for scheduling and coordinating   
-	one or more data processing clusters.

Given the amount of data to process, a distributed system is likely required, in order to complete daily processing overnight. 

A commercial or open source scheduler / workflow system, such as Luigi or Pinball, will provide capabilities such as 
-	Storage of the directed acyclic graph (DAG), which encodes the sequence of the various processing steps to be performed, in a simple format, typically a JSON object or a bit of code in a scripting language like Python. This makes creating a workflow or changing a workflow easier.
-	Error and retrying handling.   
-	Start / Stop / Pause capabilities.
-	Cron-like ability to schedule jobs on a regular basis.
-	Possibly the ability to run in parallel portions of the job that are independent of one another, on different servers / clusters.
-	A user interface and dashboard that allows easy monitoring of the progress of each job.

The scheduler, being a relatively lightweight, long-running process, may run alongside a number of other processes - in this example, by hosting it in a Docker container on an existing AWS ECS cluster. 

The separation of the workflow manager and of the compute servers means that, after completion of the daily processing job(s), the compute cluster may be shut down to save costs. In addition, different technologies may be used for different data processing steps.  
In this instance, I chose an AWS Elastic Map Reduce cluster. Such a system can be easily provisioned, manages and autoscales the underlying hardware, and integrates with cheaper Spot instances (interruptible instances).   
A good choice for the distributed data processing software stack may be Apache Spark, which runs off-the-shelf on AWS EMR. It is fast, due to its in-memory computing and lazy evaluation features. Furthermore, Spark is suitable for both batch processing and interactive use (via the DataBricks notebook, for example), which eases code changes and testing. 

In operation, the scheduler would, at a predetermined time, provision a AWS EMR cluster (by running a shell script that calls the AWS CLI, for example). After the cluster becomes available, the scheduler would submit one or more Spark jobs. Each Spark job would read data from one or more data source (e.g. from AS S3 via SparkSession.read or via the appropriate driver), cache and process the data as required, store intermediate data, if required, in a Spark-friendly data format (e.g. Parquet), then ultimately push the final data to one or more data sinks (by calling the appropriate AWS SDK method or sending JSON to a REST API endpoint). After completion of all jobs or after irrecoverable error, the scheduler would then terminate the cluster until the next day.     
Networking components (not detailed for clarity) include a virtual private cloud that isolates private servers and clusters from the Internet; one or more subnets to distribute servers in multiple availability zones for fault tolerance; a NAT gateway to download software patches and updates; an Internet Gateway to public access and a service endpoint, which directly connects internal systems to AWS services without exposing traffic to the public Internet.     
Detailed monitoring of the system may be achieved using AWS tools (CloudTrail to log API calls; CloudWatch to collect and track metrics, collect and monitor log files, and trigger alarms) or purchasing access to a third-party platform, such as NewRelic.  
Notifications about errors and events, such as the processing end, may be relayed to the developer team via SNS (a pub sub system) or SES (an email relay).
Further redundancy and parallelism may be introduced by replicating the system across multiple regions (geographically distributed groups of datacenters). 
If budget permits, the system above may be used in conjunction with a commercial ETL tool e.g. Talend, which would additionally provide a workflow development GUI, a rich library of data processing building blocks and automatic Spark code generation, for ease of developer use.
