

A good tutorial on gRPC is [here](https://engineering.semantics3.com/a-simplified-guide-to-grpc-in-python-6c4e25f0c506).


## Setup

Create the virtualenv and install the deps:

```bash
virtualenv -p python3 venv
source venv/bin/activate # or .\venv\Scripts\activate on Windows
```

Launch the server:

```bash
python -m langrpc.server
```

Run the client:

```bash
python -m langrpc.client
```

## Generate the python proto files

From the here (where this readme resides), run:

```bash
python -m grpc_tools.protoc \
    -I../protos \
    --python_out=. \
    --grpc_python_out=. \
    ../protos/langrpc/*.proto
```

__Important__: the proto files are in the parent directory because they are also used by the Spark (scala/sbt) program.
In python, the module is determined by the location of the proto files, so it is important that the `langid.proto` be inside a `langrpc` directory to work. So in short, don't change the line above. 

## Generate clients for other languages

For example, say you want to communicate with the server in Java. To simplify, you can install a docker image containing the `protoc` executable:

```bash
docker pull znly/protoc
```

The protoc command is the following (don't forget the `--grpc-java_out` to also generate the grpc stub):

```bash
/protoc --grpc-java_out=. --java_out=. -I. langid.proto
```

Using docker on Windows:

```bash
docker run --rm -v %cd%:/user/app -w /user/app znly/protoc --grpc-java_out=. --java_out=. -I. langid.proto
```

For linux and mac simply replace `%cd%` with `$(pwd)` (or `${PWD}` in PowerShell). The generated java files can then be imported to your project (just beware of the package, which cannot be changed. If no package is set, simply put the generated files at the root).

## Run on Docker containers

First, build the image using the available `Dockerfile` :

```shell
docker build -t langrpc --rm .
```

Launch the server:
```shell
docker run --rm -d -p 50051:50051 langrpc
```
Done.

You can also run the client (interactive mode) on Docker using:
```shell
docker run -it --rm --net=host langrpc python -m langrpc.client
```
__Important__: don't forget the `--net=host` so that the client container
can connect to the server using the host as a bridge.
