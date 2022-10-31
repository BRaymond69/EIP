#!/bin/sh

[[ ! -f extracted_page.html ]] && echo "Usage: copy paste the page's content in extracted_page.html" && exit 1

grep -oe "https://www.ikea.com/fr/fr/p/[0-9a-zA-Z_-]*/" extracted_page.html | sort | uniq

# URLS we have done so far:
# https://www.ikea.com/fr/fr/cat/commodes-et-caissons-a-tiroirs-st004/?page=100
