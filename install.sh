
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
wget -q -O - https://github.com/ali77gh/shecan-cli/releases/download/1.3.0/shecan.py > temp.py
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
