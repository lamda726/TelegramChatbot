import requests
from decouple import config


url = 'https://translation.googleapis.com/language/translate/v2'
key = config('GOOGLE_TOKEN')
data = {
    'q' : '엄마 판다는 새끼가 있네',
    'source' : 'ko',
    'target' : 'en',
    'format' : 'text'

}
result = requests.post(f'{url}?key={key}',data).json()
print(result)



# https://api.telegram.org/bot821566613:AAH8GrDzUHYJskpsNKXkutr4-Benu5YdfdY/setWebhook?url=https://726lamdawan.pythonanywhere.com/821566613:AAH8GrDzUHYJskpsNKXkutr4-Benu5YdfdY