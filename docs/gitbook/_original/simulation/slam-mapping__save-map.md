> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/save-map.md).

# Save map

With the following command in a new terminal the map can be saved.&#x20;

{% hint style="warning" %}
It is important not to stop the mapping node of the previous step.
{% endhint %}

{% code overflow="wrap" %}

```sh
ros2 run nav2_map_server map_saver_cli -f /home/dockeruserjazzy/my_map --fmt png
```

{% endcode %}

The map will be saved as a PNG. In the terminal you should see the output below.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FqUwFSbByX6vjzpvCPT62%2Fimage.png?alt=media&amp;token=5ad2600f-ce68-4551-bf66-dd49fe42c939" alt=""><figcaption></figcaption></figure>

If you look in the directory with VScode inside the container, you can find the image of the map.

This map will be used as base map for the autonomous navigation.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FbT88rZTHHwTRpoxOVRQ0%2Fimage.png?alt=media&amp;token=0ef9ffc4-9d21-4ecb-89ff-9abd1c9466b0" alt=""><figcaption></figcaption></figure>
