"""
Тесты для калькулятора обратной польской нотации (RPN)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

cd = os.path.dirname(os.path.abspath(__file__))
pd = os.path.dirname(cd)
fp = os.path.join(pd, 'src')
sys.path.insert(0, fp)

import pytest
from calculator import RPNCalculator


def test_basic_operations() -> None:
    """Тестирование базовых операций калькулятора

    Тестовые случаи: (выражение, ожидаемый результат, описание)"""
    calculator = RPNCalculator()

    test_cases = [
        ("3 4 +", 7, "Простое сложение"),
        ("5 3 -", 2, "Простое вычитание"),
        ("2 3 *", 6, "Простое умножение"),
        ("6 2 /", 3.0, "Простое деление"),
        ("3 4 2 * +", 11, "Комбинированная операция"),
        ("5 1 2 + 4 * + 3 -", 14, "Сложное выражение"),
        ("2 3 **", 8, "Возведение в степень"),
        ("7 3 //", 2, "Целочисленное деление"),
        ("7 3 %", 1, "Остаток от деления"),
        ("10.5 2.5 +", 13.0, "Дробные числа"),
        ("0 5 +", 5, "Сложение с нулем"),
        ("5 0 +", 5, "Сложение с нулем"),
    ]

    print("Тесты базовых операций:")
    for expression, expected, description in test_cases:
        result = calculator.evaluate(expression)
        assert abs(result - expected) < 1e-10, f"Тест '{description}' не пройден: {expression}"
        print(f"  ✓ {description}: '{expression}' = {result}")


def test_error_cases() -> None:
    """Тестирование обработки ошибок

    Тестовые случаи ошибок: (выражение, ожидаемая ошибка, описание)"""
    calculator = RPNCalculator()

    error_cases = [
        ("3 4 + +", ValueError, "Недостаточно операндов"),
        ("3 4", ValueError, "Некорректное выражение"),
        ("3 0 /", ZeroDivisionError, "Деление на ноль"),
        ("3.5 2 //", ValueError, "Целочисленные операнды для //"),
        ("3.5 2 %", ValueError, "Целочисленные операнды для %"),
        ("abc 4 +", ValueError, "Некорректный токен"),
        ("", ValueError, "Пустое выражение"),
        ("   ", ValueError, "Пустое выражение с пробелами"),
    ]

    print("\nТесты обработки ошибок:")
    for expression, expected_error, description in error_cases:
        try:
            calculator.evaluate(expression)
            pytest.fail(f"Тест '{description}' не вызвал ожидаемую ошибку")
        except expected_error:
            print(f"  ✓ {description}: корректно вызвана ошибка для '{expression}'")
        except Exception as e:
            pytest.fail(f"Тест '{description}' вызвал неожиданную ошибку: {e}")


def test_complex_expressions() -> None:
    """Тестирование сложных выражений"""
    calculator = RPNCalculator()

    complex_cases = [
        ("15 7 1 1 + - / 3 * 2 1 1 + + -", 5, "Сложное выражение со всеми операциями"),
        ("2 3 ** 4 5 + *", 72, "Комбинация степени и умножения"),
        ("10 2 / 3 * 4 +", 19, "Последовательные операции"),
    ]

    print("\nТесты сложных выражений:")
    for expression, expected, description in complex_cases:
        result = calculator.evaluate(expression)
        assert abs(result - expected) < 1e-10, f"Тест '{description}' не пройден: {expression}"
        print(f"  ✓ {description}: '{expression}' = {result}")


def test_operator_precedence() -> None:
    """Тестирование того, что в RPN приоритеты не важны - важен порядок"""
    calculator = RPNCalculator()

    cases = [
        ("3 4 2 * +", 11),  # 3 + (4 * 2)
        ("3 4 * 2 +", 14),  # (3 * 4) + 2
    ]

    print("\nТесты приоритета операций в RPN:")
    for expression, expected in cases:
        result = calculator.evaluate(expression)
        assert result == expected, f"Неверный результат для {expression}"
        print(f"  ✓ '{expression}' = {result}")


if __name__ == "__main__":
    test_basic_operations()
    test_error_cases()
    test_complex_expressions()
    test_operator_precedence()
    print("\nВсе тесты пройдены успешно!")
