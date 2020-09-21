#!/bin/bash

EX=2
TAR_FILE=project$EX.tar
FILE_LIST='ALU  Add16  FullAdder  HalfAdder  Inc16'

mkdir testTar
cp $TAR_FILE testTar/
cd testTar/
temp=`pwd`

tar -xf $TAR_FILE

find . -iname \*.hdl -exec cp -n {} . \; # find and copy all chips to the current directory
for CHIP in $FILE_LIST; do
  if [ ! -r $CHIP.hdl ]; then
    echo Chip $CHIP was not found
  fi
done

if [ ! -r README ]; then
  README_FILE=`find . -iname 'README*' -print -quit`
  if [[ -n $README_FILE ]]; then
    echo Found $README_FILE, renaming it to README.
    echo I advise you to resubmit with the proper name.
    cp $README_FILE README
    chmod a+r README
  fi
fi

if [ -r README ]; then
  dos2unix README &> /dev/null
  logins=`head -1 README`
  echo Your logins are: $logins, is that ok?
else
  echo No README was found
fi

cd ../
rm -Rf testTar