#!/usr/bin/env bash

HEADER="## Sections"

# create blank sections in README.md
sed "/${HEADER}/,$ d" -i README.md
echo "${HEADER}" >> README.md

# fill sections
sections=$(find . -maxdepth 1 -type d ! -name '.*')
for section_dir in $sections
do
	plantuml -tpng "$section_dir/*.puml" -o "$section_dir"
    section_header="$(echo $section_dir | cut -c 3-)"
    echo "## $section_header" >> README.md

    for diagram_path in $(ls $section_dir/*.png)
    do
        echo "| ![$section_header]($diagram_path) |" >> README.md
        echo "| ------ |" >> README.md
        echo "" >> README.md
    done
done