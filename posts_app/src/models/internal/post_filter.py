class PostFilter:
    def __init__(
        self,
        expire: bool | None = None,
        route: str | None = None,
        owner: str | None = None,
    ):
        self.expire = expire
        self.route = route
        self.owner = owner
