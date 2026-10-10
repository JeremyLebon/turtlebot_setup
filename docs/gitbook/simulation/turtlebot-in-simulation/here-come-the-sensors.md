# Here come the sensors

## 2D lidar

In this step, we want to visualise the 2D lidar present on the Turtlebot3.

Click Add and select the tab *By topic,* and select the topic */scan.*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FhlHmmQfmDfvpgPzvcWqY%2Fimage.png?alt=media&amp;token=784d5607-f955-4c5f-b470-93b0921d01fd" alt=""><figcaption></figcaption></figure>

Normally, the lidar output should be shown with red dots.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FDJBJ4zWBcTaBf32aMo7I%2Fimage.png?alt=media&amp;token=337d4a23-7afa-4593-a356-0eb23283e015" alt=""><figcaption></figcaption></figure>

By using the `ros2 topic echo` command, you can also see the /scan topic.

```
ros2 topic echo /scan
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FTL0iNXp2k9wGnX8iz2gj%2Fimage.png?alt=media&amp;token=87921f0c-cc7e-4008-85cb-67bc07ee92a6" alt=""><figcaption></figcaption></figure>

You can see the following:

* the angle scan range (0-6.28 rad)
* The angle increment: 0.017 rad or 0.1 degree
* Minimum range detected: 0.1199 m
* Maximum range detected: 3.5m
* In the item *ranges,* you can see all distances of every point.

Try driving around and see the lidar scan change.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FMaXjRFrwHvgKRlsR0a3T%2FRobot_scan_demo.gif?alt=media&amp;token=3d835e48-bba3-4b98-b949-1d8553e7342c" alt=""><figcaption></figcaption></figure>

## Odometry

The odometry shows us the path that the robot has been driven based on the wheel rotation.

Click Add and select the tab *By topic,* and select the topic */odom.*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9LMmGp6LFrOXsNilUrMK%2Fimage.png?alt=media&amp;token=039c800b-c760-47af-b926-2650cd3df440" alt=""><figcaption></figcaption></figure>

Collapse the item Odometry on the left. And change the parameter to keep to 500. This means the last 500 locations will be visualised in Rviz2. Then try driving around.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZkYe8O1NTIsSyi5CcPxG%2Fimage.png?alt=media&amp;token=31694e11-6e09-4af2-bc71-fcccdb0ebc53" alt=""><figcaption></figcaption></figure>

&#x20;Then try driving around. You should get a collection of arrows showing the location and orientation of the robot.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FRyxHCooFUVTT1NJ48pNv%2FRobot_odom_demo.gif?alt=media&amp;token=182cad3a-930f-4f77-ad83-6552b5f2eef2" alt=""><figcaption></figcaption></figure>

## IMU

The Turtlebot3 has a build in imu sensor. This can't be directly shown in RViz2.&#x20;

With `ros2 topic echo`, the real-time value can be shown. Open a new terminal if needed. You can see the linear z acceleration is roughly the known 9.81 m/s².&#x20;

```
ros2 topic echo /imu
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FgwaDgaLqETpefgG11ng0%2Fimage.png?alt=media&amp;token=996d4617-b5d6-4fb5-85cb-761768b59c2b" alt=""><figcaption></figcaption></figure>
