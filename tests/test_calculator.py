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


class TestRPNCalculator:
    """Класс тестов для RPN калькулятора"""

    def setup_method(self):
        """Инициализация калькулятора перед каждым тестом"""
        self.calculator = RPNCalculator()

    def test_basic_operations(self) -> None:
        """Тестирование базовых операций калькулятора"""
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
        ]

        print("Тесты базовых операций:")
        for expression, expected, description in test_cases:
            result = self.calculator.evaluate(expression)
            assert abs(result - expected) < 1e-10, f"Тест '{description}' не пройден: {expression}"
            print(f"  ✓ {description}: '{expression}' = {result}")

    def test_valid_parentheses(self) -> None:
        """Тестирование корректных выражений со скобками"""
        test_cases = [
            ("(3 4 +) 2 *", 14, "Скобки вокруг полного выражения"),
            ("3 (4 2 *) +", 11, "Скобки вокруг части выражения"),
            ("( ( 3 4 + ) )", 7, "Множественные скобки"),
            ("(3 4 + 5 *) 2 /", 17.5, "Сложное выражение в скобках"),
        ]

        print("\nТесты корректных скобок:")
        for expression, expected, description in test_cases:
            result = self.calculator.evaluate(expression)
            assert abs(result - expected) < 1e-10, f"Тест '{description}' не пройден: {expression}"
            print(f"  ✓ {description}: '{expression}' = {result}")

    def test_parentheses_balance_errors(self) -> None:
        """Тестирование ошибок баланса скобок"""
        error_cases = [
            ("((3 4 +) 2 *", "Незакрытые скобки"),
            ("(3 4 +)) 2 *", "Лишние закрывающие скобки"),
            (")3 4 +(", "Несбалансированные скобки"),
            ("(3 4 + 2 *", "Незакрытые скобки"),
            ("3 4 +) 2 *", "Лишние закрывающие скобки"),
        ]

        print("\nТесты ошибок баланса скобок:")
        for expression, description in error_cases:
            try:
                self.calculator.evaluate(expression)
                pytest.fail(f"Тест '{description}' не вызвал ожидаемую ошибку")
            except ValueError as e:
                assert "Несбалансированные скобки" in str(e)
                print(f"  ✓ {description}: '{expression}'")
            except Exception as e:
                pytest.fail(f"Тест '{description}' вызвал неожиданную ошибку: {e}")

    def test_parentheses_content_errors(self) -> None:
        """Тестирование ошибок содержимого скобок"""
        error_cases = [
            ("() 3 4 +", "Пустые скобки"),
            ("( ) 3 4 +", "Пустые скобки с пробелом"),
            ("(4 +) 2 *", "Незавершенное выражение в скобках"),
            ("(3 4) 2 *", "Незавершенное выражение в скобках"),
            ("(3 (4 +)) 2 *", "Вложенные некорректные скобки"),
            ("(() 3 4 +) 2 *", "Пустые вложенные скобки"),
        ]

        print("\nТесты ошибок содержимого скобок:")
        for expression, description in error_cases:
            try:
                self.calculator.evaluate(expression)
                pytest.fail(f"Тест '{description}' не вызвал ожидаемую ошибку")
            except ValueError as e:
                assert any(msg in str(e) for msg in ["Пустые скобки", "Незавершенное выражение"])
                print(f"  ✓ {description}: '{expression}'")
            except Exception as e:
                pytest.fail(f"Тест '{description}' вызвал неожиданную ошибку: {e}")

    def test_arithmetic_errors(self) -> None:
        """Тестирование арифметических ошибок"""
        error_cases = [
            ("3 0 /", ZeroDivisionError, "Деление на ноль"),
            ("3 0 //", ZeroDivisionError, "Целочисленное деление на ноль"),
            ("3.5 2 //", ValueError, "Целочисленные операнды для //"),
            ("3.5 2 %", ValueError, "Целочисленные операнды для %"),
        ]

        print("\nТесты арифметических ошибок:")
        for expression, expected_error, description in error_cases:
            try:
                self.calculator.evaluate(expression)
                pytest.fail(f"Тест '{description}' не вызвал ожидаемую ошибку")
            except expected_error:
                print(f"  ✓ {description}: '{expression}'")
            except Exception as e:
                pytest.fail(f"Тест '{description}' вызвал неожиданную ошибку: {e}")

    def test_syntax_errors(self) -> None:
        """Тестирование синтаксических ошибок"""
        error_cases = [
            ("3 4 + +", "Недостаточно операндов"),
            ("3 4", "Некорректное выражение"),
            ("abc 4 +", "Некорректный токен"),
            ("", "Пустое выражение"),
            ("   ", "Пустое выражение с пробелами"),
            ("12.34.56 2 +", "Некорректный формат числа"),
            ("1a2 3 +", "Некорректный числовой формат"),
        ]

        print("\nТесты синтаксических ошибок:")
        for expression, description in error_cases:
            try:
                self.calculator.evaluate(expression)
                pytest.fail(f"Тест '{description}' не вызвал ожидаемую ошибку")
            except ValueError:
                print(f"  ✓ {description}: '{expression}'")
            except Exception as e:
                pytest.fail(f"Тест '{description}' вызвал неожиданную ошибку: {e}")

    def test_complex_expressions(self) -> None:
        """Тестирование сложных выражений"""
        complex_cases = [
            ("15 7 1 1 + - / 3 * 2 1 1 + + -", 5, "Сложное выражение со всеми операциями"),
            ("2 3 ** 4 5 + *", 72, "Комбинация степени и умножения"),
            ("10 2 / 3 * 4 +", 19, "Последовательные операции"),
        ]

        print("\nТесты сложных выражений:")
        for expression, expected, description in complex_cases:
            result = self.calculator.evaluate(expression)
            assert abs(result - expected) < 1e-10, f"Тест '{description}' не пройден: {expression}"
            print(f"  ✓ {description}: '{expression}' = {result}")

    def test_operator_precedence(self) -> None:
        """Тестирование приоритета операций в RPN"""
        cases = [
            ("3 4 2 * +", 11),  # 3 + (4 * 2)
            ("3 4 * 2 +", 14),  # (3 * 4) + 2
            ("5 1 2 + 4 * + 3 -", 14),  # 5 + ((1 + 2) * 4) - 3
        ]

        print("\nТесты приоритета операций в RPN:")
        for expression, expected in cases:
            result = self.calculator.evaluate(expression)
            assert result == expected, f"Неверный результат для {expression}"
            print(f"  ✓ '{expression}' = {result}")


def run_all_tests():
    """Запуск всех тестов"""
    test_class = TestRPNCalculator()

    test_methods = [
        test_class.test_basic_operations,
        test_class.test_valid_parentheses,
        test_class.test_parentheses_balance_errors,
        test_class.test_parentheses_content_errors,
        test_class.test_arithmetic_errors,
        test_class.test_syntax_errors,
        test_class.test_complex_expressions,
        test_class.test_operator_precedence,
    ]

    for method in test_methods:
        test_class.setup_method()
        method()

    print("\nВсё успешно пройдено! Победа!")


if __name__ == "__main__":
    run_all_tests()
