class ComfyConnectionError(Exception):
    def __init__(self, message, server_url, error_message):
        super().__init__("{}\n       Could not connect to server: [underline]{}[/]\n       {}".format(message, server_url, error_message))