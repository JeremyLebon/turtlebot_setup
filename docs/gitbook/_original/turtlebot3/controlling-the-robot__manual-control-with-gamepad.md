> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/controlling-the-robot/manual-control-with-gamepad.md).

# Manual control with gamepad

Open a new WSL terminal.

Connect to the turtlebot with SSH.

```
ssh turtlebot-rpi5@192.168.60.6x
```

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

Connect to the Docker container running on the turtlebot&#x20;

```
docker exec -it turtlebot_x bash
```

Start the following command

```
ros2 launch teleop_twist_joy teleop-launch.py
```

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FF9Fn7DrS7oJJmsJaDlSe%2Fimage.png?alt=media&amp;token=36070f3a-4f16-45fd-8450-7c7ccf767160" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The last line should be Opened joystick
{% endhint %}

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FAInHd8tz8SdHAoj52wGQ%2Fimage.png?alt=media&amp;token=34cf715e-bf11-46ab-99d3-1e5a64e7aba7" alt=""><figcaption></figcaption></figure>

How to control the turtlebot

1. Press the right joystick continuously (enable button)
2. Use the left joystick to control the turtlebot.

Try to drive around. This can be later used to map the environment.

Show the progress to the lecturer.
