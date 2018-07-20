#!/bin/bash
inDir=../MC/Signal/smallified
outDir=preSelectedSignal
first=0
for file in $inDir/*.root ; do
  name=${file##*/}
  echo "$file , $name"
  if [ $first = 0 ]
  then
    python runWgammaPreSelector.py -i "$file" -o "$outDir"/preSelected_"$name"
    first=1
  else
    python runWgammaPreSelector.py -i "$file" -o "$outDir"/preSelected_"$name" -l
  fi

done


