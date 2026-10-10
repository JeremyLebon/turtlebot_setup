> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/install-python-libraries-in-container.md).

# Install python libraries in container

Needed to install libraries (Matplotlib, reportlab)

Go inside the docker `ros2-jazzy-gazebo-turtlebot`.

<pre><code><strong>apt update
</strong><strong>apt install python3.12-venv
</strong></code></pre>

Make venv

```
python -m venv .venv
```

Activate of venv

```
source .venv/bin/activate
```

Install the specific libraries with

```
python -m pip install matplotlib reportlab PyYAML pandas seaborn
```
