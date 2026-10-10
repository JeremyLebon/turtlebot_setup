> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/turtlebot-in-simulation/show-me-the-robot.md).

# Show me the robot

Make sure the turtlebot3 is still running in the Gazebo environment

Open a new terminal and connect to the running Docker container.

Add the following command

```
rviz2
```

The window below should pop up.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FhaAGPs4C7DjKS2qe2xN5%2Fimage.png?alt=media&amp;token=1ffda22a-0317-47ae-9aa7-c0af2c4cd625" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
In the current configuration, the map frame doesn't exist, which is why the Global Status gives an error
{% endhint %}

## Configuration Rviz

### Change fixed frame

Select as fixed frame as the odom frame

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FKXOe51sV1ksvoZJN7nLr%2Fimage.png?alt=media&amp;token=87ae629c-6ccb-4e36-ba60-0f7b67f5cabf" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FO0rwUJ8wsFlfi24sITSz%2Fimage.png?alt=media&amp;token=e8ec05dc-f554-478c-add2-97a2c2a45ee6" alt=""><figcaption></figcaption></figure></div>

### Show the robot

Click Add and select *RobotModel*

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJe8X9yBRn1ZbRyZjsEtA%2Fimage.png?alt=media&amp;token=f12aca05-c6c9-4321-b22d-d102ac52b3ee" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FgMsWwphlAlfnWQS48yaA%2Fimage.png?alt=media&amp;token=2ec1ea03-4e8f-41f7-b71d-7c472b3b4651" alt=""><figcaption></figcaption></figure></div>

Collapse the item *RobotModel* and select the topic `/robot_description`

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F7FosZqIfyqronRM8un4I%2Fimage.png?alt=media&amp;token=7a2b0b76-c4f0-4e13-8244-3e121baa3172" alt=""><figcaption></figcaption></figure>

Normally, the robot should be visible when using the zoom in.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIdOCpZgS4iR4CyX1UwDd%2Fimage.png?alt=media&amp;token=ec1799b5-0c1e-4b87-a7a1-50f14569639d" alt=""><figcaption></figcaption></figure>

## TF

### Visualise the TF

Click Add and select *TF*

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJe8X9yBRn1ZbRyZjsEtA%2Fimage.png?alt=media&amp;token=f12aca05-c6c9-4321-b22d-d102ac52b3ee" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F4CuCZzvfQkOUeN4pBHE4%2Fimage.png?alt=media&amp;token=ce253cf7-07b8-4a69-a42a-181d4f7e78c6" alt=""><figcaption></figcaption></figure></div>

You can now see the different links/frames of the robot.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fr4W55Akx5O7qhX61T0Dz%2Fimage.png?alt=media&amp;token=15a60afc-ffca-4838-a745-3e6a5fb86b25" alt=""><figcaption></figcaption></figure>

Collapse the item *TF* and check the *Show Names* item.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FHyhk98CJoACIRjY363hE%2Fimage.png?alt=media&amp;token=82541c34-d3b7-4777-9f80-7573eeb0964a" alt=""><figcaption></figcaption></figure>

Collapse the item TF further to see the different frames (item *Frames*). Enable and disable them to see where the frames are located. Select the *Tree* item to see how the links/frames are connected.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FBFxig56bOl0d8oe7CKhm%2Fimage.png?alt=media&amp;token=f5ac1010-62f6-4795-ab86-a7484c82f80d" alt=""><figcaption></figcaption></figure>

Enable the *base\_link, base\_scan, odom, wheel\_left\_link and wheel\_right\_link*.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FLuhqFfFNhOJHb6C5RK2h%2Fimage.png?alt=media&amp;token=85e16ef5-74ee-4d00-8292-ae0669f78db7" alt=""><figcaption></figcaption></figure>

Drive around with the robot (with the teleop\_twist\_keyboard node). You should see the wheels/frames turning around. Also, look at the odom frame.

<details>

<summary>Controlling the robot command</summary>

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

</details>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F2km8tPYrLAF4FyaX5prX%2FRobot_tf_demo.gif?alt=media&amp;token=1a0cb1e7-8af4-4b0a-8cb9-e81d4828c1a1" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The tf2 ros2 library calculates all the frames and joints at very high rate.
{% endhint %}

### Echo the /tf topic

Use the following command to see a list op the ros2 topics. Use a new terminal if needed.

Output

```
/clicked_point
/clock
/cmd_vel
/goal_pose
/imu
/initialpose
/joint_states
/odom
/parameter_events
/robot_description
/rosout
/scan
/tf
/tf_static
```

{% hint style="info" %}
The /tf topic stands for the transformations of all the frames/links.&#x20;
{% endhint %}

Visualise the /tf topic with ros2 topic echo.&#x20;

```
ros2 topic echo /tf
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FMtfF6pIU8gezOXSZeBKa%2Fimage.png?alt=media&amp;token=cca13828-5ef0-41f8-a399-38a096d6429e" alt=""><figcaption></figcaption></figure>

Use the ros2 topic hz command to see the update rate. Here, the message is sent 60 times per second!

```
ros2 topic hz /tf
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fx0MpAOaM8tbpBmtP8bqC%2Fimage.png?alt=media&amp;token=48a2b37c-4a71-4935-816a-2129fdfe68d3" alt=""><figcaption></figcaption></figure>

### Look at the /joint\_state topic

If you echo the `/joint_states` And you let the robot turn. You should see the joint state position and velocity change.&#x20;

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIf9Qd2kLikFoRpBieMgl%2Fimage.png?alt=media&amp;token=1c73090f-2dd6-49bf-af5b-439e6599b5cc" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fc7iuLHaMdenJRVFX2ogG%2Fimage.png?alt=media&amp;token=d87f8603-ba1e-4e0e-8fdd-d0c49bc318f2" alt=""><figcaption></figcaption></figure></div>

&#x20;          &#x20;
