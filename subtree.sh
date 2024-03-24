
read -p "Select a mode(L: puLl, S:puSh)" MODE

if [ "$MODE" == "L" ]; then
    git subtree pull --prefix=pyplus pyplus_origin master
fi

if [ "$MODE" == "S" ]; then
    git subtree push --prefix=pyplus pyplus_origin master
fi
