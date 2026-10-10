# Startup docker

{% hint style="success" %}
Nothing to do here anymore: the Docker container on the robot (`turtlebot_<nr>`)
starts **automatically** when the robot boots, and restarts by itself if needed.
{% endhint %}

Check that it runs: on the status page `http://10.0.<nr>.10:8080` the
connection icon (plug) in the header is green, and the robot name is shown.

Or via SSH on the robot:

```sh
docker ps
```

You should see a container `turtlebot_<nr>`.

{% hint style="danger" %}
Don't run `docker compose pull` or `docker compose up/down` yourself. Updating
the robot software is done by the lecturer (status page > Beheer).
{% endhint %}
