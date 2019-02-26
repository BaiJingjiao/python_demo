mysql -umysqluser -ppassword databasename -e "drop database databasename"
sleep 5

./install.sh

./insert_db_mysql.sh
sleep 3
mysql -uuc_bmu -pChange_Me databasename -e "call test_createyyyy()"
sleep 3
mysql -uuc_bmu -pChange_Me databasename -e "call test_createxxxx()"
