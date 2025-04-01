# Find only in the root directory
rm -rf site
mkdir -p site
export files=() ; for file in `find . -name "*.py" -type f -maxdepth 1` ; do files+=($file) ; done

for file in "${files[@]}"; do
  echo $file
  without_extension="${file%.*}"
  uv run marimo export html-wasm "$file" -o site/"$without_extension".html --mode run
done

echo "<html><body><ul>" > site/index.html
for file in "${files[@]}"; do
  without_extension="${file%.*}"
  echo "<li><a href=\"$without_extension.html\">$without_extension</a></li>" >> site/index.html
done
echo "</ul></body></html>" >> site/index.html
