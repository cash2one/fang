# Fenda Sub

## rabbitmq 配置

```
sudo rabbitmqctl add_user sub sub
sudo rabbitmqctl add_vhost sub
sudo rabbitmqctl set_permissions -p sub sub ".*" ".*" ".*"
```
