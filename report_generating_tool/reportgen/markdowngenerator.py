import jinja2

class MarkDownGenerator:
    """
    This class generates a markdown file as a feedback report

    Methods
    -------
    generate_file()
        Writes the markdown file to filesystem
    """

    def __init__(self, save_path, template_dst, template_name, md_name, data):
        """
        Parameters
        ----------
        save_path : str
            Path to save the markdown file

        template_dst : str
            Directory where the template(s) can be found

        template_name : str
            Name of the template to be used

        md_name : str
            The name in which the markdown file is to be saved as

        data : dict
            The data which needs to be rendered to the markdown template
        """

        self._template_dst = template_dst
        self._template_name = template_name
        self._data = data
        self._abs_path_to_md = f"{save_path}/{md_name}"

    def __write_file(self, contents):
        """
        Writes the markdown file to the filesystem

        Parameters
        ----------
        contents : str
            Contents which needs to be saved

        Returns
        -------
        Boolean
            True if file was saved else False
        """

        try:
            file2write = open(self._abs_path_to_md, "w")
            file2write.write(contents)
            file2write.close()
        except Exception as e:
            print("Error: Error writing markdown file: ", e)
            return False
        
        return True
            
    def __read_template(self):
        """
        Reads in the Jinja2 template and adds in the data required by it

        Returns
        -------
        str
            A string containing the final markdown string with all the data
            populated
        """

        fileloader = jinja2.FileSystemLoader(f"{self._template_dst}")
        environment = jinja2.Environment(loader=fileloader)

        template_to_use = environment.get_template(self._template_name)
        template_output = template_to_use.render(data=self._data)

        return template_output

    def generate_file(self):
        """
        Writes the markdown file to filesystem

        Returns
        -------
        Boolean
            Returns True if the file was saved to file system else False
        """

        return self.__write_file(self.__read_template())