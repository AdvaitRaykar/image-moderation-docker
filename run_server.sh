#!/usr/bin/env bash
docker run --rm -ti  -p 5000:5000 caffe:cpu  python server.py 5000