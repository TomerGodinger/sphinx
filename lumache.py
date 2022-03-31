from typing import Union, List

def get_random_ingredients(kind: Union[List[str], None]=None) -> List[str]:
    """
    Return a list of random ingredients as strings.

    Args:
        kind: Optional "kind" of ingredients.
    
    Returns:
        The ingredients list.
    
    Raises:
        lumache.InvalidKindError: If the kind is invalid.
    """
    return ["shells", "gorgonzola", "parsley"]

class InvalidKindError(Exception):
    """Raised if the kind is invalid."""
    pass
