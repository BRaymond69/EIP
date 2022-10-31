#!/bin/sh

[ -z $1 ] && echo "Usage: ./info.sh url" && exit 1

url="$1"
curl -s "$url" > page.html
img_url=$(grep ".JPG" page.html | head -n3 | tail -n1 | cut -d " " -f 3)

curl -s "$img_url" > img.jpg
grep "Largeur" page.html | tr '<' '\n' | tr '>' '\n' | grep "cm$" | grep -A3 x | head -n4 | tail -n3 > dimentions.txt
rm page.html

#echo $url
#cat dimentions.txt
#eog img.jpg
