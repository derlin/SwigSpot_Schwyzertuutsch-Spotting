package ch.derlin.langid.helpers

import java.io.StringReader

import de.l3s.boilerpipe.document.TextDocument
import de.l3s.boilerpipe.extractors.{ArticleSentencesExtractor, ExtractorBase}
import de.l3s.boilerpipe.sax.BoilerpipeSAXInput

import scala.collection.JavaConverters._
import scala.xml.InputSource

object TextExtractor {

  val extractor: ExtractorBase = ArticleSentencesExtractor.INSTANCE
  val extractorName: String = extractor.getClass.getSimpleName.filter(_.isUpper).mkString

  def getText: String => String = getDoc(_: String).getText(true, false)

  def getTextBlocks: String => Seq[String] = getDoc(_: String).getTextBlocks.asScala.map(t => t.getText)

  def getDoc(url: String): TextDocument = {
    import HTMLFetcher._
    // Using fetchAsText instead of:
    // ```
    // val is = fetchAsInputSource(url)
    // val doc = new BoilerpipeSAXInput(is).getTextDocument()
    // ```
    // seems useless as it adds mkString step,
    // but using this we are able to decide what happens on malformed inputs (i.e. characters that cannot be
    // decoded using the current charset). Indeed, HTMLFetcher.fetchAsText ignores wrong inputs (vs the boilerpipe
    // inputSource decoded), thus avoiding strange characters in the texts...
    val (txt, _) = fetchAsText(url)
    val doc = new BoilerpipeSAXInput(new InputSource(new StringReader(txt))).getTextDocument()
    extractor.process(doc)
    doc
  }

}