# Connect to the WIFI

Every TurtleBot has its **own wifi network** (access point). This keeps the
connection fast and stable: you don't share the wifi with the other groups.

Check the number of your TurtleBot: see the sticker on the robot (and on its
access point). Connect your laptop to the wifi of **your** robot:

* Wifi name: `TB-AP-<nr>` (for example `TB-AP-05` for TurtleBot 5)
* Password: see lab notes

{% hint style="warning" %}
The robot wifi does not always have internet. Windows (and your phone) may then
silently switch to another network (eduroam, mobile data) - and the robot is
"gone".

* Windows: in the wifi list, untick **Connect automatically** for the other
  networks during the lab.
* Phone: when it says *"Wifi has no internet"*, choose **Stay connected**, or
  switch off mobile data.
{% endhint %}

Open a WSL terminal and check that you can reach your robot (replace `<nr>` by
the number of your robot, without a leading zero: robot 5 -> `10.0.5.10`):

```sh
ping 10.0.<nr>.10
```

You should get an answer every second. `CTRL + C` stops the ping.
