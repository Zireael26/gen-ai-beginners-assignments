from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn

load_dotenv()

app = FastAPI(title="Calculator MCP API")

@app.post("/multiply")
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together.

    args:
        a (float): The first number.
        b (float): The second number.
    returns:
        float: The product of the two numbers.
    """
    return a * b

@app.post("/divide")
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

@app.post("/add")
def add(a: float, b: float) -> float:
    """Adds two numbers together.

    args:
        a (float): The first number.
        b (float): The second number.
    returns:
        float: The sum of the two numbers.
    """
    return a + b

@app.post("/subtract")
def subtract(a: float, b: float) -> float:
    """Subtracts one number from another.

    args:
        a (float): The number to subtract from.
        b (float): The number to subtract.
    returns:
        float: The difference of the two numbers.
    """
    return a - b

@app.post("/exp")
def exp(a: float, b: float) -> float:
    """Raises one number to the power of another.

    args:
        a (float): The base number.
        b (float): The exponent.
    returns:
        float: The result of raising a to the power of b.
    """
    return a ** b

@app.post("/modulus")
def modulus(a: float, b: float) -> float:
    """Calculates the modulus of one number by another.

    args:
        a (float): The dividend.
        b (float): The divisor.
    returns:
        float: The remainder of the division of a by b.
    """
    return a % b

mcp = FastApiMCP(app, name="Calculator MCP")
mcp.mount_http()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)