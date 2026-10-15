# Read the encoder value

{% hint style="info" %}
Theory: [Odometry (/odom) and encoders](../theory/odometry.md) - ticks, wheel radius and the formulas.
{% endhint %}

Make a new python script (`sub_encoders.py`) in the `turtlebot-vis` container, in `/root/ros2_ws`.

Check if there is a ros2 topic that contains the encoder values

Check the ros2 msg typ of the ros2 topic. Add this as a python library inside in the script.

Try to subscribe to the ros2 topic.

Print the encoder values to the terminal.

Try to calculate the average speed of the wheels.

Show when ready to the lecturer.
