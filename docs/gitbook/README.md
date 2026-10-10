# GitBook - lesboeken TurtleBot3 (bijgewerkt 2026-10-11)

De twee VIVES-GitBooks, aangepast aan de nieuwe labo-opstelling (Raspberry Pi OS
+ Docker, Zenoh, eigen access point per robot `TB-AP-<nr>`, Fenix-statuspagina,
`ros2_ws`). **Geen wachtwoorden** in deze pagina's ("see lab notes"): de repo is publiek.

## Begin hier

| Boek | Overzicht (status per pagina) | Alles achter elkaar lezen | Inhoudstafel (GitBook) |
|---|---|---|---|
| Turtlebot3 (echte robot) | [turtlebot3/OVERZICHT.md](turtlebot3/OVERZICHT.md) | [turtlebot3/BOOK.md](turtlebot3/BOOK.md) | [turtlebot3/SUMMARY.md](turtlebot3/SUMMARY.md) |
| ROS2 - Simulation | [simulation/OVERZICHT.md](simulation/OVERZICHT.md) | [simulation/BOOK.md](simulation/BOOK.md) | [simulation/SUMMARY.md](simulation/SUMMARY.md) |

Status: 🟠 gewijzigd, 🟢 nieuw, 🟡 kleine aanpassing (`ros_ws` -> `ros2_ws`), ⚪ ongewijzigd.

## Structuur

```
docs/gitbook/
  turtlebot3/            volledig boek: elke pagina op haar GitBook-pad
    SUMMARY.md           inhoudstafel in GitBook-formaat (volgorde + nesting)
    OVERZICHT.md         tabel: pagina + status (gegenereerd)
    BOOK.md              alle pagina's in leesvolgorde (gegenereerd)
  simulation/            idem voor het simulatieboek
  _original/             de pagina's zoals ze op 2026-10-11 in GitBook stonden
  _tools/build_books.py  maakt SUMMARY/OVERZICHT/BOOK opnieuw
```

## Werkwijze

1. Pas een pagina aan in `turtlebot3/...` of `simulation/...`.
2. `cd docs/gitbook && python3 _tools/build_books.py` - de status (vergeleken met
   `_original`) en `BOOK.md` worden bijgewerkt.
3. Naar GitBook:
   * **Git Sync (aanbevolen)**: in GitBook het boek koppelen aan deze GitHub-repo,
     map `docs/gitbook/turtlebot3` (resp. `simulation`); GitBook leest
     `SUMMARY.md` en de pagina's. Daarna is GitHub de bron, geen kopiëren meer.
   * of per pagina kopiëren en plakken (zie de tabellen hieronder: wat er veranderd is).

## Book "Turtlebot3" - https://vives-4.gitbook.io/turtlebot3/

| File | GitBook page | What changed |
|---|---|---|
| `turtlebot3/turtlebot3-startup/connect-to-the-wifi.md` | Connect to the WIFI | own AP `TB-AP-<nr>`; warning: no internet -> laptop/phone switches network |
| `turtlebot3/turtlebot3-startup/startup-of-the-turtlebot3.md` | Startup of the turtlebot3 | container starts by itself, startup beep, check on the status page |
| `turtlebot3/turtlebot3-startup/connect-to-the-turtlebot3.md` | Connect to the turtlebot3 | status page `http://10.0.<nr>.10:8080` first; web terminal or `ssh turtlebot@10.0.<nr>.10`; **password removed** |
| `turtlebot3/turtlebot3-startup/startup-docker.md` | Startup docker | nothing to do anymore (no `docker compose pull/up` by students) |
| `turtlebot3/turtlebot3-startup/startup-turtlebot-software.md` | Startup turtlebot software | bringup in the terminal (learn) or via the status page; **password removed** |
| `turtlebot3/turtlebot3-startup/setup-laptop-student.md` | Setup laptop (student) | no firewall rules (Zenoh); `git clone` (Zenoh is on `master` now) / `git pull` for an old clone; `docker compose pull`; `.env`: `ROS_DOMAIN_ID` + `ROBOT_ZENOH_IP`; troubleshooting |
| `turtlebot3/controlling-the-robot/manual-control-by-terminal.md` | Manual control by terminal | + twist_mux: who is in control (priorities) |
| `turtlebot3/controlling-the-robot/manual-control-with-gamepad.md` | Manual control with gamepad | switch on via the status page; **LB** = enable (was "right joystick"), RB = faster |
| `turtlebot3/ros2-nodes.md` | ROS2 nodes | workspace `/root/ros2_ws` on laptop and robot |
| `turtlebot3/ros2-nodes/read-in-the-scan-topic.md` | Read in the scan topic | `/root/ros2_ws`; 220-230 points per rotation (LDS-02) |
| `turtlebot3/ros2-nodes/drive-10cm-with-a-button.md` | Drive 10cm with a button | `/root/ros2_ws`; + twist_mux hint; Twist (Humble) vs TwistStamped (Jazzy) |
| `turtlebot3/slam.md` | SLAM | way 1 yourself (Cartographer on the laptop), way 2 status page (on the robot); `map_saver_cli --free 0.196` into `ros2_ws/maps` |
| `turtlebot3/autonomous-driving.md` | Autonomous driving | **`use_sim_time:=True` removed** (wrong on a real robot); `map:=`; status page; correcting with the arrows |
| `turtlebot3/autonomous-driving-with-python-library.md` | Autonomous driving with python library | max speed via an own params file in `ros2_ws` (was: edit `/opt/ros/jazzy/...`) |
| `turtlebot3/simulation-of-sensors.md` | Simulation of sensors | topics `/sim/...` (publishing `/battery_state` clashed with the real battery) |
| `turtlebot3/install-python-libraries-in-container.md` | Install python libraries in container | `turtlebot-vis` (Humble, Python 3.10), venv in `ros2_ws` with `--system-site-packages` |
| `turtlebot3/location-files-on-wsl.md` | Location files on wsl | `turtlebot_vis/ros2_ws`, `\\wsl$\...` path |
| `turtlebot3/compare-planners-and-controllers.md` | **new** (after Autonomous driving) | exercise: NavFn/A\*/Smac/Theta\* and DWB/RPP/MPPI compared |
| `turtlebot3/zones.md` | **new** (after Autonomous driving) | exercise: no-go zone, virtual wall, preferred lane, speed zone (costmap filters) |

Unchanged (still correct): Turtlebot3 in the real world, Objectives, Visualise
the robot (Best Effort hint), Controlling the robot, See turtlebot3 topics, Read
the battery level, Read the encoder value, Exercise (scan), Measure while driving
(+ solution), Play a sound. Tip: in those pages `/root/ros_ws` -> `/root/ros2_ws`
where it occurs.

## Book "ROS2 - Simulation" - https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/

| File | GitBook page | What changed |
|---|---|---|
| `simulation/slam-mapping/save-map.md` | Save map | `--free 0.196 --occ 0.65`; `.yaml` is what Nav2 needs |
| `simulation/autonomous-navigation.md` | Autonomous Navigation | `map:=/home/dockeruserjazzy/my_map.yaml` added (else the default map is loaded) |
| `simulation/simulation-vs-real-robot.md` | **new** (end of the book) | Jazzy vs Humble, TwistStamped vs Twist, slam_toolbox vs Cartographer, use_sim_time, Zenoh, twist_mux |

## Still to check in the lab

* `turtlebot-vis`: `docker compose pull` works for students
  (image `nobel86/turtlebot-rpi5-vis:zenoh` on Docker Hub) and `cartographer.launch.py`
  / `map_saver_cli` / `navigation2.launch.py params_file:=` run in it.
* Done 2026-10-11: branch `zenoh` merged into `master` of turtlebot_vis (d000a60).
* Web terminal login (`:7681`) currently = wifi password pattern -> see the security todo.
