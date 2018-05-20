"""
langrpc: a langage-detection microservice using GRPC.

The languages supported are: english, german, italian, french and Swiss German.
See the proto file for more information on the available endpoints.

Usage:

    python -m langrpc.server 

An interactive client is also available to tet the API directly using:

    python -m langrpc.client

See the Dockerfile in order to run it inside a docker container.

This module has been created during my Deepening Project (DP)
for the HES-SO Master of Sciences in Computer Science. 
"""

__author__ = "Lucy Linder (lucy.derlin@gmail.com)"
__copyright__ = "Copyright 2018, Lucy Linder"
__license__ = "MIT"
__version__ = "0.2"