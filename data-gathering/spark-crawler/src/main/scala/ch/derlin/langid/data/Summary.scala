package ch.derlin.langid.data

import java.util.Date

import ch.derlin.langid.generated.Version
import ch.derlin.langid.helpers.TextExtractor
import ch.derlin.langid.processing.PageProcessor
import org.mongodb.scala.bson.ObjectId

/**
  * date: 20.04.18
  *
  * @author Lucy Linder <lucy.derlin@gmail.com>
  */


object Summary {
  val maxExceptionLength = 100

  def apply(p: PageProcessor, v: Version): Summary = Summary(p.url, p.sentences.length, p.results.length, p.exception, v)

  def apply(url: String, cnt: Int, sg: Int, ex: Option[Throwable], v: Version): Summary =
    Summary(new ObjectId(), url, cnt, sg,
      ex match { case Some(e) => e.toString.take(maxExceptionLength).mkString; case None => "" }, new Date(),
      v.number, v.description, TextExtractor.extractorName)
}

case class Summary(_id: ObjectId, url: String, cnt: Int, sg: Int, ex: String, when: Date,
                   model_version: Int, model_version_descr: String, extractor: String) {
  override def toString: String = s"$url (sg: $sg/$cnt) $ex"
}
