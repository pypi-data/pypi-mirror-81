from .resource import Resource


class User(Resource):
    """
    represents User() entity

    Attributes:
        session(requests.Session): requests session
        data(dict): all userData is stored inside this dict
        url
        filter
    """
    def __init__(self, url, session):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", {})
        object.__setattr__(self, "url", url + "UserAccount()")
        object.__setattr__(self, "filter", "?$filter=UserName eq '%s'")

    def get(self, username):
        """
        get user by username and fill :attr:`~data` with received data

        """
        object.__setattr__(self, "username", username)
        data = self.session.get(self.url + self.filter % username)
        if data.status_code == 200:
            object.__setattr__(self, "data", data.json()["value"][0])

    def update(self):
        data = self.session.patch(self.url[:-1] + f"{self.data['UserAccountId']})", data=self.data)
        if data.status_code == 200:
            self.data = data.json()["value"][0]
        return data
