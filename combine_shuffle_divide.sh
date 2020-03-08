echo "combine all csv to one"
mkdir ./WikiTrain19/tagged_data/data/
cat ./WikiTrain19/tagged_data/*.csv > ./WikiTrain19/tagged_data/data/total.csv

echo "change B,I to B_MISC,I_MISC"
sed -i "s/# /B_MISC /g" ./WikiTrain19/tagged_data/data/total.csv
sed -i "s/@ /I_MISC /g" ./WikiTrain19/tagged_data/data/total.csv
sed -i "s/#,/B_MISC,/g" ./WikiTrain19/tagged_data/data/total.csv
sed -i "s/@,/I_MISC,/g" ./WikiTrain19/tagged_data/data/total.csv

echo "shuffle data"
awk 'BEGIN{ 26494*srand();}{ printf "%s %s\n", rand(), $0}' ./WikiTrain19/tagged_data/data/total.csv |sort -k1n | awk '{gsub($1FS,""); print $0}' > ./WikiTrain19/tagged_data/data/total_shuffle.csv

echo "divide in to train/test/valid"
sed -n '1,2600p' ./WikiTrain19/tagged_data/data/total_shuffle.csv > ./WikiTrain19/tagged_data/data/test.csv
sed -n '2601,5200p' ./WikiTrain19/tagged_data/data/total_shuffle.csv > ./WikiTrain19/tagged_data/data/valid.csv
sed -n '5201,$p' ./WikiTrain19/tagged_data/data/total_shuffle.csv > ./WikiTrain19/tagged_data/data/train.csv

echo "Done"
