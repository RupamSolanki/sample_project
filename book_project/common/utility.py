from rest_framework.authtoken.models import Token

def generate_token(user_inst):
    """
    This function create to generate user token
    """
    token, created = Token.objects.get_or_create(user=user_inst)
    return token.key