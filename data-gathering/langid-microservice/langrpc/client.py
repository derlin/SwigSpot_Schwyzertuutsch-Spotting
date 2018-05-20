# -*- coding: utf-8 -*-

import grpc 
import sys 

# import the generated classes
from . import langid_pb2 as pb
from . import langid_pb2_grpc as pbg


# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = pbg.LangidStub(channel)
labels = stub.GetLabels(pb.Empty()).values

version = stub.GetVersion(pb.Empty())
print("LANGID version %d: %s\n" % (version.number, version.description))

while True:
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline().strip()
    if sentence in ['exit', 'stop']:
        print("Bye!")
        sys.exit(0)

    elif sentence != "":
        # make the call
        response = stub.Predict(pb.Query(sentence=sentence, return_text=True))
        # et voilà
        print(response.text)
        print("\n --> %s\n" % labels[response.result])
        for i in sorted(zip(labels, response.proba), key=lambda t: -t[1]):
            print("     %s: %g" % i)
        print()
    else:
        print("Hum, expecting an actual sentence.\n")