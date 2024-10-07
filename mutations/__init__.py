import os


def load_gql(filename):
    """Load a GraphQL query from a .graphql file."""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, "r") as file:
        return file.read()


sfapi_customer_access_token_create = load_gql("storefrontCustomerAccessTokenCreate.graphql")
