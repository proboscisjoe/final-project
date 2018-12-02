# final-project
# example docker invocation with trace file mapping: 
sudo docker run -d --net hadoop-net --name slave01 --hostname slave01 --mount type=bind,src=/var/log/syslog,dst=/var/log/syslog cloudsuite/hadoop slave
