"""
Главный модуль RPN калькулятора
Точка входа в приложение
"""

from calculator import RPNCalculator
from constants import SUPPORTED_OPERATORS


def print_help() -> None:
    """Выводит справку по использованию калькулятора"""
    print("RPN Калькулятор (Обратная Польская Нотация)")
    print("~*" * 25)
    print("Операции:")
    for operator, description in SUPPORTED_OPERATORS.items():
        print(f"  '{operator}' = {description}")
    print("Примеры:")
    print("  3 + (-4) RPN — 3 -4 +         → результат: -1")
    print("  3 * 4 + 2 в RPN —  3 4 2 * +  → результат: 11")
    print("  (3 + 4) * 5 в RPN — 3 4 + 5 * → результат: 35")
    print("Команды:")
    print("  help - показать справку")
    print("  exit - выйти из программы")
    print("*~" * 25)


def genius() -> None:
    print('''く__,.ヘヽ.　　　　/　,ー､ 〉
　　　　　＼ ', !-─‐-i　/　/´
　　　 　 ／｀ｰ'　　　 L/／｀ヽ､
　　 　 /　 ／,　 /|　 ,　 ,　　　 ',
　　　ｲ 　/ /-‐/　ｉ　L_ ﾊ ヽ!　 i
　　　 ﾚ ﾍ 7ｲ｀ﾄ　 ﾚ'ｧ-ﾄ､!ハ|　 |
　　　　 !,/7 '0'　　 ´0iソ| 　 |　　　
　　　　 |.从"　　_　　 ,,,, / |./ 　 |
　　　　 ﾚ'| i＞.､,,__　_,.イ / 　.i 　|
　　　　　 ﾚ'| | / k_７_/ﾚ'ヽ,　ﾊ.　|
　　　　　　 | |/i 〈|/　 i　,.ﾍ |　i　|
　　　　　　.|/ /　ｉ： 　 ﾍ!　　＼　|
　　　 　 　 kヽ>､ﾊ 　 _,.ﾍ､ 　 /､!
　　　　　　 !'〈//｀Ｔ´', ＼ ｀'7'ｰr'
　　　　　　 ﾚ'ヽL__|___i,___,ンﾚ|ノ
　　　　　 　　　ﾄ-,/　|___./
　　　　　 　　　'ｰ'　　!_,.:
            dev1lan did it!!!
             thanks and bye!''')


def run_interactive_mode() -> None:
    """Запускает интерактивный режим калькулятора"""
    calculator = RPNCalculator()
    print_help()
    while True:
        try:
            expression = input("\nВведите выражение в RPN: ").strip()

            if expression.lower() in ('exit', 'i love hse'):
                print("До свидания!")
                break
            elif expression.lower() == 'help':
                print_help()
                continue
            elif not expression:
                continue
            elif expression.lower() == 'dev1lan':
                genius()
                break

            result = calculator.evaluate(expression)
            print(f"Результат: {result}")

        except (ValueError, ZeroDivisionError) as err:
            print(f"Ошибка: {err}")
        except Exception as err:
            print(f"Неожиданная ошибка: {err}")


def main() -> None:
    """Основная функция - точка входа в приложение (запуск программы)"""
    try:
        run_interactive_mode()
    except:
        pass


if __name__ == "__main__":
    exit(main())
