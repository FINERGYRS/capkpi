#!/bin/bash

set -e

cd ~ || exit

sudo apt update && sudo apt install redis-server libcups2-dev

pip install finergy-bench

finergyuser=${FINERGY_USER:-"finergy"}
finergybranch=${FINERGY_BRANCH:-${GITHUB_BASE_REF:-${GITHUB_REF##*/}}}

git clone "https://github.com/${finergyuser}/finergy" --branch "${finergybranch}" --depth 1
bench init --skip-assets --finergy-path ~/finergy --python "$(which python)" finergy-bench

mkdir ~/finergy-bench/sites/test_site

if [ "$DB" == "mariadb" ];then
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_mariadb.json" ~/finergy-bench/sites/test_site/site_config.json
else
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_postgres.json" ~/finergy-bench/sites/test_site/site_config.json
fi


if [ "$DB" == "mariadb" ];then
    mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

    mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_finergy'@'localhost' IDENTIFIED BY 'test_finergy'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_finergy"
    mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_finergy\`.* TO 'test_finergy'@'localhost'"

    mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'"
    mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES"
fi

if [ "$DB" == "postgres" ];then
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_finergy" -U postgres;
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_finergy WITH PASSWORD 'test_finergy'" -U postgres;
fi


install_whktml() {
    wget -O /tmp/wkhtmltox.tar.xz https://github.com/FINERGYRS/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
    sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
    sudo chmod o+x /usr/local/bin/wkhtmltopdf
}
install_whktml &

cd ~/finergy-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app payments
bench get-app capkpi "${GITHUB_WORKSPACE}"

if [ "$TYPE" == "server" ]; then bench setup requirements --dev; fi

bench start &> bench_run_logs.txt &
CI=Yes bench build --app finergy &
bench --site test_site reinstall --yes
