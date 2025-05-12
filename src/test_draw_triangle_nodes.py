import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def plot_triangle_with_nodes(
    integral_nodes: np.ndarray, output_img_name: str = "triangle_nodes.png"
) -> None:
    """
    在一个标准三角形区域 [(0,0), (1,0), (0,1)] 上绘制积分节点，
    并保存为图片（去掉坐标轴，只保留三角形和节点）。

    参数:
    integral_nodes (numpy.ndarray): n x 2 的数组，表示积分节点的坐标。
                           例如: np.array([[0.5, 0.2], [0.1, 0.1]])
    output_img_name (str): 保存图片的文件名。
    """
    (row, col) = integral_nodes.shape
    if col != 2:
        print("节点数据必须是 n x 2 的形状!")
    output_img_name = process_img_name(output_img_name)
    triangle_vertices = np.array([[0, 0], [1, 0], [0, 1]])
    return plot_triangle_with_nodes_base(
        triangle_vertices,
        integral_nodes,
        output_img_name,
    )


def process_nodes(triangle_vertices: np.array, integral_nodes: np.ndarray) -> np.array:
    vA = triangle_vertices[0, :]
    vB = triangle_vertices[1, :]
    vC = triangle_vertices[2, :]

    lambda_1 = integral_nodes[:, 0]
    lambda_2 = integral_nodes[:, 1]
    lambda_3 = 1 - lambda_1 - lambda_2

    mapped_nodes_x = lambda_1 * vA[0] + lambda_2 * vB[0] + lambda_3 * vC[0]
    mapped_nodes_y = lambda_1 * vA[1] + lambda_2 * vB[1] + lambda_3 * vC[1]
    return np.column_stack((mapped_nodes_x, mapped_nodes_y))


def process_img_name(img_name: str) -> str:
    """
    检查输入的文件名字符串是否以指定的图片后缀结尾。
    如果是，直接返回原字符串；
    如果不是，就在原字符串后加上 ".png" 并返回。

    参数:
    filename_str (str): 输入的文件名字符串。

    返回:
    str: 处理后的文件名字符串。
    """
    valid_extensions = (".png", ".jpg", ".jepg")
    low_img_name = img_name.lower()

    for ext in valid_extensions:
        if low_img_name.endswith(ext):
            return img_name

    return img_name + ".png"


def plot_triangle_with_nodes_transformed(
    triangle_vertices: np.array,
    integral_nodes: np.ndarray,
    output_img_name: str = "triangle_nodes.png",
) -> None:
    if triangle_vertices.shape != (3, 2):
        print("三角形的顶点数组形状不符合要求!")
        return
    (row, col) = integral_nodes.shape
    if col != 2:
        print("节点数据必须是 n x 2 的形状!")
    output_img_name = process_img_name(output_img_name)
    return plot_triangle_with_nodes_base(
        triangle_vertices,
        process_nodes(triangle_vertices, integral_nodes),
        output_img_name,
    )


def plot_triangle_with_nodes_base(
    triangle_vertices: np.array,
    nodes: np.ndarray,
    output_img_name: str = "triangle_nodes.png",
) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))  # 可以调整 figsize 来改变最终图片的大小比例

    # 绘制三角形
    # facecolor 是填充颜色，edgecolor 是边框颜色，linewidth 是边框粗细
    triangle_patch = Polygon(
        triangle_vertices,
        closed=True,
        edgecolor="black",
        facecolor="whitesmoke",
        linewidth=1.5,
    )
    ax.add_patch(triangle_patch)

    # 绘制积分节点
    # nodes[:, 0] 是所有节点的 x 坐标
    # nodes[:, 1] 是所有节点的 y 坐标
    # s 是节点大小, c 是节点颜色, zorder 确保节点在三角形之上
    ax.scatter(nodes[:, 0], nodes[:, 1], s=50, c="red", zorder=5, label="积分节点")
    x_min = min(triangle_vertices[:, 0])
    x_max = max(triangle_vertices[:, 1])
    y_min = min(triangle_vertices[:, 1])
    y_max = max(triangle_vertices[:, 1])
    # (｡・ω<｡) 设置坐标轴范围，确保三角形完整显示，并留一点点边距
    ax.set_xlim(x_min - 0.1, x_max + 0.1)
    ax.set_ylim(y_min - 0.1, y_max + 0.1)

    # 确保x和y轴的单位长度相同，这样三角形不会变形
    ax.set_aspect("equal", adjustable="box")

    # (つ✧ω✧)つ 最重要的一步：去掉坐标轴！
    ax.axis("off")

    # 保存图片
    # bbox_inches='tight' 会裁剪掉图片周围多余的空白
    # pad_inches=0 确保裁剪后没有额外的空白边距
    try:
        plt.savefig(
            output_img_name, bbox_inches="tight", pad_inches=0, dpi=300
        )  # dpi可以提高图片清晰度
        print(f"图片 '{output_img_name}' 保存成功啦！快去看看吧！✨")
    except Exception as e:
        print(f"呜呜，保存图片失败了... {e} (｡ŏ﹏ŏ)")

    # 关闭图形，释放内存 (在脚本中多次调用时很重要)
    plt.close(fig)


if __name__ == "__main__":

    # with open("triangle_formula.json", "r") as f:
    #     points_dict = json.load(f)
    # triangle_vertices = np.array([[-1, 0], [0, 1], [1, 0]])  # A'  # B'  # C'
    # for key, value in points_dict.items():
    #     plot_triangle_with_nodes_transformed(
    #         triangle_vertices, np.array(value)[:, 0:2], "./img/triangle/triangle_" + key
    #     )
    plot_triangle_with_nodes(
        np.array(
            [[0, 0], [0, 1 / 2], [0, 1], [1 / 2, 0], [1 / 2, 1 / 4], [1 / 2, 1 / 2]]
        ),
        "./img/triangle/triangle_simpsion",
    )
    plot_triangle_with_nodes(
        np.array(
            [[0, 0], [0, 1 / 2], [0, 1], [1 / 2, 0], [1 / 2, 1 / 4], [1 / 2, 1 / 2]]
        ),
        "./img/triangle/triangle_gauss_ORDER3POINT9",
    )
    plot_triangle_with_nodes(
        np.array(
            [[0, 0], [0, 1 / 2], [0, 1], [1 / 2, 0], [1 / 2, 1 / 4], [1 / 2, 1 / 2]]
        ),
        "./img/triangle/triangle_gauss_ORDER2POINT4",
    )
