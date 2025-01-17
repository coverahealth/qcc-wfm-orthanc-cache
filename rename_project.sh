#!/usr/bin/env bash
################################################################################
#
# Copyright (c) 2017-2023 Covera Health (c) 
#
################################################################################

set -eu

while getopts a:n:u: flag
do
    case "${flag}" in
        a) author=${OPTARG};;
        n) name=${OPTARG};;
        u) urlname=${OPTARG};;
    esac
done

echo "Author: $author";
echo "Project Name: $name";
echo "Project URL name: $urlname";

echo "Renaming project..."

# replace references to covera_poetry_template

grep -rli --exclude="*.sh" 'covera-poetry-template' * | xargs -I@ sed -i.bak "s/covera-poetry-template/$urlname/g" @
grep -rli --exclude="*.sh" 'covera_poetry_template' * | xargs -I@ sed -i.bak "s/covera_poetry_template/$name/g" @
find . -type f -name '*.bak' -exec rm "{}" \;

# rename covera_poetry_template dir under src
pushd src
mv covera_poetry_template $name
popd

# This command runs only once on GHA!
if [ -f .github/workflows/rename_project.yml ]; then
    rm -f .github/workflows/rename_project.yml 
fi