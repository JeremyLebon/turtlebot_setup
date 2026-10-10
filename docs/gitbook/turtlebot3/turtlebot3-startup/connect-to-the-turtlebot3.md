# Connect to the turtlebot3

## The status page (Fenix)

Every robot serves its own web page. With your laptop (or phone) on the robot
wifi `TB-AP-<nr>`, open a browser:

```
http://10.0.<nr>.10:8080
```

Check in the header:

* the **robot name** (is this your robot?)
* the **battery** icon (hover over it: voltage; 0 % = 11.0 V, below that the
  OpenCR switches the motors off)
* the **labo-check** icon (tick): green = everything OK. Click it for the full list.

{% hint style="info" %}
Tabs: **Rijden** (drive, camera, make a map), **Navigatie** (navigate on a map),
**Projecten** (ready-made demos), **Info** (robot health, topics, logs).
The red **STOP** button stops everything that drives.
{% endhint %}

## A terminal on the robot

For the ROS 2 exercises you need a terminal **inside the robot container**.
Two ways:

### Option 1 - web terminal

Click the `>_` button in the header of the status page (opens
`http://10.0.<nr>.10:7681`). Login: see lab notes. You are directly inside the
robot container.

### Option 2 - SSH

Open a WSL terminal:

```sh
ssh turtlebot@10.0.<nr>.10
```

* username: `turtlebot`
* password: see lab notes

{% hint style="warning" %}
The password stays invisible while typing. Say `yes` when a fingerprint is
suggested the first time.
{% endhint %}

You are now on the Raspberry Pi of the robot. Go inside the robot container:

```sh
docker exec -it turtlebot_<nr> bash
```

{% hint style="warning" %}
`<nr>` is the robot number **without** a leading zero: robot 5 ->
`docker exec -it turtlebot_5 bash`. Press `TAB` to autocomplete.
{% endhint %}
