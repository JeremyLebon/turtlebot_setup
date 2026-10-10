> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/start-mapping.md).

# Start mapping

Open a new terminal and connect to the docker container.

Add the following command

```sh
export TURTLEBOT3_MODEL=burger
```

Start the mapping script

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py slam:=True
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ1g74ImNk5Yt3xcrBrxs%2Fimage.png?alt=media&amp;token=4dfb77c9-0802-4d96-b259-77edadf94dad" alt=""><figcaption></figcaption></figure>

Rviz2 should be started.

You can see that a partially obstacle map is generated.&#x20;

Try to ride, move around and map the entire world.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FGdexf1LRrE5fHolpf73i%2Fimage.png?alt=media&amp;token=699a5a01-1eec-4580-bfdc-eacc7e79a9ec" alt=""><figcaption></figcaption></figure>
