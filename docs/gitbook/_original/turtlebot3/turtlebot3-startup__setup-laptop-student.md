> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/setup-laptop-student.md).

# Setup laptop (student)

## Configure WSL for networking

{% hint style="warning" %}
Very important step to get the ros2 topics inside the docker container
{% endhint %}

Configure WSL to communicate with the network.

Open a Powershell terminal as administrator

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FHTpXQfLD6A8krQSOQSqa%2Fimage.png?alt=media&amp;token=805c2780-a437-4e13-93d5-4f1672b08702" alt=""><figcaption></figcaption></figure>

Add the following in the terminal.

```powershell
Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow
```

<details>

<summary>Possible second solution</summary>

```powershell
netsh advfirewall firewall add rule name="Allow_All_Inbound" dir=in action=allow protocol=any profile=any
```

</details>

## Docker container

To command and read the TurtleBot, a new Docker container must be used.

```
git clone https://github.com/JeremyLebon/turtlebot_vis.git
```

Go inside the directory

```
cd turtlebot_vis
```

Build the container with

```
docker compose build
```

{% hint style="info" %}
This can take a while
{% endhint %}

Open the .env file inside the directory turtlebot\_vis

```
nano .env
```

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FX7rjV3xcLLStTTy3wO4c%2Fimage.png?alt=media&amp;token=9263e4c5-936f-4227-be33-34bf3cd5cfd8" alt=""><figcaption></figcaption></figure>

Change the number accordingly to the number of the turtlebot.

Press CRTL +S (save) press yes and the CRTL + X (close file)

Activate the docker container with the command below

```
docker compose up
```

Open a new WSL terminal and connect to the just started container

```
docker exec -it turtlebot-vis bash
```

Start Rviz2 with the following command

```
rviz2
```

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2F358y9Y6lKNKcf94P3dW1%2Fimage.png?alt=media&amp;token=2bb7486f-7890-48fd-8d0b-259ba79fc156" alt=""><figcaption></figcaption></figure>

When clicking Fixed Frame, you should see several frames/links available. Otherwise there is a problem.

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FXyNz5124MIqFe1vpD13l%2Fimage.png?alt=media&amp;token=d3337663-c089-4e4b-bf71-9c5a4198149e" alt=""><figcaption></figcaption></figure>
