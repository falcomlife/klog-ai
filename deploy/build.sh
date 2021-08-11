#!/bin/bash
set -e

docker build -t swr.cn-north-4.myhuaweicloud.com/cotte-bigdata/python-base:3.8.5 -f Dockerfile-base .

cd ..
python -m build
cd deploy

rm -rf ./src
cp -rf ../src ./src/
version=`date +%s`
echo 'version '$version' image buliding...'
docker build -t swr.cn-north-4.myhuaweicloud.com/cotte-bigdata/analy:0.0.$version -f Dockerfile .
docker push swr.cn-north-4.myhuaweicloud.com/cotte-bigdata/analy:0.0.$version