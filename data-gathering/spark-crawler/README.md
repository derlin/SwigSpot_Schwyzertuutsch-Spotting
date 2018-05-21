# Spark Crawler

This scala Spark program crawls a list of URLs and save the Swiss German sentences found into a MongoDB database.

## Dependencies

This program needs a valid MongoDB connection and and _langid-microservice_ to run.

## Launch

#### Config

In the `config.properties` file, set the `spark.input.file` property to the file containing the URLs. 

```properties
# if the file in in local filesystem, specifiy the absolute path
spark.input.file=file:///home/user/urls.txt
# if the file in on HDFS, use either absolute or relative path
spark.input.file=/link/to/hdfs/folder/urls.txt
```

#### Build

To build the project, use the `sbt` utility: `sbt assembly`. This will create the jar artifact in the `target` directory.

To create the GRPC protos manually (they are usually constructed automatically on build), use `sbt gen-protos`.

#### Run locally

It is possible to run Spark in memory.

From _IntelliJ_, create a new run configuration and add the following properties:

- Main class: `ch.derlin.langid.Sparky`
- VM options: `-Dspark.master=local`
- Program arguments: `config.properties`

You can now run the code directly from the IDE.

From a _terminal_, ensure you have the scala library in your classpath and use the following:

```bash
sbt assembly

java -jar -Dspark.master=local target/scala-2.11/spark-langid.jar config.properties
```

#### Run on Hadoop/yarn

In a nutshell: 

1. Copy the jar to the cluster.
2. Put the text file containing the URLs in HDFS.
3. Edit the `config.properties` to match the file.
4. use `spark-submit` to launch the job.

__spark-submit__: the only required options are the spark master to use and the path to the `config.properties` file. A basic launch is:

```bash
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --properties-file=$basedir/config.properties \
    spark-langid.jar
``` 

For performance reasons, you will want at least to tune the number of executors (`--num-executors`). Another nice thing is the ability to change the default log level. For that, create a `log4j.properties` file and pass it to `spark-submit` using the options below:
```bash
spark-submit \
   --files "/absolute/path/on/driver/machine/log4j.properties" \
   --driver-java-options "-Dlog4j.configuration=log4j.properties" \
   --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=log4j.properties" \
   ...
```
Note that the first option needs an absolute path, while the others can be left as is.

__rsyslog__: see the `log4j-rsyslog.poperties` file in this directory for an example of log4j properties using an rsyslog facility. This is especially useful in a cluster, as the logs are usually fetched from the workers _after_ the end of the execution...

#### Run on the DAPLAB

A `submit.sh` script for the DAPLAB is shown below. The `wn3x` queue is specific to this cluster. Otherwise, it can be reused elsewhere:

```bash
master=yarn
mode=cluster
log4j=log4j.properties
basedir=/data1/langid  # change it
num_executors=3        # to customise

export SPARK_MAJOR_VERSION=2

spark-submit \
   --files "$basedir/$log4j" \
   --driver-java-options "-Dlog4j.configuration=$log4j" \
   --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=$log4j" \
   --properties-file=$basedir/config.properties \
   --master $master \
   --deploy-mode $mode \
   --num-executors $num_executors \
   --queue wn3x \
   spark-langid.jar
```

