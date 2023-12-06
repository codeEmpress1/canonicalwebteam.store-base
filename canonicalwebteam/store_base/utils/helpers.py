def get_icon(media):
    icons = [m["url"] for m in media if m["type"] == "icon"]
    if len(icons) > 0:
        return icons[0]
    return ""
