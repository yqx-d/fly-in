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
