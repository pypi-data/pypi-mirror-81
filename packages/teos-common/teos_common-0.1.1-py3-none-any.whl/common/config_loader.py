import os
import configparser


class ConfigLoader:
    """
     The :class:`ConfigLoader` class is in charge of loading all the configuration parameters to create a config dict
     that can be used to set all configurable parameters of the system.

    Args:
        data_dir (:obj:`str`): the path to the data directory where the configuration file may be found.
        default_conf (:obj:`dict`): a dictionary populated with the default configuration params and the expected types.
            The format is as follows:

            ``{"field0": {"value": value_from_conf_file, "type": expected_type, ...}}``

        command_line_conf (:obj:`dict`): a dictionary containing the command line parameters that may replace the
            ones in default / config file.

    Attributes:
        data_dir (:obj:`str`): The path to the data directory where the configuration file may be found.
        conf_file_path (:obj:`str`): The path to the config file (the file may not exist).
        conf_fields (:obj:`dict`): A dictionary populated with the configuration params and the expected types.
            It follows the same format as ``default_conf``.
        command_line_conf (:obj:`dict`): A dictionary containing the command line parameters that may replace the
            ones in default / config file.
    """

    def __init__(self, data_dir, conf_file_name, default_conf, command_line_conf):
        self.data_dir = data_dir
        self.conf_file_path = os.path.join(self.data_dir, conf_file_name)
        self.conf_fields = default_conf
        self.command_line_conf = command_line_conf
        self.overwritten_fields = set()

    def build_config(self):
        """
        Builds a config dictionary from command line, config file and default configuration parameters.

        The priority is as follows:
            - command line
            - config file
            - defaults

        Returns:
            :obj:`dict`: A dictionary containing all the configuration parameters.
        """

        if os.path.exists(self.conf_file_path):
            file_config = configparser.ConfigParser()
            file_config.read(self.conf_file_path)

            # Load parameters and cast them to int if necessary
            if file_config:
                for sec in file_config.sections():
                    for k, v in file_config.items(sec):
                        k_upper = k.upper()
                        if k_upper in self.conf_fields:
                            if self.conf_fields[k_upper]["type"] == int:
                                try:
                                    self.conf_fields[k_upper]["value"] = int(v)
                                except ValueError:
                                    err_msg = "{} is not an integer ({}).".format(k, v)
                                    raise ValueError(err_msg)
                            else:
                                self.conf_fields[k_upper]["value"] = v

                            self.overwritten_fields.add(k_upper)

        # Override the command line parameters to the defaults / conf file
        for k, v in self.command_line_conf.items():
            self.conf_fields[k]["value"] = v
            self.overwritten_fields.add(k)

        # Extend relative paths
        expanded_data_dir = self.extend_paths()

        # Sanity check fields and build config dictionary
        config = self.create_config_dict()
        config["DATA_DIR"] = expanded_data_dir

        return config

    def create_config_dict(self):
        """
        Checks that the configuration fields (``self.conf_fields``) have the right type and creates a config dict if so.

        Returns:
            :obj:`dict`: A dictionary with the same keys as the provided one, but containing only the "value" field as
            value if the provided ``conf_fields`` are correct.

        Raises:
            ValueError: If any of the dictionary elements does not have the expected type.
        """

        conf_dict = {}

        for field in self.conf_fields:
            value = self.conf_fields[field]["value"]
            correct_type = self.conf_fields[field]["type"]

            if isinstance(value, correct_type):
                conf_dict[field] = value
            else:
                err_msg = "{} variable in config is of the wrong type".format(field)
                raise ValueError(err_msg)

        return conf_dict

    def extend_paths(self):
        """
        Extends the relative paths of the ``conf_fields`` dictionary with ``data_dir``.

        If an absolute path is given, it will remain the same.

        If the config contains a BTC_NETWORK field whose value is not "mainnet", it is also appended to the path.
        """

        # if there is a BTC_NETWORK parameter whose value is not "mainnet", we append it to the data_dir when expanding
        network_field = self.conf_fields.get("BTC_NETWORK")
        if network_field and network_field.get("value") != "mainnet":
            expanded_data_dir = os.path.join(self.data_dir, network_field.get("value"))
        else:
            expanded_data_dir = self.data_dir

        for key, field in self.conf_fields.items():
            if field.get("path") and isinstance(field.get("value"), str):
                self.conf_fields[key]["value"] = os.path.join(expanded_data_dir, self.conf_fields[key]["value"])

        return expanded_data_dir
