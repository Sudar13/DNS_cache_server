import vk_api
import pandas as pd
from getpass import getpass

def get_friends_list():
    # Запрашиваем токен у пользователя
    token = getpass("Введите ваш токен доступа VK API: ")
    
    try:
        # Инициализируем сессию
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        
        # Получаем список друзей
        friends = vk.friends.get(fields=['first_name', 'last_name', 'online', 'last_seen'])
        
        # Создаем список для хранения данных
        friends_data = []
        
        # Обрабатываем каждого друга
        for friend in friends['items']:
            friend_info = {
                'Имя': friend['first_name'],
                'Фамилия': friend['last_name'],
                'Онлайн': 'Да' if friend.get('online', 0) == 1 else 'Нет',
                'Последний визит': friend.get('last_seen', {}).get('time', 'Неизвестно')
            }
            friends_data.append(friend_info)
        
        # Создаем DataFrame
        df = pd.DataFrame(friends_data)
        
        # Выводим таблицу
        print("\nСписок друзей:")
        print(df.to_string(index=False))
        
        # Сохраняем в CSV файл
        df.to_csv('friends_list.csv', index=False, encoding='utf-8')
        print("\nСписок друзей также сохранен в файл 'friends_list.csv'")
        
    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка API ВКонтакте: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    get_friends_list()
