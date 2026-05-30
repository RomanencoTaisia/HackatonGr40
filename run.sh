#!/bin/bash

echo "Запуск сортировки писем"

if command -v python3 &> /dev/null
then
    python3 main.py
else
    python main.py
fi

echo "Готово"
