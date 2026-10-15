# Connect to the turtlebot3

For the exercises you need a terminal **inside the robot container**. Two ways:

## Option 1 - SSH (recommended)

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

{% hint style="info" %}
`WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`? The robot was reinstalled
since your last visit. Remove the old key and try again:

```sh
ssh-keygen -R 10.0.<nr>.10
```
{% endhint %}

You are now on the Raspberry Pi of the robot. Go inside the robot container:

```sh
docker exec -it turtlebot_<nr> bash
```

{% hint style="warning" %}
`<nr>` is the robot number **without** a leading zero: robot 5 ->
`docker exec -it turtlebot_5 bash`. Press `TAB` to autocomplete.
{% endhint %}

You need a robot terminal more than once (bringup, gamepad, ...): open a new WSL
terminal and repeat both commands.

## Option 2 - web terminal

Open `http://10.0.<nr>.10:7681` in a browser (laptop on `TB-AP-<nr>`).
Login: see lab notes. You are directly inside the robot container.

## The status page (optional)

Every robot also serves a web page: `http://10.0.<nr>.10:8080`. It is handy
to check the **battery**, to see what is running, and for the **STOP** button,
which stops everything that drives. For the exercises you don't need it: you
work in the terminal.
