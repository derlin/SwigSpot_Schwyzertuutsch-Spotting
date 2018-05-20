package ch.derlin.langid.data

import java.net.URL

import ch.derlin.langid.generated.{Prediction, Version}
import ch.derlin.langid.helpers.{GrpcClient, TextExtractor}

import scala.util.Try


object Result {

  private val urlPattern = "(https?://)?([^\\.]*\\.)*([^\\.]+)\\.ch/?".r

  def apply(url: String, idx: Int, raw_text: String, text: String, result: String, proba: Seq[Double], exname: String, vnum: Int, vdesc: String): Result = {
    val host = new URL(url).getHost
    Result(s"$vnum-$exname|${url.hashCode()}-$idx", host, url, idx, raw_text, text, result, proba, exname, vnum, vdesc)
  }

  def apply(url: String, idx: Int, raw: String, p: Prediction, v: Version): Result =
    Result(url, idx, raw, p.text, GrpcClient.label(p.result), p.proba.map(_.toDouble), TextExtractor.extractorName, v.number, v.description)

  def createId_old(url: String, idx: Int): String = {
    val urlPattern(_, _, domain) = url
    s"$domain-$idx"
  }

  def createId(url: String, idx: Int): String = {
    val url_part = Try {new URL(url)}.toOption match {
      case Some(u) => s"${u.getHost}_${u.hashCode()}"
      case None => url.hashCode
    }
    s"$url_part-$idx"
  }

}

case class Result(_id: Any,
                  domain: String, url: String, idx: Int,
                  raw_text: String, text: String,
                  result: String, proba: Seq[Double],
                  extractor_name: String, version_number: Int, version_description: String,
                  when: java.util.Date = new java.util.Date()) {

  override def toString: String = s"${_id} [$result] ${proba.mkString(", ")}, ${raw_text.take(40)}"
}
