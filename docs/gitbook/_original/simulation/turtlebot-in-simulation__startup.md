> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/turtlebot-in-simulation/startup.md).

# Startup

Open a new terminal (Ubuntu 22.04).

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fsu1ojyU78ot109TUCruT%2Fimage.png?alt=media&amp;token=bd97d707-024e-45cb-b7f4-bdfc6f29c983" alt=""><figcaption></figcaption></figure>

Connect to the running Docker container with the command below.

```sh
docker exec -it gazebo_turtlebot_cont bash
```

Select the `burger` turtlebot3 as loaded model in Gazebo with the following command

```sh
export TURTLEBOT3_MODEL=burger
```

## Load the turtlebot in the turtlebot world

Start `ros2 launch` file with the command below. Normally, Gazebo should start with the standard turtle world.

{% hint style="info" %}
The  `ros2 launch` command lets you start several ros2 nodes with one command.&#x20;
{% endhint %}

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

Normally, the world below should be loaded. Try the find the turtlebot3 with the mouse and scrolling.

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAqtGNSo6CAyvDoyLjVAR%2Fimage.png?alt=media&amp;token=9e38f2e4-8593-4c06-8139-dd1ecaa342b1" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ45E9208uQDSv4e1ceNe%2Fimage.png?alt=media&amp;token=2833a4bb-a0e9-4f06-97a7-0efef922290c" alt=""><figcaption></figcaption></figure></div>

By clicking `CRTL+C` in the terminal gazebo and ros2 launch can be stopped.

## Load the turtlebot in the house world

Try the following command to drop the turtle in the house environment.

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
</strong></code></pre>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FITbPVgiVyF6yDsQRFA21%2Fimage.png?alt=media&amp;token=986a0d24-241a-42b1-b2c8-73de09b6c412" alt=""><figcaption></figcaption></figure>

By clicking `CRTL+C` in the terminal gazebo and ros2 launch can be stopped.
