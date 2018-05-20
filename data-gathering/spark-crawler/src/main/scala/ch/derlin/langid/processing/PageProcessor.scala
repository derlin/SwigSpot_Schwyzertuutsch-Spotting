package ch.derlin.langid.processing

import ch.derlin.langid.data.Result
import ch.derlin.langid.helpers.{GrpcClient, TextExtractor}


class PageProcessor(client: GrpcClient,
                    val url: String,
                    filterSentence: String => Boolean = _ => true,
                    filterResult: Result => Boolean = _ => true) {

  val (sentences: Seq[(String, Int)], title: String, exception: Option[Exception]) = scape
  lazy val results: Seq[Result] = predict

  private def scape = {
    import scala.collection.JavaConverters._
    try {
      val doc = TextExtractor.getDoc(url)
      // by filtering isContent, we avoid getting very bad text such as css, but
      // we also miss some interesting, small sentence...
      // TODO: make a decision !
      // val text = doc.getTextBlocks.asScala.filter(_.isContent).map(_.getText)
      val text = doc.getTextBlocks.asScala.map(_.getText)
      val filtered = text.zipWithIndex.filter(t => filterSentence(t._1))
      (filtered, if (doc.getTitle != null) doc.getTitle else "", None)
    } catch {
      case e: Throwable => (Seq(), "", Some(e))
    }
  }

  private def predict = {
    if (sentences.isEmpty) Seq()
    else {
      val preds = client.predictAll(sentences.map(_._1))
      val res = sentences.zip(preds).map {
        case ((raw, idx), pred) => Result(url, idx, raw, pred, client.version)
      }
      res.filter(filterResult)
    }
  }
}