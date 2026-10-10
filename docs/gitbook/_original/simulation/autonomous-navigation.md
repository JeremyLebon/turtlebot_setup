> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/autonomous-navigation.md).

# Autonomous Navigation

{% hint style="danger" %}
Cancel the slam command of the previous step with CRTL + C !!!!
{% endhint %}

<pre><code><strong>ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True
</strong></code></pre>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fm8qtkYI9GBRXteb9fQET%2Fimage.png?alt=media&amp;token=d3580a54-913c-48fe-97f1-9f2bef0dc978" alt=""><figcaption></figcaption></figure>

## Set the initial position of the turtlebot3

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FClpmrOCoRAExejuu5e2B%2Fimage.png?alt=media&amp;token=f650e6e6-52a0-4c38-af59-292ec1aa4416" alt=""><figcaption></figcaption></figure>

Set the initial pose of the turtlebot3 with the button the 2D Pose Estimate.&#x20;

\
![](https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAgTlZgwqw5iHxfEMJeLS%2Fimage.png?alt=media\&token=0cef9217-7124-4634-8edb-9be2ade78b94)![](https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FP8Dj8mGmGeHveuR2QILk%2Fimage.png?alt=media\&token=91705a88-6c43-4d68-9d7f-a221962c1dc8)

After the pose is set the autonomous navigation should be possible.

Use the Nav2 Goal button to set a desired goal. After setting the Turtlebot3 should start with the navigation.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FBFQXCaT3tvXTrBuxXD7U%2Fimage.png?alt=media&amp;token=a553f3d0-9475-456d-af31-2cd4edf629fc" alt=""><figcaption></figcaption></figure>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FpWmcDM60Kuj9Sdgz7uY9%2FRobot_navigation_demo.gif?alt=media&amp;token=68a374d4-d557-428b-9ddc-6185ef84cd28" alt=""><figcaption></figcaption></figure>

Try to navigate to point and drop an obstacle in Gazebo

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FkDB45xKwFiyqiGEg3xkl%2Fimage.png?alt=media&amp;token=2695327e-9ebf-417d-a2ba-e5f4c6be0e40" alt=""><figcaption></figcaption></figure>

You see the calculated path will change when the obstacle is detected.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FLz8BZqjl6PJmOcqXeUvd%2FRobot_navigation_obstacle_demo.gif?alt=media&amp;token=c234f926-d41c-4b28-8430-d3b8c64009ac" alt=""><figcaption></figcaption></figure>
