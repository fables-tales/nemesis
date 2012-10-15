#!/bin/bash
ruby=$(which ruby)

if [ ruby == "/usr/bin/ruby" ]
    sudo gem install vagrant
else
    gem install vagrant
fi

git clone https://github.com/samphippen/srobo-ldap-box.git
vagrant up --provision
