# Install python libraries in container

Needed to install libraries (Matplotlib, reportlab, ...).

Go inside the `turtlebot-vis` container (ROS 2 Humble, Ubuntu 22.04, Python 3.10):

```sh
docker exec -it turtlebot-vis bash
apt update
apt install -y python3-venv
```

Make a virtual environment **in your workspace** (so it survives a restart of
the container) **with** the system packages (otherwise `rclpy` and the ROS
message types are not found):

```sh
python3 -m venv --system-site-packages /root/ros2_ws/.venv
```

Activate the venv:

```sh
source /root/ros2_ws/.venv/bin/activate
```

Install the specific libraries with:

```sh
python -m pip install matplotlib reportlab PyYAML pandas seaborn
```

{% hint style="info" %}
`apt install` is lost when the container is recreated (e.g. after
`docker compose pull`); the venv in `/root/ros2_ws` stays. After a recreate,
only `apt install -y python3-venv` is needed again before using pip.
{% endhint %}

{% hint style="warning" %}
The robot wifi may have no internet: install libraries at home or when the
access point has internet.
{% endhint %}
