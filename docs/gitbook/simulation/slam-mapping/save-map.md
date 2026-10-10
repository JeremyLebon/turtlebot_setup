# Save map

With the following command in a new terminal the map can be saved.

{% hint style="warning" %}
It is important not to stop the mapping node of the previous step.
{% endhint %}

{% code overflow="wrap" %}
```sh
ros2 run nav2_map_server map_saver_cli -f /home/dockeruserjazzy/my_map --free 0.196 --occ 0.65
```
{% endcode %}

You get two files: `my_map.pgm` (the image) and `my_map.yaml` (resolution,
origin, thresholds). The `.yaml` is what Nav2 needs in the next step.

{% hint style="info" %}
`--free 0.196`: otherwise grey (unknown) cells are loaded as free space later on,
and Nav2 plans paths through unexplored areas. Want a PNG to put in a report?
Add `--fmt png` (the `.yaml` then points to the `.png`).
{% endhint %}

If you look in the directory with VS Code inside the container, you can find the
image of the map. This map will be used as base map for the autonomous navigation.
