# Protos

This directory contains the protobuf description implemented by the langid-microservice and used by the spark-crawler.

Open `doc.html` in a browser for the documentation. The former has been generated using [protoc-gen-doc](https://github.com/pseudomuto/protoc-gen-doc):

```bash
docker run --rm \
  -v $(pwd):/out \
  -v $(pwd)/langrpc:/protos \
  pseudomuto/protoc-gen-doc --doc_opt=html,doc.html
```