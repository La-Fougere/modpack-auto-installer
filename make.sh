for file in files_for_.minecraft_folder/resourcepacks/*; do
    mv "$file" "$(echo $file | tr ' ' '_')"
done
for file in files_for_.minecraft_folder/resourcepacks/*; do
    filename=$(basename "$file")
    new_filename=$(echo "$filename" | sed 's/[^a-zA-Z0-9._]/_/g')
    mv "$file" "files_for_.minecraft_folder/resourcepacks/$new_filename"
done
pyinstaller --onefile --add-data "files_for_.minecraft_folder:files_for_.minecraft_folder" --icon=icon.ico --uac-admin main.py
mv dist/main.exe ./
rm -rf build dist main.spec
current_dir=$(basename "$PWD")
if [ -f "${current_dir}.exe" ]; then
    rm "${current_dir}.exe"
fi
mv main.exe "${current_dir}.exe"