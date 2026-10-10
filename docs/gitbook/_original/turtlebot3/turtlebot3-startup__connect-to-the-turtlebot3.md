> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/connect-to-the-turtlebot3.md).

# Connect to the turtlebot3

Check the number of the turtlebot. See the sticker on the RPI5 on the turtlebot3. This number is important for some commands.

Open a WSL terminal and open an SSH tunnel with the turtlebot.

Check if the turtlebot is available by using the following command. Change `x` by the turtlebot number

```
ping 192.168.60.6x
```

You should get a response like

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2F86QxEA1A7J54qdEZAPAj%2Fimage.png?alt=media&amp;token=dc138e96-371c-4eac-886c-4911c45476b3" alt=""><figcaption></figcaption></figure>

Connect with turtlebot with ssh command

```sh
ssh turtlebot-rpi5@192.168.60.6x
```

username: turtlebot-rpi5

IP address: 192.168.60.6x

Password: xxx - see lab notes

{% hint style="warning" %}
Important: the password remains invisible!!
{% endhint %}

Say `yes` when a fingerprint is suggested

If successful, you are now inside the turtlebot via Wifi
