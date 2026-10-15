"""Build the complete books in docs/gitbook/<book>/ from the pages there plus the
originals in docs/gitbook/_original/ (downloaded from GitBook on 2026-10-11):
missing pages are copied from the original, then SUMMARY.md (GitBook table of
contents), OVERZICHT.md (status per page) and BOOK.md (everything in reading
order) are (re)generated. The status compares each page with its original.

    cd docs/gitbook && python3 _tools/build_books.py

Edit pages in docs/gitbook/<book>/..., then run this again."""
import os, re, sys

GB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(GB, "_original")
BOOKS = {
    "turtlebot3": ("Turtlebot3", "turtlebot3", "https://vives-4.gitbook.io/turtlebot3/",
                   # new pages: (insert after this path, new path, title)
                   [("autonomous-driving-with-python-library.md", "compare-planners-and-controllers.md", "Compare planners and controllers"),
                    ("compare-planners-and-controllers.md", "zones.md", "Zones"),
                    ("turtlebot3-startup/setup-laptop-student.md", "theory.md", "Theory: what the robot measures"),
                    ("turtlebot3-in-the-real-world.md", "installation.md", "Installation"),
                    ("theory.md", "theory/laser-scan.md", "Laser scan (/scan)"),
                    ("theory/laser-scan.md", "theory/odometry.md", "Odometry (/odom) and encoders"),
                    ("theory/odometry.md", "theory/imu.md", "IMU (/imu)"),
                    ("theory/imu.md", "theory/tf.md", "TF - coordinate frames"),
                    ("theory/tf.md", "theory/cmd-vel.md", "Driving the robot (/cmd_vel)"),
                    ("theory/cmd-vel.md", "theory/qos.md", "QoS - Quality of Service")]),
    "simulation": ("ROS2 - Simulation - Turtlebot - Gazebo", "simulation", "https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/",
                   [("autonomous-navigation/autonomous-driving-with-python-library.md", "simulation-vs-real-robot.md", "Simulation vs. real robot"),
                    ("turtlebot-in-simulation/here-come-the-sensors.md", "turtlebot-in-simulation/theory.md", "Theory: what the robot measures"),
                    ("turtlebot-in-simulation/theory.md", "turtlebot-in-simulation/theory/laser-scan.md", "Laser scan (/scan)"),
                    ("turtlebot-in-simulation/theory/laser-scan.md", "turtlebot-in-simulation/theory/odometry.md", "Odometry (/odom) and wheels"),
                    ("turtlebot-in-simulation/theory/odometry.md", "turtlebot-in-simulation/theory/imu.md", "IMU (/imu)"),
                    ("turtlebot-in-simulation/theory/imu.md", "turtlebot-in-simulation/theory/tf.md", "TF - coordinate frames"),
                    ("turtlebot-in-simulation/theory/tf.md", "turtlebot-in-simulation/theory/cmd-vel.md", "Driving the robot (/cmd_vel)"),
                    ("turtlebot-in-simulation/theory/cmd-vel.md", "turtlebot-in-simulation/theory/qos.md", "QoS - Quality of Service")]),
}

# Optional order of the top-level pages (a page moves together with its subpages).
# Top-level pages not listed keep their place after the listed ones.
ORDER = {
    "turtlebot3": [
        "turtlebot3-in-the-real-world.md", "installation.md", "turtlebot3-startup.md",
        "visualise-the-robot.md", "controlling-the-robot.md", "see-turtlebot3-topics.md",
        "play-a-sound.md", "ros2-nodes.md", "simulation-of-sensors.md",
        # SLAM / navigation (hidden for now: 'hidden: true' front matter)
        "slam.md", "autonomous-driving.md", "autonomous-driving-with-python-library.md",
        "compare-planners-and-controllers.md", "zones.md",
        "measure-while-driving.md", "solution-measure-while-driving.md",
        # reference
        "install-python-libraries-in-container.md", "location-files-on-wsl.md", "theory.md",
    ],
}


# Pages of the original book that are dropped on purpose (content moved elsewhere).
REMOVED = {
    "turtlebot3": ["objectives.md"],   # merged into turtlebot3-in-the-real-world.md (2026-10-15)
}


def top(path):
    return path.split("/")[0].replace(".md", "")


def fpath(book, path):
    """File of a page. GitBook stores a page that has subpages as <dir>/README.md
    (its export after Git Sync renamed e.g. theory.md -> theory/README.md);
    use that file when it exists, else <page>.md. 'path' stays the logical
    page path (original lookup, nesting depth, ORDER)."""
    readme = path[:-3] + "/README.md"
    return readme if os.path.exists(os.path.join(GB, book, readme)) else path


def is_hidden(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return bool(m and re.search(r"^hidden:\s*true\s*$", m.group(1), re.M))


for book, (title, dl, base, new_pages) in BOOKS.items():
    index = open(os.path.join(DL, dl + "_index.txt")).read()
    pages = []   # (path, title)
    for t, url in re.findall(r"- \[([^\]]+)\]\((https://[^)]+\.md)\)", index):
        pages.append((url[len(base):], t))
    for after, path, t in new_pages:
        i = [p for p, _ in pages].index(after)
        pages.insert(i + 1, (path, t))

    pages = [(p, t) for p, t in pages if p not in REMOVED.get(book, [])]

    if book in ORDER:
        order = [top(p) for p in ORDER[book]]
        missing = [p for p in ORDER[book] if p not in [q for q, _ in pages]]
        assert not missing, missing
        pos = {k: i for i, k in enumerate(order)}
        pages.sort(key=lambda pt: pos.get(top(pt[0]), len(order)))   # stable: subpages keep their order

    status = {}
    for path, t in pages:
        dst = os.path.join(GB, book, fpath(book, path))
        src = os.path.join(DL, dl, path.replace("/", "__"))
        orig = None
        if os.path.exists(src):
            orig = re.sub(r"^> For the complete documentation index.*\n\n?", "", open(src).read(), flags=re.M)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "w").write(orig.replace("/root/ros_ws", "/root/ros2_ws"))
        cur = open(dst).read()
        if orig is None:
            status[path] = "nieuw"
        elif cur.strip() == orig.strip():
            status[path] = "ongewijzigd"
        elif cur.strip() == orig.replace("/root/ros_ws", "/root/ros2_ws").strip():
            status[path] = "kleine aanpassing (ros2_ws)"
        else:
            status[path] = "gewijzigd"

    # SUMMARY.md (GitBook format) + status labels in an HTML comment-free list
    lines = ["# Table of contents", ""]
    for path, t in pages:
        depth = path.count("/")
        lines.append("  " * depth + "* [%s](%s)" % (t.replace("_", "\\_"), fpath(book, path)))   # as GitBook writes it
    open(os.path.join(GB, book, "SUMMARY.md"), "w").write("\n".join(lines) + "\n")

    label = {"gewijzigd": "🟠 gewijzigd", "nieuw": "🟢 nieuw", "ongewijzigd": "⚪ ongewijzigd",
             "kleine aanpassing (ros2_ws)": "🟡 kleine aanpassing (ros2_ws)"}
    ov = ["# %s - overzicht" % title, "",
          "Volgorde zoals in GitBook. Klik een pagina aan, of lees alles achter elkaar in [BOOK.md](BOOK.md).", "",
          "| # | Pagina | Status |", "|---|---|---|"]
    for n, (path, t) in enumerate(pages, 1):
        hidden = " 🙈 verborgen" if is_hidden(open(os.path.join(GB, book, fpath(book, path))).read()) else ""
        ov.append("| %d | %s[%s](%s) | %s%s |" % (n, "&nbsp;&nbsp;&nbsp;&nbsp;" * path.count("/"), t, fpath(book, path), label[status[path]], hidden))
    counts = {}
    for v in status.values():
        counts[v] = counts.get(v, 0) + 1
    ov += ["", "Samen: " + ", ".join("%d %s" % (c, k) for k, c in counts.items()) + "."]
    open(os.path.join(GB, book, "OVERZICHT.md"), "w").write("\n".join(ov) + "\n")

    book_md = ["# %s" % title, "",
               "_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/%s/`._" % book, ""]
    for n, (path, t) in enumerate(pages, 1):
        body = open(os.path.join(GB, book, fpath(book, path))).read().strip()
        body = re.sub(r"^---\n.*?\n---\n+", "", body, count=1, flags=re.S)   # GitBook front matter (hidden: true)
        body = re.sub(r"^# .*\n", "", body, count=1)            # page title comes from the header below
        h = "#" * min(2 + path.count("/"), 4)
        book_md += ["---", "", "%s %d. %s  `[%s]`" % (h, n, t, status[path]), "", "<sub>%s</sub>" % fpath(book, path), "", body, ""]
    open(os.path.join(GB, book, "BOOK.md"), "w").write("\n".join(book_md) + "\n")
    print(book, len(pages), "pagina's:", counts)
