#!/bin/bash
# check for git update
git fetch
NEW_COMMITS="$(git rev-list HEAD...origin/master --count)"

if [[ $NEW_COMMITS > 0 ]]; then
    git pull
fi

python /root/hexacat/hexacat.py
