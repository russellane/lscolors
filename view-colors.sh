:

[ "$1" ] || { echo "Usage: $0 files" >&2; exit 1; }

for FILE; do
    tput clear
    echo ::::: "$FILE" :::::
    cat "$FILE"
    echo -n "Press ENTER..."
    read </dev/tty || break
done
