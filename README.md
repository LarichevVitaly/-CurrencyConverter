# Конвертер валют (Валюта -> RUB)
## Сборка
Сборка docker-контейнера:
```
docker build -t valute/service .
```
## Запуск сервиса
```
docker run -it -p 8000:8000 valute/service
```
После запуска сервиса доступ к нему осуществляется через 8000 порт.

## Пример запроса
### Request
Для конвертации валюты в RUB необходимо отправить POST-запрос по пути `/converter` со следующим содержимым JSON объекта:
```
{
    "Valute": String,
    "Value": Number
}
```
где `Valute` - это валюта (пример формата: "EUR"), а `Value` - это запрошенное значение.

### Response
В случае успеха сервис вернет следующий JSON объект:
```
{
    "Valute": String,
    "Value": Number,
    "Result": Number
}
```
В поле `Result` возвращается результирующее значение в рублях.
Данные о курсе валют берутся из ресурса ЦБ РФ: https://www.cbr-xml-daily.ru/