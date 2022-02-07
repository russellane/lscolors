:

trap 'exit 0' 0 1 2 15

[ "$1" ] || { echo "Usage: $0 basename" >&2; exit 1; }
FILE1="$1"

if [ "$2" ]; then
    FILE2="$2"
else
    FILE2=docs/ansi/$1.txt
    FILE1=docs/txt/$1.txt
fi

ANS=
while [ "$ANS" != q ]; do
    for FILE in "$FILE1" "$FILE2"; do
        tput clear
        echo ::::: "$FILE" :::::
        cat "$FILE"
        echo -n "Press ENTER..."
        read ANS || break
        [ "$ANS" = "q" ] && break
        echo ANS=$ANS
    done
done
