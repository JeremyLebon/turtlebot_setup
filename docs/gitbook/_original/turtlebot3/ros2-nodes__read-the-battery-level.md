> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/ros2-nodes/read-the-battery-level.md).

# Read the battery level

Make a new python script (`sub_battery_level.py`) in the docker container turtlebot-vis.

Check the ros2 msg typ of the `/battery_state` topic. Add this as a python library.

Try to subscribe to the `/battery_state` topic.

Check what data is available in the ros2 topic `/battery_state`.

Print the voltage value and SoC (state of charge) of the battery to the terminal.

Print a warning when the SoC is below the 50%

Show when ready to the lecturer.
