package ch.derlin.langid


import ch.derlin.langid.helpers.{Config, GrpcClient, MongoClient}
import ch.derlin.langid.processing.PageProcessor
import org.apache.log4j.LogManager
import org.apache.spark.sql.SparkSession
import org.mongodb.scala.Completed

import scala.concurrent.Await
import scala.concurrent.duration._
import scala.util.{Failure, Success}

object Sparky {

  val log = LogManager.getLogger(getClass.getName)

  def main(args: Array[String]) {


    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .getOrCreate()

    // if specified, use the properties file passed as argument
    // else check for properties defined in the sparkconf
    val conf = if (args.length > 0) Config(args(0)) else Config(spark.sparkContext.getConf)
    // used to rebalance the URLs in case we have more workers than HDFS splits.
    val numExecutors = spark.sparkContext.statusTracker.getExecutorInfos.length

    log.info(s"beginning crawling ${conf.inpt} (minWords:${conf.minWords}, minProba:${conf.minProba}, executors: $numExecutors)")
    val start = System.currentTimeMillis()

    val urls = spark.sparkContext.textFile(conf.inpt)

    // if the input file is very small, there is a good chance that the number of hadoop partitions
    // will be smaller than the number of executors. If we don't repartition the RDD, not all
    // executors will have work to do...
    {if (urls.getNumPartitions > numExecutors) urls else urls.repartition(numExecutors)}
      .foreachPartition(urls => {

        val gClient = GrpcClient.get(conf.grpcHost)
        val mClient = MongoClient.get(conf.mongoUrl, conf.mongoDB, conf.mongoColl, conf.mongoSummaryColl)

        urls
          /* uncomment this line to avoid processing twice the same URL *
          .filter(url => {
            val processed = mClient.isAlreadyProcessed(url)
            if (processed) log.debug(s"$url already processed. Skipping")
            !processed
          })
          */
          .map(new PageProcessor(gClient, _, conf.sentenceFilter, conf.resultFilter))
          .foreach { p =>
            var summary = Summary(p, gClient.version)

            if (p.exception.isDefined) {
              log.warn(s"${p.url}: ${p.exception.get}")

            } else if (p.results.nonEmpty) {
              val res = Await.ready(mClient.insertMany(p.results), 1 minute).value.get
              res match {
                case Success(v: Completed) => log.info(s"${p.url}: ${p.results.length} results.")
                // ignore duplicates errors for now
                case Failure(e: com.mongodb.MongoBulkWriteException) => log.warn(s"${p.url}: duplicate error")
                case Failure(e) => summary = summary.copy(ex = e.toString); log.warn(s"${p.url}: $e")
              }
            } else {
              log.info(s"${p.url}: 0 results.")
            }

            mClient.summaries.insertOne(summary).subscribe(MongoClient.silentObserver)
          }
      }

      )

    // terminate spark context
    // spark.stop() (triggers an error when run on the DAPLAB

    val elapsed = (System.currentTimeMillis - start) / 1000
    printf("URLs processed in %02d minutes %02d seconds", (elapsed / 60) % 60, elapsed % 60)
  }

}
