import sys
sys.path.append("..")
import pytest
import os


from sf_21.api_pf import PetFriends
from sf_21.settings_pf import valid_email, valid_password, invalid_email, invalid_email_2, invalid_password, invalid_password_2
from sf_21.test_data_generators import chinese_chars, russian_chars, special_chars, generate_string

pf = PetFriends()

class TestFunctions:


    @pytest.fixture(autouse=True)
    def get_key(self):
        _, self.key = pf.get_api_key(valid_email, valid_password)
        print ('Тест запущен', self.key)

    def test_get_key(self, email=valid_email, password=valid_password):
        self.pf = pf
        status, self.key = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in self.key
        print ('Key =', self.key)

    #print('auth_key=', auth_key, 'status =', status, )
    #@pytest.mark.smoke
    #@pytest.mark.negative
    @pytest.mark.parametrize("email", [valid_email, 'None', generate_string(255)], ids=['valid_em', 'empty_em', 'generate_string(255)'])
    @pytest.mark.parametrize("password", [valid_password, 'None', generate_string(255)], ids=['valid_ps', 'empty_ps', 'generate_string(255)'])

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
    def test_2_get_all_pets_check(self, filter):  # filter available values : my_pets
        # _, petfr.key = pf.get_api_key(valid_email, valid_password)
        self.status, self.result = pf.get_list_of_pets(self.key, filter)
        print('key=', self.key)
        assert len(self.result['pets']) > 0
        assert self.status == 200
        if filter == 'my_pets':
            print (self.result)
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


    # def test_4_add_new_pet_with_valid_data(name='danger', animal_type='virus',
     #                                age='3', pet_photo='pictures/covirus.jpg'):
     #   """Проверяем что можно добавить питомца с корректными данными.   """


    @pytest.mark.parametrize("name"
            , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
               special_chars(), '123']
            , ids=['255 symbols', 'more than 255 symbols', 'russian',  'specials', 'digit'])
    @pytest.mark.parametrize("animal_type"
            , ['', generate_string(255), generate_string(1001), russian_chars()
               ,  special_chars(), '123']
            , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian',  'specials',
                   'digit'])
    @pytest.mark.parametrize("age"
        , ['', '-1', '0', '100', '1.5', '2147483647', special_chars(), russian_chars()]
        , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                'specials', 'russian'])

    def test_4_add_new_pet_simple_without_photo(self, name, animal_type, age):
            self.status, self.result = pf.add_new_pet_simple(self.key, name, animal_type, age)
            assert self.status == 200
            #assert self.result['name'] == name
            #assert self.result['age'] == age
            #assert self.result['animal_type'] == animal_type




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
