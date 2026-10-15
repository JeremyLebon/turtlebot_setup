# Compare planners and controllers

**New exercise.** Nav2 has two "brains":

* the **planner** (global): calculates a path over the whole map, from the
  robot to the goal;
* the **controller** (local): follows that path, a few times per second, and
  avoids obstacles that are not on the map.

On the status page > **Navigatie** > **Algoritmes** you can choose both; the
choice counts for the next goal or route.

| Planner | Idea |
|---|---|
| NavFn (Dijkstra) | standard of TurtleBot3; shortest path over the grid |
| NavFn (A\*) | same paths, calculated faster (heuristic towards the goal) |
| Smac 2D | A\* on the grid, smoother paths |
| Theta\* | straight lines between corners ("any-angle") |

| Controller | Idea |
|---|---|
| DWB | tries many speeds and picks the best (standard) |
| Regulated Pure Pursuit | follows a point some distance ahead on the path, calm |
| MPPI | simulates ~1000 possible trajectories per step and picks the best; smooth but heavy for the Pi |

## Exercise

1. Start Navigatie with your map and set the initial position.
2. Choose 2 points far apart, with a corner or an obstacle in between.
3. Drive from A to B with every **planner** (controller: DWB). Note for each:
   the shape of the path (screenshot), the time, does it reach the goal?
4. Same route with every **controller** (planner: NavFn). Note: the time, how
   smooth it drives, how close it passes obstacles, does it wiggle at the goal?
5. Put a box on the path while driving. Which controller reacts best?
6. Look at **Info** > logs and the CPU load in the header: which combination is
   heavy for the Raspberry Pi?

Explain your results to the lecturer: which combination would you choose for a
narrow classroom, and which for a large hall?

{% hint style="info" %}
**Nauwkeurigheid** (accuracy) decides when the robot is "there". More accurate
than the localisation (5-10 cm) makes no sense: then the robot keeps wiggling
at the goal.
{% endhint %}
