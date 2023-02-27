#!/usr/bin/env bash

set -e

rm -rf bin/artm*
rm -rf bin/pulum*
rm bin/requirements.txt || true
rm bin/run-provider.py || true
rm -rf dist/
rm -rf provider/cmd/pulumi-resource-artmazure/artmazure_provider.egg-info
rm -rf provider/cmd/pulumi-resource-artmazure/build
rm -rf sdk/

make generate
make build
make dist

pulumi plugin rm resource artmazure -y
pulumi plugin install resource artmazure 0.0.1 --file dist/pulumi-resource-artmazure-v0.0.1-linux-amd64.tar.gz --

chmod 777 -R ~/.pulumi/