package ch.derlin.langid.helpers

import java.io.{IOException, InputStream}
import java.net.URL
import java.nio.charset.{Charset, CodingErrorAction}
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.util.zip.GZIPInputStream

import javax.net.ssl._

import scala.xml.InputSource

/**
  *
  * An object to fetch HTML resources.
  *
  * Features:
  *  - HTTP and HTTPS support
  *  - unsecure SSL certificates support
  *  - GZIP compression
  *
  * Note that it will only work for text/HTML resources.
  *
  * date: 19.04.18
  *
  * @author Lucy Linder <lucy.derlin@gmail.com>
  */
object HTMLFetcher {

  // TODO guess encoding !!!
  // see http://mvnrepository.com/artifact/org.codehaus.guessencoding/guessencoding/1.4

  trustAllHttpsCertificates()

  private val charsetPattern = "charset=\"?([^;\" ]+)".r
  private val defaultCharset = Charset.forName("Cp1252")
  private val timeoutMillis = 10000

  implicit def stringToURL(u: String): URL = new URL(u)

  /**
    * Fetch an HTML resource. Example usage:
    * {{{
    * val is = fetchAsInputSource(url)
    * val doc = new BoilerpipeSAXInput(is).getTextDocument()
    * }}}
    *
    * @param url the url
    * @return an InputSource ready to use for a [[de.l3s.boilerpipe.sax.BoilerpipeSAXInput]] :)
    */
  @throws(classOf[java.io.IOException])
  def fetchAsInputSource(url: URL): InputSource = {
    val (fetched, charset) = fetch(url)
    val is = new InputSource(fetched)
    is.setEncoding(charset.name())
    is
  }

  /**
    * Fetch an HTML resource.
    *
    * @param url the url
    * @return a tuple (html content as string, charset)
    */
  @throws(classOf[java.io.IOException])
  def fetchAsText(url: URL): (String, Charset) = {
    val (is, charset) = fetch(url)
    // ignore invalid characters
    val decoder = charset.newDecoder()
    decoder.onMalformedInput(CodingErrorAction.IGNORE)
    (scala.io.Source.fromInputStream(is)(decoder).mkString, charset)
  }

  // fetch and return as simple inputStream
  @throws(classOf[java.io.IOException])
  def fetch(url: URL): (InputStream, Charset) = {

    val conn = url.openConnection()
    conn.setRequestProperty("Accept-Encoding", "gzip")

    // set some timeouts, see
    // https://eventuallyconsistent.net/2011/08/02/working-with-urlconnection-and-timeouts/
    conn.setConnectTimeout(timeoutMillis)
    conn.setReadTimeout(timeoutMillis)

    val contentType = conn.getContentType

    if (contentType == null)
      throw new IOException(s"Content type is null. $url might be unreachable.")
    if (!contentType.contains("text/html"))
      throw new Exception(s"Unsupported content type: $contentType")

    val charset = charsetPattern.findFirstMatchIn(contentType) match {
      case Some(c) => Charset.forName(c.group(1).toLowerCase)
      case None => defaultCharset
    }

    val encoding = conn.getContentEncoding
    val is = if (encoding != null && encoding.toLowerCase == "gzip")
      new GZIPInputStream(conn.getInputStream)
    else conn.getInputStream

    (is, charset)
  }

  // Make the URL#getConnection accept unsecure HTTPS certificates as well to avoid
  // `java.net.ssl.SSLHandshakeException`. Just call it once per JVM.
  // see http://www.rgagnon.com/javadetails/java-fix-certificate-problem-in-HTTPS.html for more details
  private def trustAllHttpsCertificates(): Unit = {
    val dummyTrustManagers = Array[TrustManager](new X509TrustManager() {

      def getAcceptedIssuers: Array[X509Certificate] = null

      override def checkClientTrusted(x509Certificates: Array[X509Certificate], s: String): Unit = {}

      override def checkServerTrusted(x509Certificates: Array[X509Certificate], s: String): Unit = {}
    })

    val sc = SSLContext.getInstance("SSL")
    sc.init(null, dummyTrustManagers, new SecureRandom)
    HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory)

    // Create and install all-trusting host name verifier
    HttpsURLConnection.setDefaultHostnameVerifier(new HostnameVerifier {
      override def verify(s: String, sslSession: SSLSession): Boolean = true
    })
  }


}
