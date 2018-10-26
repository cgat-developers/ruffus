#! /usr/bin/env bash
set -e -u -o pipefail

# parallelism currently fails
# use all cores on test machine
# if [ -z ${TEST_CORES+x} ]; then TEST_CORES=$(nproc); fi
#
# make -k -j ${TEST_CORES} all

make -k all
