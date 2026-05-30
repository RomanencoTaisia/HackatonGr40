import logging
from pathlib import Path

inp = Path("data/inbox")
out = Path("output")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def read_email(file_path):
    raw_data = file_path.read_bytes()

    try:
        return raw_data.decode("utf-8")
    except UnicodeDecodeError as e:
        logging.warning(f"В файле {file_path} проблемы с кодировкой: {e}")
        return raw_data.decode("utf-8", errors="replace")


def parse_email(text):
    subject = ""
    from_adressat = ""
    main_info_mail = []

    for line in text.splitlines():
        lower_line = line.lower()

        if lower_line.startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
        elif lower_line.startswith("from:"):
            from_adressat = line.split(":", 1)[1].strip()
        else:
            main_info_mail.append(line)

    body = "\n".join(main_info_mail)
    return subject, body, from_adressat


def categorize_email(subject, body, from_adressat):
    text = (subject + " " + body).lower()
    from_adressat = from_adressat.lower()

    if any(word in text for word in ["выиграли", "подтвердите личность", "аккаунт будет заблокирован"]):
        return "Фишинг или спам"

    if any(word in text for word in ["работа остановлена", "ошибка 500", "критичный инцидент"]):
        return "Критический инцидент"

    if any(word in text for word in ["ремонт", "гарнитура", "ноутбук", "принтер", "сканер", "мышь"]):
        return "Оборудование"

    if any(word in text for word in ["выдать доступ", "нужны права", "новый сотрудник"]):
        return "Запрос доступа"

    if "после обновления" in text:
        return "Проблема с ПО после обновления"

    if any(word in text for word in [
        "alerts@", "monitoring@", "zabbix@", "prometheus@", 
        "nagios@", "grafana@", "noreply@", "alert@",
        "monit@", "sensu@", "datadog@"
    ]):
        return "Мониторинг или оповещение"

    if any(word in text for word in ["счёт", "счет", "акт", "договор", "оплата", "согласование"]):
        return "Работа с клиентами"

    if any(word in text for word in ["дайджест", "выпуск"]):
        return "Корпоративная рассылка"

    if any(word in text for word in ["созвон", "демо", "встретиться"]):
        return "Встреча или созвон"

    if any(word in text for word in ["больничный", "отпуск"]):
        return "HR или не IT"

    return "Прочее"


def process_emails():
    out.mkdir(exist_ok=True)

    pisima_ineachcategoria = {}

    for email_file in inp.glob("*.txt"):
        text = read_email(email_file)

        subject, body, from_adressat = parse_email(text)
        category = categorize_email(subject, body, from_adressat)

        category_folder = out / category
        category_folder.mkdir(exist_ok=True)

        new_file = category_folder / email_file.name
        new_file.write_text(text, encoding="utf-8")

        pisima_ineachcategoria[category] = pisima_ineachcategoria.get(category, 0) + 1

        print(f"{email_file.name} -> {category}")

    return pisima_ineachcategoria


def main():
    print("Запуск программы распределения писем")

    if not inp.exists():
        print("Ошибка: папка data/inbox не найдена")
        return

    statistics = process_emails()

    print("Обработка завершена")


if __name__ == "__main__":
    main()