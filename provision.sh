#!/usr/bin/env bash
[[ `id -u` -ne 0 ]] && echo 'This script must be run as root user' && exit 1
set -xe

echo 'Updating package cache'
apt-get update -qq

echo 'Installing git and cloning repository'
apt-get install -y git
rm -rf trust-metrics && git clone --depth=2 --branch='fix/includes-dir' https://github.com/IOAyman/trust-metrics
pushd trust-metrics

echo 'Installing python dependencies'
apt-get install -y python-{dev,setuptools,pip} graphviz-dev libglib2.0{,-dev} build-essential tzdata
pip install numpy scipy pyparsing pygnuplot pygraphviz networkx==0.37

echo 'Installing netconv-0.12'
tar xvf netconv-0.12.tar.gz
pushd pynetconv-0.12
python setup.py install
popd

echo 'Installing trustlet'
python setup.py install

echo 'Installing net_flow'
pushd trustlet/net_flow
python setup.py install
popd

popd # trust-metrics
echo 'DONE!'

git clone https://github.com/IOAyman/trust-network-examples.git
pushd trust-network-examples
echo
python simple-trust-network.py -h
echo
python simple-trust-network.py data/users_from_to.csv -o data/users_from_to_results.csv
