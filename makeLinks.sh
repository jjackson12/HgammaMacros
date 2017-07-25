rm -rf organize_smallifications
mkdir organize_smallifications
cd organize_smallifications
mkdir backgrounds
cd backgrounds
for i in `ls ../../smallifications_May2/ | grep .root | grep -v data`; do ln -s ../../smallifications_May2/$i $i; done
cd ..
mkdir data
cd data
for i in `ls ../../smallifications_May2/ | grep .root | grep data`; do  ln -s ../../smallifications_May2/$i $i; done
cd ..
mkdir signals
cd signals
for i in `ls -1v ../../../HgammaCondor | grep smallified_sig`; do ln -s ../../../HgammaCondor/$i $i; done
cd ..
