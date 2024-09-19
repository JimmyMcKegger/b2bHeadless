import os


def load_query(filename):
    """Load a GraphQL query from a .graphql file."""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, "r") as file:
        return file.read()


customer_query = load_query("customerQuery.graphql")
