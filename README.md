# final-project
# example docker invocation with trace file mapping: 
sudo docker run -d --net hadoop-net --name slave01 --hostname slave01 --mount type=bind,src=/sys/kernel/debug/tracing/trace,dst=/sys/kernel/debug/tracing/trace cloudsuite/hadoop slave
