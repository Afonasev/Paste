set -e

pip install -r requirements.txt
isort -c
flake8 paste tests
pylint paste tests
py.test --cov=./paste

push="push"

if [ "$TRAVIS_EVENT_TYPE" = "$push" ]; then
    coveralls
    sudo apt-get install sshpass
    sshpass -e ssh root@138.68.65.124 -t supervisorctl restart paste
fi
