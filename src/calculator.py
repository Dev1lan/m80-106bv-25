"""
Модуль вычисления калькулятора обратной польской нотации (RPN)
"""

from typing import Union
from constants import SUPPORTED_OPERATORS, ERROR_MESSAGES

class RPNCalculator:
    """
    Калькулятор для вычисления выражений в обратной польской нотации (RPN)
    """

    def __init__(self) -> None:
        """Инициализация калькулятора с поддержкой операторов"""
        self.supported_operators = SUPPORTED_OPERATORS

    def _tokenize(self, expression: str) -> list[str]:
        """
        Разбивает строку выражения на токены

        Args:
            expression (str): Входное выражение в RPN

        Returns:
            list[str]: Список токенов (числа и операторы)
        """
        tokens = []
        current_token = ""

        for char in expression:
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def _parse_number(self, token: str) -> Union[int, float]:
        """
        Парсит токен в число

        Args:
            token (str): Токен для парсинга

        Returns:
            Union[int, float]: Числовое значение

        Raises:
            ValueError: Если токен не может быть преобразован в число
        """
        try:
            if '.' in token:
                return float(token)
            else:
                return int(token)
        except ValueError:
            raise ValueError(f"{ERROR_MESSAGES['invalid_token']}: {token}")

    def _apply_operator(self, operator: str, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Применяет оператор к двум операндам

        Args:
            operator (str): Оператор
            a (Union[int, float]): 1-ый операнд
            b (Union[int, float]): 2-ой операнд

        Returns:
            Union[int, float]: Результат операции

        Raises:
            ValueError: При ошибках операции
            ZeroDivisionError: При делении на ноль
        """
        operator_functions = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '//': lambda x, y: x // y,
            '%': lambda x, y: x % y,
            '**': lambda x, y: x ** y
        }

        if operator in ('//', '%'):
            if not isinstance(a, int) or not isinstance(b, int):
                raise ValueError(ERROR_MESSAGES['integer_operands_required'])

        if operator in ('/', '//') and b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['division_by_zero'])

        return operator_functions[operator](a, b)

    def evaluate(self, expression: str) -> Union[int, float]:
        """
        Вычисляет выражение в обратной польской нотации

        Args:
            expression (str): Выражение в обратной польской нотации (RPN)

        Returns:
            Union[int, float]: Результат вычисления

        Raises:
            ValueError: При ошибках в выражении или вычислении
            ZeroDivisionError: При делении на ноль
        """
        if not expression.strip():
            raise ValueError(ERROR_MESSAGES['empty_expression'])

        tokens = self._tokenize(expression)
        stack: list[Union[int, float]] = []

        for token in tokens:
            if token in self.supported_operators:
                if len(stack) < 2:
                    raise ValueError(f"{ERROR_MESSAGES['insufficient_operands']} '{token}'")

                b = stack.pop()
                a = stack.pop()

                try:
                    result = self._apply_operator(token, a, b)
                    stack.append(result)
                except (ValueError, ZeroDivisionError):
                    raise
                except Exception as e:
                    raise ValueError(f"Ошибка при выполнении операции {a} {token} {b}: {str(e)}")
            else:
                try:
                    number = self._parse_number(token)
                    stack.append(number)
                except ValueError:
                    raise

        if len(stack) != 1:
            raise ValueError(f"{ERROR_MESSAGES['invalid_expression']}. В стеке осталось {len(stack)} элементов")

        return stack[0]
