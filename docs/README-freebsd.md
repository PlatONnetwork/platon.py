# platon.py on FreeBSD (11.2)

## Developer Setup

### Prerequisites

Make sure you've UTF-8 defined for charset and lang in your [~/.login_conf](https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/using-localization.html), 
otherwise almost every Python 3 module will fail to install.

`~/.login_conf`:
```
me:\
	:charset=UTF-8:\
	:lang=en_US.UTF-8:
```

Also make sure you've defined valid include and library paths in `~/.pydistutils.cfg`, otherwise native compilations fail.

`~/.pydistutils.cfg`:
```
[build_ext]
include_dirs=/usr/local/include
library_dirs=/usr/local/lib
```

```
sudo pkg install python3 py36-virtualenv git leveldb libxml2 libxslt pkgconf gmake secp256k1

# hack around https://github.com/platonnetwork/ethash/pull/107#issuecomment-445072692
sudo touch /usr/local/include/alloca.h

mkdir -p /tmp/venv_python
virtualenv-3.6 /tmp/venv_python/python3
source /tmp/venv_python/python3/bin/activate.csh

pip install coincurve

cd /tmp
git clone https://github.com/platonnetwork/platon.py.git
cd platon.py

# assuming you're using tcsh
pip install -e .\[dev\]
```

### Test

#### Prerequisites for integration tests:

##### node (https://github.com/platonnetwork/platon-go/wiki/Installation-Instructions-for-FreeBSD)
```
pkg install go
cd /tmp
git clone https://github.com/platonnetwork/platon-go
cd PlatON-Go
make node
cp build/bin/node /usr/local/bin/
```

##### parity (https://github.com/paukstis/freebsd_parity/blob/v1.6/README.md)
```
BROKEN (build crashes on FreeBSD 11.2)
```

```
cd platon.py
tox -e py36-core
tox -e py36-ens
tox -e py36-integration
etc

or

py.test tests/core
py.test tests/ens
py.test tests/integration
etc
```
