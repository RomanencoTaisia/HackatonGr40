from pathlib import Path
import main


def test_categorize_1():
    category = main.categorize_email(
        "Ураааа ты получил iPhone",
        "Быстро подтвердите личность!! Иначе аккаунт будет заблокирован",
        "promo@test.ru"
    )
    assert category == "Фишинг или спам"


def test_categorize_2():
    category = main.categorize_email(
        "Ошибка 500",
        "Работа остановлена",
        "admin@test.ru"
    )
    assert category == "Критический инцидент"


def test_categorize_3():
    category = main.categorize_email(
        "Новый сотрудник",
        "Нужно выдать доступ",
        "hr@test.ru"
    )
    assert category == "Запрос доступа"


def test_parse_email():
    text = """From: user@test.ru
Subject: Ошибка 500

Сервис не работает
"""
    subject, body, from_adressat = main.parse_email(text)
    assert subject == "Ошибка 500"
    assert from_adressat == "user@test.ru"
    assert "Сервис не работает" in body

def test_empty_email():
    empty_file = main.inp / "empty_test.txt"
    empty_file.write_text("", encoding="utf-8")
    main.process_emails()
    result_file = main.out / "Некорректные письма" / "empty_test.txt"
    assert result_file.exists()
    empty_file.unlink()
    result_file.unlink()

def test_wrong_extension():
    test_file = main.inp / "test_wrong_extension.pdf"
    test_file.write_text("test", encoding="utf-8")
    main.process_emails()
    result_file = main.out / "Неправильное расширение файла" / "test_wrong_extension.pdf"
    assert result_file.exists()
    test_file.unlink()
    result_file.unlink()
