import pygal

class BarGraphGenerator:
    """
    This class is used to create graphs using pygal

    Methods
    -------
    generate_bar_graph(data_dict, title="COMP000000 Stats", 
        min_y=0, max_y=None)
            Generates and saves a bar graph to a folder

    graph_name()
        Gets the name of the graph generated
    """

    def __init__(self, path2save, graph_name, save_format="svg"):
        """
        Parameters
        ----------
        path2save : str
            path to which the graph needs to be saved to
        
        graph_name : str
            name of the graph
        
        save_format : str, optional
            format in which the graph needs to be saved as
        """

        self._save_path = path2save
        self._graph_name = f"{graph_name}.{save_format}"
        self._abs_path_to_graph = f"{path2save}/{graph_name}.{save_format}" 

    def generate_graph(self, data_dict, title="COMP000000 Stats", 
                                                    min_y=0, max_y=None):
        """
        Generates and saves a bar graph to a folder

        Parameters
        ----------
        data_dict : dict
            dict containing the data which needs to be used for the graph. The 
            key is used as the x-axis and the value is used as the y-axis
        
        title : str, optional.
            Title for the graph. By default its "COMP000000 Stats"

        min_y : int, optional
            Minimum y value to be shown in the y axis. By default its 0

        max_y : int, optional
            Maximum y value to be shown in the y axis. By default it is None
        """

        x_labels = tuple(data_dict.keys())
        data_points = []

        for key in data_dict.keys():
            data_points.append(data_dict[key])

        bar_chart = pygal.Bar(
            style=pygal.style.BlueStyle, 
            show_legend=False, 
            title=title, 
            range=(min_y, max_y) if max_y != None else None,
            width=500,
            height=500,
            min_scale=0,
            max_scale=100
        )

        bar_chart.x_labels = x_labels
        bar_chart.add("y_label", data_dict)

        self.__save_graph(bar_chart)

    def __save_graph(self, graphObj):
        """
        Saves the graph into the file system
        """
        graphObj.render_to_file(self._abs_path_to_graph)

    @property
    def graph_name(self):
        return self._graph_name