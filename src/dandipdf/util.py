from dandy_lib.geometry import Point, Segment


def stroke_to_seg(stroke: dict[str, list[str]]) -> Segment:
    if not stroke["type"] in ["s", "sf"]:
        raise ValueError("no stroke")

    # ToDo see about handling non single strokes here
    if len(stroke["items"]) != 1:
        raise ValueError("Too many!")

    if not stroke["items"][0][0] == "l":
        raise ValueError("Wat do?")
    pt_a, pt_b = stroke["items"][0][1:]
    return Segment(Point(pt_a.x, pt_a.y), Point(pt_b.x, pt_b.y))
