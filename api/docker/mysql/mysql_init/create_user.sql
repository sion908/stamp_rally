create database local_test_db;
create user 'hy'@'%' identified by 'ia';
grant all on local_test_db.* to 'hy'@'%';
