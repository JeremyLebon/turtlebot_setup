# Moving the turtlebot

Load the turtlebot again in the turtlebot world.

<pre><code><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

Open a new terminal and connect to the docker container. Try to find how many ros2 nodes are running.&#x20;

<details>

<summary>Solution</summary>

```
ros2 node list
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIEDot7g4vqcm8WO2u1Ya%2Fimage.png?alt=media&amp;token=ae0b6e4d-6ee9-4f88-8bfc-160905719838" alt=""><figcaption></figcaption></figure>

</details>

Open a new terminal and connect the docker container.

Add the following command to start the `teleop_twist_keyboard` ros2 node. This will publish the cmd\_vel (command\_velocity) topic. The turtlebot is subscribed to this topic. And will drive accordingly.

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

{% hint style="info" %}
Important the terminal should be selected when controlling the robot.
{% endhint %}

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FrxY13HeLjcAf3rG2FdHB%2Fimage.png?alt=media&amp;token=69ed0886-302c-4210-8a52-13db4aacc6d5" alt=""><figcaption></figcaption></figure>

Try to drive the robot around in the world. Maybe in the beginning, try to lower the speed by tapping z.

Open a new terminal and check with ros2 topic list which ros2 topics are available.

Try to show the actual `cmd_vel` topic. Important the robot should be driving to see the cmd\_vel topic.

<details>

<summary>Solution</summary>

```
ros2 topic echo /cmd_vel
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FEMWz3atS5skfBlaTVDRo%2Fimage.png?alt=media&amp;token=371b76d8-124a-4408-9f3e-9575a32f0a7e" alt=""><figcaption></figcaption></figure>

</details>

Try to lookup the location of the turtlebot with the `ros2 topic echo` command. Which topic has the location information?&#x20;

<details>

<summary>Solution</summary>

The /odom topic contains the location and the orientation of the turtlebot

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FqwYP0hPk3b74vzVfqxlc%2Fimage.png?alt=media&amp;token=d29b71eb-a7b0-40aa-88f5-9f50326c5f9b" alt=""><figcaption></figcaption></figure>

</details>

Try to ride around and look at the location. Start `rqt` and try to visualize the x and y coordinates in a graph.

<details>

<summary>Solution</summary>

Open a new terminal and add the command below to start rqt

```
rqt
```

Select the topic with Plugins > Topics > Topic monitor.

Select the graph with Plugins > Visualisation> Plot

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FFDOM01gw9GcX0mVKRweZ%2Fimage.png?alt=media&amp;token=8ac28a21-6e1d-4b3a-870a-9acca6687e53" alt=""><figcaption></figcaption></figure>

</details>

Close rqt with CRTL + C in the terminal
