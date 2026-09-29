#!/usr/bin/env bash
./scripts/rebuild-docs.sh
echo "Serving site"
bundle exec jekyll serve --incremental
