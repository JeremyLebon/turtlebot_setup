# Read the battery level

Make a new python script (`sub_battery_level.py`) in the `turtlebot-vis` container, in `/root/ros2_ws`.

Check the ros2 msg typ of the `/battery_state` topic. Add this as a python library.

Try to subscribe to the `/battery_state` topic.

Check what data is available in the ros2 topic `/battery_state`.

Print the voltage value and SoC (state of charge) of the battery to the terminal.

Print a warning when the SoC is below the 50%

{% hint style="info" %}
* Is `percentage` a value between 0 and 1, or between 0 and 100? Check it with
  `ros2 topic echo /battery_state --once`.
* The percentage of the OpenCR is optimistic: the motors already stop at
  **11.0 V**. Extra: also print a warning when the **voltage** is below 11.2 V.
{% endhint %}

Show when ready to the lecturer.
