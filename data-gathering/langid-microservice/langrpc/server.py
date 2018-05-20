# -*- coding: utf-8 -*-

import grpc
from concurrent import futures
import time

# import the generated classes
from . import langid_pb2 as pb
from . import langid_pb2_grpc as pbg

# import the original langid.py
from .langid import langid

# create a class to define the server functions
class LangidServicer(pbg.LangidServicer):

    def GetVersion(self, request, context):
        return pb.Version(number = langid.VERSION_NUMBER, 
            description = langid.VERSION_DESCRIPTION)

    def GetLabels(self, request, context):
        return pb.Labels(values = langid.LABELS)

    def Predict(self, request, context):
        (s, result, proba) = langid.predict(request.sentence)
        if request.return_text:
            return pb.Prediction(result=result, proba=proba, text=s)
        else:
            return pb.Prediction(result=result, proba=proba)

    def PredictAll(self, request, context):
        (ss, results, probas) = langid.predict_all(request.sentences)
        response = pb.Predictions()

        if not request.return_text:
            for (res, proba) in zip(results, probas):
                response.predictions.add(result=res, proba=proba)
        else:
            for (s, res, proba) in zip(ss, results, probas):
                response.predictions.add(result=res, proba=proba, text=s)
        return response


def run(port=50051):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_CalculatorServicer_to_server`
    # to add the defined class to the server
    pbg.add_LangidServicer_to_server(LangidServicer(), server)

    # listen on port 50051
    print('Starting server. Listening on port %d.' % port)
    server.add_insecure_port('[::]:%d' % port)
    server.start()

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    run()