#!/bin/sh
set +eux

curl https://publicsuffix.org/list/public_suffix_list.dat --output plugins/public_suffix_list.dat

git status plugins/public_suffix_list.dat
