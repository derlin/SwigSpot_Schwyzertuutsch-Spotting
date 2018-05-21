package ch.derlin.langid.helpers

import java.net.InetAddress

import ch.derlin.langid.generated.LangidGrpc.LangidBlockingStub
import ch.derlin.langid.generated._
import io.grpc.{ManagedChannel, ManagedChannelBuilder}
import org.apache.log4j.LogManager


object GrpcClient {
  /**
    * The list of labels. Should be equivalent to a call to
    * [[ch.derlin.langid.helpers.GrpcClient.labels]].
    */
  val labels = Array("de", "fr", "en", "it", "sg")

  /**
    * Get the label associated with the given index.
    * @return the text label
    */
  def label = labels(_)

  private var client: GrpcClient = _

  /**
    * Get a GrpcClient, creating it only if it doesn't already exist (Singleton).
    * See the [[ch.derlin.langid.helpers.GrpcClient.create()]] constructor for details about the parameters.
    */
  def get(host: (String, Int) = ("localhost", 50051)): GrpcClient = {
    // cache client between calls in one JVM
    if (client == null) {
      client = create(host)
      LogManager.getLogger(getClass.getName).info(s"Created a new gRPC client on ${InetAddress.getLocalHost}.")
    }
    client
  }

  /**
    * Get a gRPC client using the parameters in the configuration object.
    *
    * @param conf The configuration
    * @return The client.
    */
  def get(conf: Config): GrpcClient = get(conf.grpcHost)


  /**
    * Create an insecure gRPC client using the given server address.
    * @param host the address and port of the server
    * @return the gRPC client
    */
  def create(host: (String, Int) = ("localhost", 50051)): GrpcClient =
    new GrpcClient(
      channel = ManagedChannelBuilder.forAddress(host._1, host._2)
        .usePlaintext()
        .build())

}

class GrpcClient(val channel: ManagedChannel) {

  private val stub: LangidBlockingStub = new LangidBlockingStub(channel)

  /** The language labels. */
  lazy val labels: Seq[String] = stub.getLabels(Empty()).values

  /** The model version used by the server. */
  lazy val version: Version = stub.getVersion(Empty())

  /**
    * Predict the language of a sentence.
    * @param sentence the sentence.
    * @param returnText whether or not to include the sanitized text in the answer.
    * @return The server answer.
    */
  def predict(sentence: String, returnText: Boolean = true): Prediction =
    stub.predict(Query(sentence, returnText))

  /**
    * Same as [[ch.derlin.langid.helpers.GrpcClient.predict()]], but for multiple sentences.
    */
  def predictAll(sentences: Seq[String], returnText: Boolean = true): Seq[Prediction] =
    stub.predictAll(QueryMultiple(sentences, returnText)).predictions

}
