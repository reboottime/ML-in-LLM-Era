# Python Grammars Accumulated

## Data Structure

- string
  - use `"""` for multiple line string
  - use `f""` to embed string variable
- merge dictionary with provided overrides

```python
default_params = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000,
    "temperature": 0.7
}

default_params.update(kwargs)

```

## OOP related properties

- `@staticmethod`
  - grammar

    ```python
    class Human:
      def __init__ (self, name: str):
          self.name = name
      
      @staticmethod
      def kind(): 
          return 'human being'
    ```

  - In Python, while a class instance can access static methods from its class, yet this is not recommended because it's misleading about the static methods nature.
- `@property`: it is similar to Javascript getter