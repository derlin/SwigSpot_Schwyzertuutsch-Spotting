package ch.derlin.langid


import ch.derlin.langid.data.Summary
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

    // the Spark master should be passed as a JVM argument
    val spark = SparkSession
      .builder()
      .appName("SwigSpot -- Spark Crawler")
      .getOrCreate()

    // if specified, use the properties file passed as argument
    // else check for properties defined in the sparkconf
    val conf = if (args.length > 0) Config(args(0)) else Config(spark.sparkContext.getConf)
    // used to rebalance the URLs in case we have more workers than HDFS splits.
    val numExecutors = spark.sparkContext.statusTracker.getExecutorInfos.length
    // start the timer
    log.info(s"beginning crawling ${conf.inpt} (minWords:${conf.minWords}, minProba:${conf.minProba}, executors: $numExecutors)")
    val start = System.currentTimeMillis()
    // read the URL files
    val urls = spark.sparkContext.textFile(conf.inpt)

    // if the input file is very small, there is a good chance that the number of hadoop partitions
    // will be smaller than the number of executors. If we don't repartition the RDD, not all
    // executors will have work to do...
    {if (urls.getNumPartitions > numExecutors) urls else urls.repartition(numExecutors)}
      /* uncomment this line to avoid processing twice the same URL
      .filter(url => {
        val processed = MongoClient.get(conf).isAlreadyProcessed(url)
        if (processed) log.debug(s"$url already processed. Skipping")
        !processed
      })
      */
      .map(new PageProcessor(GrpcClient.get(conf), _, conf.sentenceFilter, conf.resultFilter))
      .foreach { p =>

        val mClient = MongoClient.get(conf)
        var summary = Summary(p)

        if (p.exception.isDefined) {
          // an error occurred during scraping
          log.warn(s"${p.url}: ${p.exception.get}")
        } else if (p.results.nonEmpty) {
          // we got some SG sentences => store the results
          val res = Await.ready(mClient.insertMany(p.results), 1 minute).value.get
          res match {
            case Success(v: Completed) => log.info(s"${p.url}: ${p.results.length} results.")
            // ignore duplicates errors for now
            case Failure(e: com.mongodb.MongoBulkWriteException) => log.warn(s"${p.url}: duplicate error")
            case Failure(e) => summary = summary.copy(ex = e.toString); log.warn(s"${p.url}: $e")
          }
        } else {
          // no Swiss German found
          log.info(s"${p.url}: 0 results.")
        }

        mClient.summaries.insertOne(summary).subscribe(MongoClient.silentObserver)
      }

    // terminate spark context
    // spark.stop() NO ! triggers an error when run on the DAPLAB

    val elapsed = (System.currentTimeMillis - start) / 1000
    printf("URLs processed in %02d minutes %02d seconds", (elapsed / 60) % 60, elapsed % 60)
  }

}
