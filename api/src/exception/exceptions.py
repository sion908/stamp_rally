class SimpleException(Exception):  # noqa: N818
    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code


class TeamRegistrationError(Exception):  # noqa: N818
    def __init__(self, message: str="チームに登録されていません", rep_token: str=None):
        self.custom_rep = True
        self.message = message
        self.status_code = 404
        self.rep_token = rep_token


class UserAlreadyRegistrationError(Exception):  # noqa: N818
    def __init__(self, team_name=""):
        self.message = f"すでにチームに登録されています: {team_name}"
        self.status_code = 404
