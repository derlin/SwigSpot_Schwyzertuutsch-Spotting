package ch.derlin.langid.processing

import ch.derlin.langid.generated.Prediction
import ch.derlin.langid.helpers.{GrpcClient, TextExtractor}

import scala.collection.JavaConverters._

class HtmlPage(client: GrpcClient, val url: String, minWords: Option[Int] = Option.empty[Int]) {

  import de.l3s.boilerpipe.document.TextDocument

  val boilerdoc: TextDocument = TextExtractor.getDoc(url)

  val allSentences: Seq[String] = boilerdoc.getTextBlocks.asScala.map(_.getText).toList

  val sentences: Seq[String] = minWords match {
    case Some(x) => for (s <- allSentences if s.split(" ").length >= x) yield s
    case None => allSentences
  }

  lazy val htmlSentences: Seq[HtmlSentence] =
    sentences.zip(client.predictAll(sentences)).zipWithIndex.map {
      case ((raw: String, Prediction(result, proba, text)), idx: Int) =>
        HtmlSentence(idx, raw, text, client.labels(result), proba)
    }

}


case class HtmlSentence(id: Int, raw_text: String, text: String, result: String, proba: Seq[Float]) {

  def mkString: String = {
    s"$id : $text\n -> $result (probs: ${proba.mkString(", ")})"
  }
}