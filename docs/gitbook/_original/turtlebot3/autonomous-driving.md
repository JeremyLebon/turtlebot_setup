> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/autonomous-driving.md).

# Autonomous driving

{% hint style="danger" %}
Cancel the slam command of the previous step with CTRL + C !!!!
{% endhint %}

Start the autonomous navigation part.

Check where the map was stored in the mapping step. So change the map item below accordingly

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True
```

## Open rviz2&#x20;

And added the following items:

* /scan topic
* /tf
* /map
* /costmap

## Set the initial position of the turtlebot3

Set the fixed frame to map.

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FgZAOCYg89xeBmm7LGZoc%2Fimage.png?alt=media&amp;token=c3f89a99-9a91-46d7-a4ce-f8694bfa306c" alt=""><figcaption></figcaption></figure>

Set the initial pose of the TurtleBot3 using the 2D Pose Estimate button.&#x20;

{% hint style="info" %}
The first time loading RViz2 the map will not be visible.
{% endhint %}

After the pose is set, the autonomous navigation should be possible.

Use the Nav2 Goal button to set a desired goal. After setting up the TurtleBot3, it should start navigating to the desired point.

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FsmxUJhY8IFfsGF5rEtx6%2Fimage.png?alt=media&amp;token=83253ff1-6ed0-41f0-9b0e-87a009db10fc" alt=""><figcaption></figcaption></figure>

Demonstrate to the lecturer.

Try to add a obstacle in front of the turtlebot3 will it is navigating.
