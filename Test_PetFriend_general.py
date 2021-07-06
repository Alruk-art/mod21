import sys
sys.path.append("..")
import pytest
import os


from sf_21.api_pf import PetFriends
from sf_21.settings_pf import valid_email, valid_password, invalid_email, invalid_email_2, invalid_password, invalid_password_2
from sf_21.test_data_generators import chinese_chars, russian_chars, special_chars, generate_string

pf = PetFriends()

class TestFunctions:


    #@pytest.fixture(autouse=True)

    def test_get_key(petfr, email=valid_email, password=valid_password):
        petfr.pf = pf
        status, petfr.key = petfr.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in petfr.key
        print ('Key =', petfr.key)

    #print('auth_key=', auth_key, 'status =', status, )
    #@pytest.mark.smoke
    #@pytest.mark.negative
    @pytest.mark.parametrize("email", [valid_email, 'None'], ids=['valid_em', 'empty_em'])
    @pytest.mark.parametrize("password", [valid_password, 'None'], ids=['valid_ps', 'empty_ps'])

    def test_1_get_api_key_check(petfr, email, password):
        print (email, password)
        status, result = pf.get_api_key(email, password)
        if status == 200:
            print ('status 200, key in result')
        else:
            assert status == 403
            print('status 403, key not in result')


    # def logging(self, request):
    #     ''' Функция логирования для задания 21.6.4,
    #     реализовано: создание файла, внесение кода ответа, тела ответа
    #     не реализовано: перечислены заголовки запроса, параметры пути, параметры строки и тело запроса
    #     '''
    #     yield
    #
    #     with open('log.txt', 'at', encoding='utf8') as log_file:
    #         log_file.write(f'\n============Test::{request.node.name}================\n')
    #         # log_file.write(f'Test name: {request.function.__name__}\n')
    #         log_file.write(f'Status code: {str(self.status)}\n')
    #         log_file.write(f'Body: {self.result}\n')
    #         log_file.write(f'Exp: {request.response}\n')


    @pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_2_get_all_pets_check(petfr, filter):  # filter available values : my_pets
        _, petfr.key = pf.get_api_key(valid_email, valid_password)
        petfr.status, petfr.result = pf.get_list_of_pets(petfr.key, filter)
        print('key=', petfr.key)
        assert len(petfr.result['pets']) > 0
        assert petfr.status == 200
        if filter == 'my_pets':
            print (petfr.result)
    #@pytest.mark.smoke
    #@pytest.mark.negative
    #@pytest.mark.xfail

    @pytest.mark.parametrize("filter",
                             [generate_string(255),
                              generate_string(1001),
                              russian_chars(),
                              russian_chars().upper(),
                              chinese_chars(),
                              special_chars(),
                              123
                              ]
        , ids=['255 symbols'
            , 'more than 1000 symbols'
            , 'russian'
            , 'RUSSIAN'
            , 'chinese'
            , 'specials'
            , 'digit'])

    def test_3_get_all_pets_with_another_filter(self, filter):
        _, self.key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.get_list_of_pets(self.key, filter)
        assert status == 500
        print (status)
        print('auth_key=',self.key, 'status =',status, )




    def test_4_add_new_pet_with_valid_data(name='danger', animal_type='virus',
                                     age='3', pet_photo='pictures/covirus.jpg'):
        """Проверяем что можно добавить питомца с корректными данными.   """

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        print()
        print('result=',result)
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200



def test_8_add_new_pet_with_wrong_data(name='Stuart'*100, animal_type='mask'*100,
                                     age='-444444', pet_photo='pictures/mask.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(invalid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert result['name'] == name
    print()
    print('result [name]=', result['name'])

def test_9_add_new_pet_with_invalid_data(name='Stuart', animal_type='терьер',
                                     age='44', pet_photo='pictures/big_photo.jpg'):
    """Проверяем что можно добавить питомца с большим фото.
     но у меня плохой интернет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == 'Stuart'
    print()
    print('result [name]=',result['name'])

def test_10_add_new_pet_with_wrong_data(name='Stuart', animal_type='терьер',
                                     age='14', pet_photo='pictures/text_pf.txt'):
    """Проверяем что можно добавить питомца с некорректными расширением фото.
     В ответе, что фото с таким расширением не принимается сервером"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500
    assert result['age'] == '14'
    print()
    print('result [age]=', result['age'])

def test_11_add_new_pet_with_None(name=None, animal_type='терьер',
                                     age=None, pet_photo='pictures/mask.jpg'):
    """Проверяем что можно добавить питомца с None .
     Ответ не понял. Прошёл тест или нет. на странице ошибки нет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == None
    print()
    print('result [name]=', result['name'])

def test_12_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key,  "Суперкот", "кот", "3", "pictures/mask.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print()
    print ('pet_id=', pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_13_successful_update_self_pet_info(name='Мрзк', animal_type='Cat', age= 5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print()
        print('result [name]=', result['name'])
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# мои записи
def test_14_add_new_pet_simple_with_valid_data(name='Тигрик', animal_type='КОТОтище',
                                                age='19'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        print()
        assert status == 200
        print('status simple ADD name =', status)
        assert result['name'] == 'Тигрик'
        print('result [name]=', result['name'])
        assert result['age'] == '19'
        print('result [age]=', result['age'])
        assert result['animal_type'] == 'КОТОтище'
        print('result [animal_type]=', result['animal_type'])
        print()


def test_15_add_photo_pet(pet_photo='pictures/mask.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    print()
    print('Обновление фото для pet_id=', pet_id)

    status, result = pf.add_photo_pet(auth_key, pet_id,  pet_photo)

    assert status == 200
    print ('status=',status)
