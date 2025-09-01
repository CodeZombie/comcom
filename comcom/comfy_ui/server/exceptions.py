INDENT: int = 7

def format_network_error(server_url, broad_error, specific_error, granular_error):
    return f"{broad_error.replace('\n', ' - ')} at [underline]{server_url}[/]\n{' '*INDENT}{specific_error.replace('\n', ' - ')}\n{' '*INDENT}{granular_error.replace('\n', ' - ')}"


class ComfyConnectionError(Exception):
    def __init__(self, message, server_url, error_message):
        super().__init__(format_network_error(
            server_url=server_url,
            broad_error="Could not connect to server",
            specific_error=message,
            granular_error=error_message
        ))

class ComfyServerError(Exception):
    def __init__(self, message, server_url, error_message):
        super().__init__(format_network_error(
            server_url=server_url,
            broad_error="Internal Server Error",
            specific_error=message,
            granular_error=error_message
        ))

class PromptExecutionError(Exception): pass