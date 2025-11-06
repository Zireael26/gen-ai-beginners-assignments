from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(name="Calculator MCP")

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together.

    args:
        a (float): The first number.
        b (float): The second number.
    returns:
        float: The product of the two numbers.
    """
    return a * b

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divides one number by another.

    args:
        a (float): The numerator.
        b (float): The denominator.
    returns:
        float: The quotient of the two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@mcp.tool
def add(a: float, b: float) -> float:
    """Adds two numbers together.

    args:
        a (float): The first number.
        b (float): The second number.
    returns:
        float: The sum of the two numbers.
    """
    return a + b

@mcp.tool
def subtract(a: float, b: float) -> float:
    """Subtracts one number from another.

    args:
        a (float): The number to subtract from.
        b (float): The number to subtract.
    returns:
        float: The difference of the two numbers.
    """
    return a - b

@mcp.tool
def exp(a: float, b: float) -> float:
    """Raises one number to the power of another.

    args:
        a (float): The base number.
        b (float): The exponent.
    returns:
        float: The result of raising a to the power of b.
    """
    return a ** b

@mcp.tool
def sqrt(a: float) -> float:
    """Calculates the square root of a number.

    args:
        a (float): The number to calculate the square root of.
    returns:
        float: The square root of the number.
    """
    if a < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return exp(a, 0.5)

@mcp.tool
def modulo(a: float, b: float) -> float:
    """Calculates the modulo of one number by another.

    args:
        a (float): The dividend.
        b (float): The divisor.
    returns:
        float: The remainder of the division of a by b.
    """
    return a % b

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)