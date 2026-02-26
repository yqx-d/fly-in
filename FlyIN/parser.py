from typing import Any, Union, Dict


class Parser:

    @staticmethod
    def get_content(
        path: str
    ) -> list[str]:

        try:
            with open(path, "r") as f:
                lines = f.readlines()

            lst_line = []
            for line in lines:
                if not line.startswith('#'):
                    line = line.rstrip('\n')
                    line = line.strip()
                    lst_line.append(line)

            if not lines[0].startswith('nb_drones'):
                raise ValueError(
                    "First line wrong format.\n"
                    f"line: '{lines[0]}'.")

            return lst_line

        except PermissionError:
            raise PermissionError(
                f"{path} permission error.")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"{path} not found.")

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def parse_data(
        data: list[str]
    ) -> str:

        if data[0] == "color":
            try:
                value = str(data[1]) # noqa
            except ValueError:
                raise ValueError(
                    f"Error: {data[0]}, wrong value: {data[1]}")

        elif data[0] == "zone":
            ...

        elif data[0] == "max_drones":
            ...

        elif data[0] == "max_link_capacity":
            ...

    @staticmethod
    def parse_metadata(
        string: str
    ) -> Union[Dict[str, Any], None]:

        if "[" in string and "]" in string:
            string = string.rstrip(']')
            cut_string = string.split('[')

            metadata = cut_string[1].split(' ')
            dict_metadata: Dict[str, Any] = {}

            try:
                for all_data in metadata:
                    data = all_data.split('=')
                    value = Parser.parse_data(data)
                    dict_metadata.update({data[0], value})

                if "color" not in dict_metadata:
                    dict_metadata.update({"color", None})

                if "zone" not in dict_metadata:
                    dict_metadata.update({"zone", "normal"})

                if "max_drones" not in dict_metadata:
                    dict_metadata.update({"max_drones", 1})

                if "max_link_capacity" not in dict_metadata:
                    dict_metadata.update({"max_link_capacity", 1})

            except Exception as e:
                raise Exception(e)

            return dict_metadata

        return None

    @staticmethod
    def parse_line(
        line: str
    ) -> Union[Dict[Any, Any], None]:

        try:
            lst_line = line.split(':')
            name_type = lst_line[0].strip()
            result = {}

            if name_type in ('start_hub', 'end_hub', 'hub'):
                try:
                    hub_content = lst_line[1].split(' ', 3)
                    name = hub_content[0]
                    x = int(hub_content[1])
                    y = int(hub_content[2])

                    result.update({
                            "type": hub_content,
                            "name": name,
                            "x": x,
                            "y": y
                        })

                    metadata = Parser.parse_metadata(lst_line[1])
                    if metadata:
                        result.update(metadata)

                except ValueError as e:
                    raise ValueError(e)

            elif name_type in ('connection'):
                try:
                    name1 = lst_line[1].split('-')[0].strip()
                    name2 = lst_line[1].split('-')[1].strip()

                    result.update({
                            "type": name_type,
                            "name1": name1,
                            "name2": name2
                        })

                    metadata = Parser.parse_metadata(lst_line[1])
                    if metadata:
                        result.update(metadata)

                except ValueError as e:
                    raise ValueError(e)

            elif name_type in ('nb_drones'):
                try:
                    drones = int(lst_line[1].strip())
                    if drones < 0:
                        raise ValueError("Negative value for 'nb_drones'.")

                    result.update({"nb_drones": drones})

                except ValueError:
                    raise ValueError("'nb_drones' does not contain integer.")
            else:
                raise ValueError(
                    f"{name_type} not valid.")

            return result

        except Exception as e:
            raise Exception(e)
