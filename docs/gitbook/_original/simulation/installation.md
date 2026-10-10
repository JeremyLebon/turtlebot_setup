> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/installation.md).

# Installation

For the lab WSL should already be installed.

Start WSL or the selected Ubuntu distro by searching the windows start menu.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3JbsPADcSfJN3Ymg4Fqs%2Fimage.png?alt=media&amp;token=c2fe29f7-1b47-4029-b729-5cb3ae869028" alt=""><figcaption></figcaption></figure>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3ZxKU4oI7Wk0x6MF1A3y%2Fimage.png?alt=media&amp;token=d0def977-488e-4abb-9c78-c9615f0cc2bc" alt=""><figcaption></figcaption></figure>

Clone the docker image repo

```sh
git clone https://github.com/JeremyLebon/ros2-jazzy-gazebo-turtlebot
```

Go inside the directory

```sh
cd ros2-jazzy-gazebo-turtlebot
```

Build the docker image to a docker container with the docker compose command

```sh
docker compose build
```

{% hint style="info" %}
This can take while.&#x20;
{% endhint %}

When build without errors the docker container can be started.

```sh
docker compose up
```

This should start without any error.

Open a second wsl terminal and check if the docker container is active with

```sh
docker ps
```

You should see that one container is active with the name `gazebo_turtlebot_cont`

Output:

```
CONTAINER ID   IMAGE                              COMMAND                  CREATED        STATUS          PORTS     NAMES
86c4097429f9   ros2-jazzy-gazebo-turtlebot-ros2   "/ros_entrypoint.sh …"   15 hours ago   Up 18 seconds             gazebo_turtlebot_cont
```

Now in the second terminal make connection with the docker container by typing:

```sh
docker exec -it gazebo_turtlebot_cont bash
```

{% hint style="info" %}
The `docker exec` lets you make a connection with the docker container via bash. Important is that the container name should be correct. With `TAB` it is normally autocompleted.
{% endhint %}
