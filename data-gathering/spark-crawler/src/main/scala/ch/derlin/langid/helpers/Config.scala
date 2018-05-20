package ch.derlin.langid.helpers

import java.util.Properties

import ch.derlin.langid.Result
import org.apache.log4j.LogManager
import org.apache.spark.SparkConf

import scala.collection.Map
import scala.io.Source

/**
  * date: 08.04.18
  *
  * @author Lucy Linder <lucy.derlin@gmail.com>
  */
class Config(conf: Map[String, String], defaults: Map[String, String] = Map()) extends java.io.Serializable {

  // log
  LogManager.getLogger(getClass.getName).info(s"Configs:\n   conf: ${conf.mkString(", ")}, defaults: ${conf.mkString(", ")}")

  val grpcHost: (String, Int) = (
    get("spark.grpc.host"),
    get("spark.grpc.port", _.toInt))

  val mongoUrl: String = get("spark.mongo.url")
  val mongoDB: String = get("spark.mongo.db")
  val mongoColl: String = get("spark.mongo.collection")
  val mongoSummaryColl: String = get("spark.mongo.summaryCollection")

  val minProba: Double = get("spark.result.minProba", _.toDouble)
  val minWords: Int = get("spark.result.minWords", _.toInt)

  val inpt = conf("spark.input.file")


  def sentenceFilter: String => Boolean = _.split(" ").length >= minWords

  def resultFilter: Result => Boolean = p => p.text.split(" ").length >= minWords && p.proba.last >= minProba


  private def get[A](key: String, convert: String => A = identity[String] _): A = {
    convert(conf.getOrElse(key, defaults(key)))
  }
}

object Config {

  import scala.collection.JavaConverters._

  def apply(conf: Any): Config = conf match {
    case null => new Config(defaultConfig)
    case map: Map[String, String]@unchecked => new Config(map, defaultConfig)
    case props: Properties => new Config(props.asScala.toMap, defaultConfig)
    case conf: SparkConf => new Config(conf.getAll.toMap, defaultConfig)
    case filepath: String => {
      val p = new Properties()
      p.load(Source.fromFile(filepath).reader())
      Config(p)
    }
    case _ => throw new IllegalArgumentException("unknown type for config")
  }

  lazy val defaultConfig: Map[String, String] = {
    val p = new Properties()
    p.load(getClass.getResourceAsStream("/default_config.properties"))
    p.asScala.toMap
  }
}