# Startup docker

{% hint style="success" %}
Nothing to do here anymore: the Docker container on the robot (`turtlebot_<nr>`)
starts **automatically** when the robot boots, and restarts by itself if needed.
{% endhint %}

Check that it runs. Via SSH on the robot (not inside the container):

```sh
docker ps
```

You should see a container `turtlebot_<nr>` with status `Up`.

{% hint style="danger" %}
Don't run `docker compose pull`, `docker compose up/down` or `docker rm`
yourself on the robot. Updating the robot software is done by the lecturer.
{% endhint %}
