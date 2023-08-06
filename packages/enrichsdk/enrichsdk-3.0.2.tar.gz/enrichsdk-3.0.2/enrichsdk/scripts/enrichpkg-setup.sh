#!/bin/bash 

# Colors 
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
CHECK="\xE2\x9C\x94"

echo "############################################"
echo "Welcome to enrich environment setup script" 
echo "############################################"
echo ""

function usage() {
    echo "Usage: enrichpkg-setup.sh username workspace-dir" 
    echo ""
    echo "Notes:"
    echo "   Username: Can be anything. Is not related to system username" 
    echo "   Workspace directory: Where enrich should store its data"
    echo "" 
    exit 
}

hostos="Unknown"
if [ -e /etc/os-release ]; then 
    hostos=$(awk -F= '/^NAME/{print $2}' /etc/os-release|sed 's/"//g')
fi

if [ "$hostos" != "Ubuntu" ]; then
    echo "Unsupposed OS: $hostos" 
    exit
fi

if [ $# -lt 2 ]; then 
    usage; 
fi 

USERNAME=$1
WORKSPACE=$2

echo -e "Installing OS dependencies" 
echo "=====================" 
echo "Install Python3, git etc" 
sudo apt-get install -qq -y git python3-dev python3-pip 
sudo apt-get install -qq -y git python-dev python-pip 
sudo apt-get install -qq -y realpath
sudo pip install virtualenvwrapper
sudo apt-get install libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
echo -e "${GREEN}${CHECK}${NC} Done\n\n"


echo -e "Setting Workspace: $WORKSPACE" 
echo "====================="
echo "Creating directory hierarchy, etc files" 
mkdir -p $WORKSPACE 
WORKSPACE=$(realpath $WORKSPACE) 
for d in etc data log var opt customers shared 
do 
    mkdir -p $WORKSPACE/$d 
done 

etc=$(cat<<EOF
export ENRICH_ROOT="$WORKSPACE"
export ENRICH_DATA="$WORKSPACE/data"
export ENRICH_TEST="$WORKSPACE/data/_test"
export ENRICH_ETC="$WORKSPACE/etc"
export ENRICH_SHARED="$WORKSPACE/shared"
export ENRICH_VAR="$WORKSPACE/var"
export ENRICH_LIB="$WORKSPACE/lib"
export ENRICH_OPT="$WORKSPACE/opt"
export ENRICH_LOGS="$WORKSPACE/logs"
export ENRICH_CUSTOMERS="$WORKSPACE/customers"
export ENRICH_RELEASES="$WORKSPACE/releases"
export ENRICH_CUSTOMERS="$WORKSPACE/customers"
export ENRICH_TEST="$WORKSPACE/data/_test"

# Background Tasks configuration
export ENRICH_TASKDB_URL="sqlite:///$ENRICH_SHARED/jobs.sqlite3"
export ENRICH_TASKDB_HOSTNAME="127.0.0.1"
export ENRICH_TASKDB_PORT=12345
export ENRICH_TASKDB_LOGFILE=$ENRICH_LOGS/tasks/task.log

export EMAIL_HOST=""
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export EMAIL_PORT=""
export EMAIL_USE_TLS=""

EOF
)
echo "$etc" > $WORKSPACE/etc/django-env 
echo -e "${GREEN}${WORKSPACE}${NC} has your environment"
echo -e "${GREEN}${CHECK}${NC} Done\n\n"

SITECONF="$WORKSPACE/etc/siteconf.json" 
echo -e "\nSetting Up Siteconf" 
echo -e "=====================" 
echo -e "This has settings including credentials. Please edit"
echo -e "${GREEN}${SITECONF}${NC} to suit your needs"
cat > $SITECONF  << EOF
{
    "customer": "Acme Inc", 
    "dashboard": {
        "title": "Acme Rich Data Platform"
    },
    "credentials": { 
        "data-bucket": {
            "nature": "s3",
            "bucket": "acme-datalake",
            "readonly": false,
            "access_key": "AKIAJURXL...Q", 
            "secret_key": "tutww...A" 
        }
     }
}
EOF
echo -e "${GREEN}${CHECK}${NC} Done\n\n"

VERSIONMAP="$WORKSPACE/etc/versionmap.json" 
echo -e "\nSetting Up Version Map" 
echo "=====================" 
echo "This has versions of tools deployed. Edit" 
echo -e "${GREEN}${VERSIONMAP}${NC} to suit your needs. This can be added"
echo "to the run transform metadata using the config calls" 
cat > $VERSIONMAP  << EOF
[
   {
        "description": "Enrich SDK for pipeline development",
        "date": "2018-03-20 16:14:19 +0530",
        "repo": "enrich-sdk",
        "release": "v1.5.5",
        "label": "sdk",
        "commit": "6b406f0b083b962c164ac54431a44811c45b9ff0"
    }
]
EOF
echo -e "${GREEN}${CHECK}${NC} Done\n\n"


echo -e "\nSetting Virtual Environment" 
echo "=====================" 
echo "Python environment that doesnt interfere with anything else" 
echo "You could use virtualenv, pipenv etc as well. We add"
echo "virtualenvwrapper to your bashrc." 
echo "Please check https://virtualenvwrapper.readthedocs.io/en/latest/ on how to use it"

if grep -Fxqi "virtualenvwrapper" ~/.bashrc
then
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
fi

# Effectively source it..
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

echo "Creating a virtualenv: enrichdev-$USERNAME"
mkvirtualenv enrichdev-$USERNAME 
echo -e "${GREEN}${CHECK}${NC} Done\n\n"

localenv=$(cat<<EOF
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
workon enrichdev-$USERNAME 
source $WORKSPACE/etc/django-env 
EOF
)
echo -e "${GREEN}${CHECK}${NC} Done"

echo -e "\nCreating Starter Script" 
echo "=====================" 
echo "$localenv" > $WORKSPACE/enrich-env.sh 
echo -e "Created a local ${GREEN}$WORKSPACE/enrich-env.sh${NC}. Always source it before starting work" 

