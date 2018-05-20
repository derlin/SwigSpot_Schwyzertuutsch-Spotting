lazy val root = (project in file(".")).
  settings(
    name := "spark-crawler",
    organization := "ch.derlin.langid",
    version := "1.0",
    scalaVersion := "2.11.8",
    mainClass in Compile := Some("ch.derlin.langid.Sparky")
  )

// -- boilerpipe
//libraryDependencies += "com.syncthemall" % "boilerpipe" % "1.2.2"
libraryDependencies += "com.robbypond" % "boilerpipe" % "1.2.3"

// -- spark
val sparkVersion = "2.1.1"
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion % Provided,
  "org.apache.spark" %% "spark-sql" % sparkVersion % Provided
)

// -- gRPC
// https://mvnrepository.com/artifact/com.google.protobuf/protobuf-java
// TODO: still needed ?
libraryDependencies ++= Seq(
  //  "com.google.protobuf" % "protobuf-java" % "3.5.1",
  //  "com.google.protobuf" % "protobuf-java" % "3.5.1",
  //  "io.grpc" % "grpc-stub" % "1.11.0",
  //  "io.grpc" % "grpc-protobuf" % "1.11.0",
  "io.grpc" % "grpc-netty-shaded" % "1.11.0",
  "com.google.guava" % "guava" % "20.0"

)
// -- mongo
// see http://mongodb.github.io/mongo-scala-driver/2.1/getting-started/installation-guide/
libraryDependencies += "org.mongodb.scala" %% "mongo-scala-driver" % "2.1.0"

// -- scala protobuf
// see https://scalapb.github.io
resolvers += Resolver.url("bintray-sbt-plugins", url("http://dl.bintray.com/sbt/sbt-plugin-releases"))(Resolver.ivyStylePatterns)
libraryDependencies += "com.thesamet.scalapb" %% "scalapb-runtime-grpc" % scalapb.compiler.Version.scalapbVersion
// scalapb configuration (see project/scalapb.sbt)
// Changing where to look for protos to compile (default src/main/protobuf):
PB.protoSources in Compile := Seq(file("../protos"))
// run sbt proto-generate (or protoGenerate in the sbt shell on IntelliJ) to generate the proto
// note: flatPackage => don't append the project name to the package
PB.targets in Compile := Seq(
  scalapb.gen(flatPackage = true) -> (sourceManaged in Compile).value
)




/* without this explicit merge strategy code you get a lot of noise from sbt-assembly
   complaining about not being able to dedup files */
assemblyMergeStrategy in assembly := {
  case PathList("org", "aopalliance", xs@_*) => MergeStrategy.last
  case PathList("javax", "inject", xs@_*) => MergeStrategy.last
  case PathList("javax", "servlet", xs@_*) => MergeStrategy.last
  case PathList("javax", "activation", xs@_*) => MergeStrategy.last
  case PathList("org", "apache", xs@_*) => MergeStrategy.last
  case PathList("com", "google", xs@_*) => MergeStrategy.last
  case PathList("com", "esotericsoftware", xs@_*) => MergeStrategy.last
  case PathList("com", "codahale", xs@_*) => MergeStrategy.last
  case PathList("com", "yammer", xs@_*) => MergeStrategy.last

  case PathList("org", "cyberneko", xs@_*) => MergeStrategy.last

  case "about.html" => MergeStrategy.rename
  case "META-INF/ECLIPSEF.RSA" => MergeStrategy.last
  case "META-INF/mailcap" => MergeStrategy.last
  case "META-INF/mimetypes.default" => MergeStrategy.last
  case "plugin.properties" => MergeStrategy.last
  case "log4j.properties" => MergeStrategy.last
  case "overview.html" => MergeStrategy.last // Added this for 2.1.0 I think
  case x if x.endsWith("io.netty.versions.properties") => MergeStrategy.first
  case x =>
    val oldStrategy = (assemblyMergeStrategy in assembly).value
    oldStrategy(x)
}

assemblyShadeRules in assembly := Seq(
  ShadeRule.rename("com.google.common.**" -> "my_conf.@1").inAll
)

/* including scala bloats your assembly jar unnecessarily, and may interfere with
   spark runtime */
assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)
assemblyJarName in assembly := "spark-langid.jar"

/* you need to be able to undo the "provided" annotation on the deps when running your spark
   programs locally i.e. from sbt; this bit reincludes the full classpaths in the compile and run tasks. */
fullClasspath in Runtime := (fullClasspath in(Compile, run)).value