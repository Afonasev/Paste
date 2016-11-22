set -e

pip install -r requirements.txt
py.test --cov=./paste
flake8
pylint paste

push="push"

if [ "$TRAVIS_EVENT_TYPE" = "$push" ]; then
    coveralls
    sudo apt-get install sshpass
    sshpass -e ssh root@138.68.65.124 -t supervisorctl restart paste
fi
