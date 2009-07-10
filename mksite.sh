#!/bin/sh
#
# Script to generate up-to-date version of the site / bogorodskiy@gmail.com

if test "x$1" = "x"; then
	echo "you must specify password"
	exit 1
fi

PASSWORD="$1"

URL="http://novel.evilcoder.org/gg/"
SITEDIR="site"
VERSION=`grep version setup.py|sed 's|^[ ]*version[ ]*\=[ ]*"\(.*\)".|\1|'`
DIST="gg-${VERSION}.tar.gz"

mkdir -p ${SITEDIR}/dist 2>&1 > /dev/null
mkdir -p ${SITEDIR}/docs/${VERSION}/

echo "creating dist..."

python setup.py sdist

mv dist/${DIST}  ${SITEDIR}/dist

echo "generating documentation..."

epydoc --html -n GoGridManager -u ${URL} --graph=all -o ${SITEDIR}/docs/${VERSION}/ GoGridManager

echo "generating index.html..."

sed "s|%%VERSION%%|${VERSION}|g" website/index.html > ${SITEDIR}/index.html
cp website/gg.css ${SITEDIR}/

lftp -u novel,${PASSWORD} -e "mirror --reverse --verbose ${SITEDIR} public_html/gg" novel.evilcoder.org
