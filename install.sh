#!/bin/bash

platform=`uname`

if [ "$platform" = "Linux" ]
then
    install_path="/usr/bin/shecan-cli"
fi
if [ "$platform" = "Darwin" ]
then
    install_path="/usr/local/bin/shecan-cli"
fi

# download
echo "downloading..."
repo="ali77gh/shecan-cli"
tag_name=$(curl --silent https://api.github.com/repos/$repo/releases/latest \
                  | grep '"tag_name"' \
                  | sed --regexp-extended 's/.*"([^"]+)".*/\1/')
curl -sfL "https://github.com/$repo/releases/download/$tag_name/shecan.py" --output temp.py
echo "done"

# copy
echo "installing..."
mv temp.py "$install_path"
echo "done"

# access
echo "making script executable..."
chmod +x "$install_path"
echo "done"

echo "shecan-cli installed successfully"
shecan-cli help
