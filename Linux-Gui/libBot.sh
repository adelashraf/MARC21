zenity --info --title 'Warning ' --text 'This is a Beta version' --ellipsize
fil=result.txt
ENTRY=$(zenity --file-selection --title="Select a PDF File")
echo "Scanning $ENTRY ...."
result=$(python libBot.py "$ENTRY")
echo "$result" >> "$fil"
zenity --text-info --filename "$fil" --editable --auto-scroll --title 'The results' --width 1000 --height 700
