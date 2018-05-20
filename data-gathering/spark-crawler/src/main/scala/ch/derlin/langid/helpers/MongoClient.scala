package ch.derlin.langid.helpers


import ch.derlin.langid.{Result, Summary}
import org.mongodb.scala.{Completed, Observer}

import scala.concurrent.{Await, Future}

/**
  * A singleton wrapper for the [[ch.derlin.langid.helpers.MongoClient]].
  */
object MongoClient {

  private var client: MongoClient = _   // The singleton

  /**
    * Get a MongoClient, creating it only if it doesn't already exist (Singleton).
    * See the [[ch.derlin.langid.helpers.MongoClient]] constructor for details about the parameters.
    */
  def get(connectionUrl: String, dbName: String, collectionName: String, summaryCollectionName: String = "log"): MongoClient = {
    if (client == null) client = new MongoClient(connectionUrl, dbName, collectionName, summaryCollectionName)
    client
  }

  /**
    * An observer printing to the console on error, next and complete events.
    * Example usage:
    * {{{
    * mongoClient.collection
    *   .insert(result)
    *   .subscribe(printlnObserver)
    * }}}
    */
  def printlnObserver: Observer[Completed] = new Observer[Completed] {
    override def onError(e: Throwable): Unit = System.err.println("Insertion failed", e)

    override def onNext(result: Completed): Unit = println("Inserted")

    override def onComplete(): Unit = println("Completed")
  }

  /**
    * An observer that triggers the action, but does on complete.
    * (The mongo client methods are most of the time lazy, so you need an observer to
    * actually do your thing).
    * Example usage:
    * {{{
    * mongoClient.collection
    *   .insert(result)
    *   .subscribe(silentObserver)
    * }}}
    */
  def silentObserver: Observer[Completed] = new Observer[Completed] {
    override def onError(e: Throwable): Unit = {}

    override def onNext(result: Completed): Unit = {}

    override def onComplete(): Unit = {}
  }

}

/**
  * A MongoDB client especially made for storing [[ch.derlin.langid.Result]] and [[ch.derlin.langid.Summary]].
  *
  * @param connectionUrl         the mongo url, for example `mongodb://localhost:27017`
  * @param dbName                the name of the mongo database, for example `sg`
  * @param collectionName        the name of the collection used to store the [[ch.derlin.langid.Result]], for example `sentences`
  * @param summaryCollectionName the name of the collection used to store the [[ch.derlin.langid.Summary]], for example `log`
  * @return the mongo client
  */
class MongoClient(connectionUrl: String, dbName: String, collectionName: String, summaryCollectionName: String) {

  import org.bson.codecs.configuration.CodecRegistries.{fromProviders, fromRegistries}
  import org.mongodb.scala._
  import org.mongodb.scala.bson.codecs.DEFAULT_CODEC_REGISTRY
  import org.mongodb.scala.bson.codecs.Macros._

  // The client and the database configured with the right codecs
  val (client, database) = initClient
  // The collection for the results
  val collection: MongoCollection[Result] = database.getCollection(collectionName)
  // The collection for the logs, i.e. informations about a processed URL
  val summaries: MongoCollection[Summary] = database.getCollection(summaryCollectionName)


  /** Close the mongo client connection. */
  def close(): Unit = client.close()

  /** Insert a one Result and return a future. */
  def insert: Result => Future[Completed] = collection.insertOne(_).toFuture

  /** Insert a sequence of Result and return a future. */
  def insertMany: Seq[Result] => Future[Completed] = collection.insertMany(_).toFuture

  /**
    * Checks if the given URL is already present in the summary collection.
    *
    * @param url the url
    * @return True if the URL has been processed, false otherwise
    */
  def isAlreadyProcessed(url: String): Boolean = {
    import org.mongodb.scala.model.Filters._
    import scala.concurrent.duration._

    // don't use case class here, since old records have different fields...
    val req = database.getCollection(summaryCollectionName).find(equal("url", url)).first()
    val result = Await.result(req.toFuture(), 1 minute)
    result != null
  }

  // Initialise the client with the right codecs
  private def initClient: (org.mongodb.scala.MongoClient, org.mongodb.scala.MongoDatabase) = {
    import org.bson.codecs.configuration.CodecRegistries
    import org.bson.codecs.DateCodec
    // configure the client to handle Result objects
    // see http://mongodb.github.io/mongo-scala-driver/2.1/getting-started/quick-tour-case-classes/
    // and http://www.jannikarndt.de/blog/2017/08/writing_case_classes_to_mongodb_in_scala/
    val customCodecs = fromProviders(classOf[Result], classOf[Summary])
    val javaCodecs = CodecRegistries.fromCodecs(new DateCodec())
    val codecRegistry = fromRegistries(customCodecs, javaCodecs, DEFAULT_CODEC_REGISTRY)

    val client = org.mongodb.scala.MongoClient(connectionUrl)
    val database = client.getDatabase(dbName).withCodecRegistry(codecRegistry)

    (client, database)
  }

}
