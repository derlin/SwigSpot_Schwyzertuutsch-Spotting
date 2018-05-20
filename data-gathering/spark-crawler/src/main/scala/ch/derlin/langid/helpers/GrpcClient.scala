package ch.derlin.langid.helpers


import ch.derlin.langid.generated.LangidGrpc.LangidBlockingStub
import ch.derlin.langid.generated._
import io.grpc.{ManagedChannel, ManagedChannelBuilder}


object GrpcClient {
  val labels = Array("de", "fr", "en", "it", "sg")

  def label = labels(_)

  private var client: GrpcClient = _

  // cache client between calls in each JVM
  def get(host: (String, Int) = ("localhost", 50051)): GrpcClient = {
    if (client == null) client = create(host)
    client
  }

  def create(host: (String, Int) = ("localhost", 50051)): GrpcClient =
    new GrpcClient(
      channel = ManagedChannelBuilder.forAddress(host._1, host._2)
        .usePlaintext()
        .build())

}

class GrpcClient(val channel: ManagedChannel) {

  val stub: LangidBlockingStub = new LangidBlockingStub(channel)

  lazy val labels: Seq[String] = stub.getLabels(Empty()).values

  lazy val version: Version = stub.getVersion(Empty())

  def predict(sentence: String, returnText: Boolean = true): Prediction =
    stub.predict(Query(sentence, returnText))

  def predictAll(sentences: Seq[String], returnText: Boolean = true): Seq[Prediction] =
    stub.predictAll(QueryMultiple(sentences, returnText)).predictions


}
