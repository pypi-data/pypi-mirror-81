# A symfony message translation plugin for YAZ
TODO: Short description here

# Installing
## From a package
```sh
sudo pip3 install yaz_messaging_plugin
```

## From source
```sh
git clone git@github.com:yaz/yaz_messaging_plugin.git
cd yaz_messaging_plugin
python3 setup.py install
```

## From source (for development, with virtualenv)
```sh
# skip this step if you have a python3.5 (or higher) environment
sudo apt-get install libssl-dev
cd $HOME/local
git clone https://github.com/python/cpython.git
cd cpython
./configure --prefix=$HOME/local
make install

# get yaz
git clone git@github.com:boudewijn-zicht/yaz_messaging_plugin.git
cd yaz_messaging_plugin

# skip this step if you have a python3.5 (or higher) environment
# create and activate your python3.5 (or higher) virtual env
virtualenv --python=python3.5 env
source env/bin/activate
# run deactivate to exit the virtualenv

# run tests
make test
```

# Maintainer(s)
- Boudewijn Schoon <boudewijn@zicht.nl>
