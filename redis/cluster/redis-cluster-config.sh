kubectl create configmap redis-cluster-config  -n bjrdc-dev --from-file=redis.conf=./redis.conf --from-file=redis-cluster-boot.py=./redis-cluster-boot.py
