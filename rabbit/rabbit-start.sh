set -ex
echo  "waiting headless online"
sleep 30
hostname=`hostname`
rabbitmq-server -detached
echo "start rabbitmq-server"

until rabbitmqctl node_health_check; do sleep 3; done
echo "$hostname is started."
if [[ "$hostname" -eq "$CLUSTER" ]]; then
  rabbitmqctl stop_app
  echo "stop_app on $hostname"
  echo  "reset on $hostname"
  rabbitmqctl start_app
  echo "start_app on $hostname"
  rabbitmq-plugins enable rabbitmq_management
  echo  "rabbitmq_management enabled on $hostname"
  bjrdc=`rabbitmqctl list_users|grep bjrdc||true`
  if [ -z "$bjrdc" ]; then
    echo "create user bjrdc.."
    rabbitmqctl add_user bjrdc zgjx@321
    rabbitmqctl set_user_tags bjrdc administrator
    rabbitmqctl set_permissions -p / bjrdc ".*" ".*" ".*"
    echo "create user finished."
  else
    echo "bjrdc is in cluster so do nothing."	  
  fi	  
else
  cluster=`rabbitmqctl cluster_status|grep $CLUSTER.$HEADLESS||true`
  echo "cluster is $cluster ."
  if [ -z "$cluster" ]; then
    echo "$hostname is not join to cluster $CLUSTER.$HEADLESS"
    rabbitmqctl stop_app
    rabbitmqctl join_cluster rabbit@$CLUSTER.$HEADLESS
    echo  "$hostname join cluster to rabbit@$CLUSTER.$HEADLESS"
    rabbitmqctl start_app
  else
    echo "$hostname is in cluster $CLUSTER.$HEADLESS"
  fi
fi

