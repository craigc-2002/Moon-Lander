"""
Library to draw a graph onto a pygame screen
"""
import pygame


def line_graph(data, dims, axis_titles=(None, None), custom_margins=None):
    margins = [10, 10, 10, 10] if custom_margins is None else custom_margins
    graph = _draw_axes(dims, axis_titles, margins)

    scale_max_x = max(data[0])
    scale_max_y = max(data[1])
    display_points = []

    # Add points to graph (scaled to axes)
    for i in range(len(data[0])):
        display_points.append([margins[3]+round(((dims[0]-(margins[3]+margins[1]))*data[0][i])/scale_max_x, 2),
                               dims[1]-margins[2]-round(((dims[1]-(margins[0]+margins[2]))*data[1][i])/scale_max_y, 2)])
    pygame.draw.lines(graph, (255, 255, 255), False, display_points)

    # Return graph as a surface
    return graph


def multiline_graph(data, dims, axis_titles=(None, None), custom_margins=None):
    margins = [10, 10, 10, 10] if custom_margins is None else custom_margins
    graph = _draw_axes(dims, axis_titles, margins)

    scale_max_x = max(data[0])
    scale_max_y = max(data[1])
    display_points = []

    # Add points to graph (scaled to axes)
    for i in range(len(data[0])):
        display_points.append([margins[3]+round(((dims[0]-(margins[3]+margins[1]))*data[0][i])/scale_max_x, 2),
                               dims[1]-margins[2]-round(((dims[1]-(margins[0]+margins[2]))*data[1][i])/scale_max_y, 2)])
    pygame.draw.lines(graph, (255, 255, 255), False, display_points)

    # Return graph as a surface
    return graph


def _draw_axes(dims, axis_titles=(None, None), margins=None):
    surf = pygame.Surface(dims, flags=pygame.SRCALPHA)
    surf.fill((0, 0, 0, 155))

    axis_font = pygame.font.SysFont("Helvetica", 20)

    if axis_titles[0] is not None:
        x_title = axis_font.render(str(axis_titles[0]), False, (255, 255, 255))
        surf.blit(x_title, (((dims[0] / 2) - (x_title.get_width() / 2)), dims[1]-x_title.get_height()))
        margins[2] += x_title.get_height()
    if axis_titles[1] is not None:
        y_title = axis_font.render(str(axis_titles[1]), False, (255, 255, 255))
        y_title = pygame.transform.rotate(y_title, 90)
        surf.blit(y_title, (0, (dims[1]/2)-(y_title.get_height()/2)))
        margins[3] += y_title.get_width()

    # Draw axes
    pygame.draw.line(surf, (255, 255, 255), (margins[3], margins[0]), (margins[3], dims[1] - margins[2]), width=10)
    pygame.draw.line(surf, (255, 255, 255), (margins[3] - 4, dims[1] - margins[2]),
                     (dims[0] - margins[1], dims[1] - margins[2]), width=10)

    return surf
