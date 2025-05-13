#!/usr/bin/env python
import sys
import os
from latex2sympy2 import latex2sympy
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, request, jsonify, send_from_directory

import json
import numpy as np
import matplotlib


matplotlib.use("Agg")  # Use Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
import io
import base64
import sympy

app = Flask(__name__, static_folder="static", static_url_path="")

# --- Helper Functions (adapted from test_draw_triangle_nodes.py and new ones) ---


def draw_triangle_and_nodes(
    vertices,
    nodes,
    node_color="r",
    edge_color="b",
    fill_color="lightblue",
    show_axes=True,
):
    """
    Draws a triangle and integration nodes.
    vertices: list of 3 tuples, e.g., [(x1, y1), (x2, y2), (x3, y3)]
    nodes: list of N tuples for node coordinates, e.g., [(nx1, ny1), (nx2, ny2), ...]
    """
    fig, ax = plt.subplots()

    # Draw triangle
    triangle_patch = plt.Polygon(
        vertices, closed=True, edgecolor=edge_color, facecolor=fill_color, linewidth=1.5
    )
    ax.add_patch(triangle_patch)
    # Draw nodes
    if nodes:
        nodes = process_nodes(vertices, nodes)

        node_x = [n[0] for n in nodes]
        node_y = [n[1] for n in nodes]
        ax.scatter(
            node_x, node_y, c=node_color, s=50, zorder=5
        )  # s is size, zorder to draw on top

    # Set plot limits and aspect ratio
    all_x = [v[0] for v in vertices] + ([n[0] for n in nodes] if nodes else [])
    all_y = [v[1] for v in vertices] + ([n[1] for n in nodes] if nodes else [])

    if not all_x or not all_y:  # Handle empty case
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
    else:
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        x_range = x_max - x_min if x_max > x_min else 1.0
        y_range = y_max - y_min if y_max > y_min else 1.0

        ax.set_xlim(x_min - 0.1 * x_range, x_max + 0.1 * x_range)
        ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)

    ax.set_aspect("equal", adjustable="box")

    if show_axes:
        ax.axhline(0, color="black", lw=0.5)
        ax.axvline(0, color="black", lw=0.5)
        ax.grid(True, linestyle="--", alpha=0.7)
    else:
        ax.axis("off")

    # Save to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)  # Close the figure to free memory
    return img_base64


def process_nodes(
    triangle_vertices: list[list[float]], integral_nodes: list[list[float]]
) -> list[list[float]]:
    vA, vB, vC = triangle_vertices
    mapped_x = [
        vA[0] * node[0] + vB[0] * node[1] + vC[0] * (1.0 - node[0] - node[1])
        for node in integral_nodes
    ]
    mapped_y = [
        vA[1] * node[0] + vB[1] * node[1] + vC[1] * (1.0 - node[0] - node[1])
        for node in integral_nodes
    ]
    mapped_nodes = np.column_stack((mapped_x, mapped_y))
    return mapped_nodes.tolist()


def calculate_triangle_square(triangle_vertices) -> float:
    """
    Calculate the area of a triangle given its vertices using the shoelace formula.

    Parameters:
    triangle_vertices (list of tuples): A list containing three tuples, each representing the (x, y) coordinates of a triangle vertex.

    Returns:
    float: The area of the triangle.
    """
    x1, y1 = triangle_vertices[0]
    x2, y2 = triangle_vertices[1]
    x3, y3 = triangle_vertices[2]

    # Use the shoelace formula to calculate the area
    area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0

    return area


# --- API Routes ---


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/formulas")
def get_formulas():
    """
    API endpoint to serve triangle integration formulas.

    This function will first try to fetch the formula data from an online source.
    If the request fails, it will try to load the formula data from a local file instead.
    If the local file is not found, it will return a 500 error with the error message.

    Returns:
    A JSON response containing the formula data.
    """
    try:
        return get_formulas_online()
    except requests.exceptions.RequestException or Exception as e:
        app.logger.warning(f"Error in /api/formulas: {str(e)}, trying offline")
        try:
            return get_formulas_offline()
        except FileNotFoundError or Exception as e:
            app.logger.error(f"Error in /api/formulas: {str(e)}")
            return jsonify({"error": str(e)}), 500


def get_formulas_online():
    formula_url = (
        "https://hsmkhexo.s3.ap-northeast-1.amazonaws.com/other/triangle_formula.json"
    )
    # try:
    response = requests.get(formula_url)
    response.raise_for_status()  # 检查HTTP请求是否成功

    original_formulas = response.json()
    transformed_formulas = {}
    for key, formula in original_formulas.items():
        data_array = formula["data"]
        formula_description = formula.get("description")  # 使用get()避免KeyError
        nodes = [[item[0], item[1]] for item in data_array]
        weights = [item[2] for item in data_array]
        transformed_formulas[key] = {
            "name": key,
            "description": (
                formula_description
                if formula_description is not None
                else f"预设的积分公式 {key}"
            ),
            "nodes": nodes,
            "weights": weights,
        }
    return jsonify(transformed_formulas)


def get_formulas_offline():

    formulas_path = os.path.join(os.path.dirname(__file__), "triangle_formula.json")
    with open(formulas_path, "r", encoding="utf-8") as f:
        original_formulas = json.load(f)

    transformed_formulas = {}
    for key, formula in original_formulas.items():
        data_array = formula["data"]
        foormula_description = formula["description"]
        nodes = [[item[0], item[1]] for item in data_array]
        weights = [item[2] for item in data_array]
        transformed_formulas[key] = {
            "name": key,  # Use the key as the name
            "description": (
                foormula_description
                if foormula_description is not None
                else f"预设的积分公式 {key}"
            ),  # Placeholder description
            "nodes": nodes,
            "weights": weights,
        }
    return jsonify(transformed_formulas)


@app.route("/api/plot", methods=["POST"])
def plot_nodes():
    try:
        data = request.get_json()
        vertices_data = data.get("vertices")
        nodes_data = data.get("nodes")

        node_color = data.get("node_color", "red")
        edge_color = data.get("edge_color", "black")
        fill_color = data.get("fill_color", "lightblue")
        show_axes = data.get("show_axes", True)

        if not vertices_data or len(vertices_data) != 3:
            return (
                jsonify(
                    {"error": "Invalid or missing vertices data. Expecting 3 vertices."}
                ),
                400,
            )

        vertices = [(v["x"], v["y"]) for v in vertices_data]
        # nodes_data is expected to be [[x,y],...] from JS

        img_base64 = draw_triangle_and_nodes(
            vertices, nodes_data, node_color, edge_color, fill_color, show_axes
        )
        return jsonify({"image_data": img_base64})

    except Exception as e:
        app.logger.error(f"Error in /api/plot: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/calculate", methods=["POST"])
def calculate_integral():
    try:
        data = request.get_json()
        vertices_data = data.get("vertices")
        func_str = data.get("func_str")
        nodes_coords = data.get("nodes")  # List of [x, y] coordinates
        weights = data.get("weights")  # List of weights

        if not vertices_data or len(vertices_data) != 3:
            return (
                jsonify(
                    {"error": "Invalid or missing vertices data. Expecting 3 vertices."}
                ),
                400,
            )
        if not func_str or nodes_coords is None or weights is None:
            return jsonify({"error": "Missing function string, nodes, or weights"}), 400

        if len(nodes_coords) != len(weights):
            return jsonify({"error": "Number of nodes and weights must match"}), 400
        vertices = [(v["x"], v["y"]) for v in vertices_data]

        try:
            sympy_expr = latex2sympy(func_str)
            x, y = sympy.sympify("x"), sympy.sympify("y")
        except Exception as e_latex:
            return (
                jsonify({"error": f"Error parsing function string: {str(e_latex)}"}),
                400,
            )

        try:
            func = sympy.lambdify((x, y), sympy_expr, modules=["numpy", "math"])
        except Exception as e_lambdify:
            return (
                jsonify(
                    {"error": f"Error creating callable function: {str(e_lambdify)}"}
                ),
                400,
            )
        nodes_coords = process_nodes(vertices, nodes_coords)
        integral_sum = 0
        for i in range(len(nodes_coords)):
            node_x, node_y = nodes_coords[i]
            weight = weights[i]
            try:
                term_value = func(node_x, node_y)
                integral_sum += weight * term_value
            except Exception as e_eval:
                return (
                    jsonify(
                        {
                            "error": f"Error evaluating function at node ({node_x},{node_y}): {str(e_eval)}"
                        }
                    ),
                    400,
                )

        return jsonify(
            {"result": float(integral_sum * calculate_triangle_square(vertices) * 2)}
        )

    except Exception as e:
        app.logger.error(f"Error in /api/calculate: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)
