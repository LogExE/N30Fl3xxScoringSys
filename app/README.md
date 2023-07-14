## Запустить frontend+backend 

### (Важно) Применение изменений
Если до этого окружение уже разворачивалось, нужно заранее выполнить эту строчку:
```sh
docker-compose -f docker-compose.yml build
```

### Запуск
Наберите в командной строке:
```sh
docker-compose -f docker-compose.yml up -d
```

## Завершение работы
Для сворачивания нужно написать вот это:
```sh
docker-compose -f docker-compose.yml down
```
