#!/bin/sh

[ -z $1 ] && echo "Usage: ./generate_database link_file" && exit 1

[ -d "./dataset" ] || mkdir dataset 

link_file="$1"

for link in $(< $link_file); do
    #firefox "$link"
    ./info.sh "$link"

    name=$(echo $link | cut -d '/' -f7 | tr '-' '_')
    read -r -a wdh <<< $(echo -n $(cut dimentions.txt -d " " -f1))
    final_file=./dataset/"$name"_${wdh[0]}-${wdh[2]}-${wdh[1]}.jpg
    mv img.jpg $final_file
    rm dimentions.txt
    echo "$final_file"
done
