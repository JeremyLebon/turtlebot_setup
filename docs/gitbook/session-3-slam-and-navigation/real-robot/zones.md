# Zones: no-go areas, virtual walls, speed zones

**New exercise.** Not everything the robot should avoid is visible for the lidar:
a staircase, a cable on the floor, a glass wall, an area where people work.
Nav2 solves this with **costmap filters**: extra layers on top of the map.

Status page > **Navigatie** > tool **Zones** (dashed square icon):

| Zone | Effect |
|---|---|
| verboden zone (no-go) | the robot never enters it (planner and controller) |
| virtuele muur (virtual wall) | a line the robot doesn't cross |
| voorkeurszone (preferred lane) | the planner prefers paths through it; outside is allowed but costs more |
| snelheidszone (speed zone) | maximum speed in that zone, in % of the normal top speed |

Click the corner points on the map, finish the shape (double click or the check
button), then **save & apply**. The zones are stored with the map.

## Exercise

1. Start Navigatie and set the initial position.
2. Draw a **no-go zone** in the middle of an open area. Send a goal behind it:
   which path does the robot take now?
3. Draw a **virtual wall** across a passage. Can the robot still reach the
   other side?
4. Make a **speed zone** of 30 % near the door. Drive through it and watch the
   speed (Info > logs, or `ros2 topic echo /cmd_vel` in turtlebot-vis).
5. Turn on the **global costmap** layer (icon on the right of the map): how do
   your zones appear in it?

{% hint style="info" %}
Behind the scenes the status page publishes a mask (an image like the map) and
Nav2 uses it in the `KeepoutFilter` and `SpeedFilter`. Find these filters in the
Nav2 documentation: https://docs.nav2.org
{% endhint %}

Show your zones and the result to the lecturer.
