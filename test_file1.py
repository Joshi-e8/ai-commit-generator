"""Test file 1 for multi-file commit testing."""

def function_one():
    """This is a new function in file 1."""
    return "Hello from file 1"

def function_one_enhanced():
    """Enhanced version with error handling."""
    try:
        return "Hello from enhanced file 1"
    except Exception as e:
        return f"Error: {e}"

class TestClass1:
    """A test class in file 1."""
    
    def __init__(self):
        self.name = "TestClass1"
    
    def get_info(self):
        return f"This is {self.name}"
