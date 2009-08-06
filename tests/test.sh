#!/bin/sh

BIN_DIR="`pwd`/.."

setup() {
	echo "preparing testing..."

	for tool in ${BIN_DIR}/gg-*; do
		tool_name=`basename ${tool}`
		cp ${tool} stubs/${tool_name}.test
	done
}

teardown() {
	echo "cleaning up..."

	rm stubs/gg-*.test
}

setup



teardown
