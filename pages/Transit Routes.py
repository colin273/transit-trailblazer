from database import db
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

title = "Transit Routes"

st.set_page_config(
    page_title=title,
    page_icon="🗺️",
)

st.title(title)

# Rudimentary algorithm to figure out a transit route.
# It's really not the best, but it figures out something.

places = {place["name"]: {**place, "count": 0} for place in db["places"].find()}


for person in db["people"].find():
    # This is a really awful way of doing it, but time constraints are a factor
    # in how much I can get down in the weeds of data science.
    # Essentially not even measuring where people go, just where they are.
    # This whole algorithm needs to be replaced.
    places[person["live"]]["count"] += 1
    places[person["work"]]["count"] += 1


def point_neighbors(x, y, max_x, max_y):
    if x > 0:
        yield x - 1, y
    if x < max_x:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < max_y:
        yield x, y + 1


def calculate_route():
    # This is where the actual best-path algorithm goes
    # Start from the biggest location and follow a path to adjacent populated areas.
    # Don't revisit places.
    biggest_place = max(places.values(), key=lambda place: place["count"])
    max_x = max(places.values(), key=lambda place: place["x"])["x"]
    max_y = max(places.values(), key=lambda place: place["y"])["y"]

    biggest_neighbor = biggest_place

    while True:
        biggest_neighbor["visited"] = True
        path.append(biggest_neighbor)

        found_one = False

        neighbor_max = 0

        for neighbor_x, neighbor_y in point_neighbors(biggest_neighbor["x"], biggest_neighbor["y"], max_x, max_y):
            neighbor_place = [*filter(lambda place: place["x"] == neighbor_x and place["y"] == neighbor_y, places.values())][0]
            if "visited" in neighbor_place:
                continue
            if neighbor_place["count"] > neighbor_max:
                found_one = True
                neighbor_max = neighbor_place["count"]
                biggest_neighbor = neighbor_place

        if not found_one:
            break

    print([place["name"] for place in path])
    return path


st.text("See the generated public transit routes below.")

fig, ax = plt.subplots()

# Graph places
x_coords = [place["x"] for place in places.values()]
y_coords = [place["y"] for place in places.values()]
sizes = [place["count"] * 20 for place in places.values()]
ax.scatter(x_coords, y_coords, s=sizes)

for place in places.values():
    ax.text(place["x"], place["y"], place["name"])

# Graph route
path = calculate_route()
plot_x = [place["x"] for place in path]
plot_y = [place["y"] for place in path]
ax.plot(plot_x, plot_y, marker="o", color="red")

st.pyplot(fig)
