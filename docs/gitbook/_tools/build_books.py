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
                    ("compare-planners-and-controllers.md", "zones.md", "Zones")]),
    "simulation": ("ROS2 - Simulation - Turtlebot - Gazebo", "simulation", "https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/",
                   [("autonomous-navigation/autonomous-driving-with-python-library.md", "simulation-vs-real-robot.md", "Simulation vs. real robot")]),
}

for book, (title, dl, base, new_pages) in BOOKS.items():
    index = open(os.path.join(DL, dl + "_index.txt")).read()
    pages = []   # (path, title)
    for t, url in re.findall(r"- \[([^\]]+)\]\((https://[^)]+\.md)\)", index):
        pages.append((url[len(base):], t))
    for after, path, t in new_pages:
        i = [p for p, _ in pages].index(after)
        pages.insert(i + 1, (path, t))

    status = {}
    for path, t in pages:
        dst = os.path.join(GB, book, path)
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
        lines.append("  " * depth + "* [%s](%s)" % (t, path))
    open(os.path.join(GB, book, "SUMMARY.md"), "w").write("\n".join(lines) + "\n")

    label = {"gewijzigd": "🟠 gewijzigd", "nieuw": "🟢 nieuw", "ongewijzigd": "⚪ ongewijzigd",
             "kleine aanpassing (ros2_ws)": "🟡 kleine aanpassing (ros2_ws)"}
    ov = ["# %s - overzicht" % title, "",
          "Volgorde zoals in GitBook. Klik een pagina aan, of lees alles achter elkaar in [BOOK.md](BOOK.md).", "",
          "| # | Pagina | Status |", "|---|---|---|"]
    for n, (path, t) in enumerate(pages, 1):
        ov.append("| %d | %s[%s](%s) | %s |" % (n, "&nbsp;&nbsp;&nbsp;&nbsp;" * path.count("/"), t, path, label[status[path]]))
    counts = {}
    for v in status.values():
        counts[v] = counts.get(v, 0) + 1
    ov += ["", "Samen: " + ", ".join("%d %s" % (c, k) for k, c in counts.items()) + "."]
    open(os.path.join(GB, book, "OVERZICHT.md"), "w").write("\n".join(ov) + "\n")

    book_md = ["# %s" % title, "",
               "_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/%s/`._" % book, ""]
    for n, (path, t) in enumerate(pages, 1):
        body = open(os.path.join(GB, book, path)).read().strip()
        body = re.sub(r"^# .*\n", "", body, count=1)            # page title comes from the header below
        h = "#" * min(2 + path.count("/"), 4)
        book_md += ["---", "", "%s %d. %s  `[%s]`" % (h, n, t, status[path]), "", "<sub>%s</sub>" % path, "", body, ""]
    open(os.path.join(GB, book, "BOOK.md"), "w").write("\n".join(book_md) + "\n")
    print(book, len(pages), "pagina's:", counts)
