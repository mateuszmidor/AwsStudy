#!/usr/bin/env bash

HEADER="## Sections"

# create blank sections in README.md
sed "/${HEADER}/,$ d" -i README.md
echo "${HEADER}" >> README.md

# fill sections
sections=$(find . -maxdepth 1 -type d ! -name '.*')
for section_dir in $sections
do
	plantuml -tpng "$section_dir/*.puml"
    section_header="${section_dir##*/}" # cut leading "./"
    echo "Processing $section_header..."
    echo "## $section_header" >> README.md

    for diagram_path in $(ls $section_dir/*.png)
    do
        basename=${diagram_path##*/}
        noext=${basename%%.*}
        echo "### $noext" >> README.md
        echo "| ![$section_header]($diagram_path) |" >> README.md
        echo "| ------ |" >> README.md
        echo "" >> README.md
    done
done

echo "Done."