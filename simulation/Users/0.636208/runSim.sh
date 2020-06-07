#!/bin/sh
cd simulation
cd Users
cd $3
make  micaz sim
python MySimulation.py $1 $2
