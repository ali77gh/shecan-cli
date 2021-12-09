
# download
echo "downloading..."
wget -O - https://github.com/ali77gh/shecan-cli/releases/download/1.0.0/shecan.py > temp.py
echo "done"

# copy
echo "installing..."
cp temp.py /usr/bin/shecan-cli
echo "done"

# access
echo "making script executable..."
chmod +x /usr/bin/shecan-cli
echo "done"

# remove temp
rm temp.py

echo "shecancli installed successfully"

echo "running => shcan-cli help"
shecan-cli help