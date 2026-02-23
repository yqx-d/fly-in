from typing import Any, Union


class Parser:

    @staticmethod
    def get_content(
        path: str
    ) -> list[str]:

        try:
            with open(path, "r") as f:
                lines = f.readlines()

            for line in lines:
                line.rstrip('\n')

            return lines

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
    ) -> Union[dict[Any, Any], None]:

        ...
