import sys

sys.path.append ("")
import pytest
import os

from SF_mod_21.api_pf import PetFriends
from SF_mod_21.settings_pf import valid_email, valid_password
from SF_mod_21.test_data_generators import russian_chars, special_chars, generate_string

pf = PetFriends ()


class TestFunctions:

    @pytest.fixture (autouse=True)
    def get_key(self):
        print ('Тест запущен')
        self.pf = pf
        status, self.key = self.pf.get_api_key (valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

       # assert self.status == 200



    @pytest.mark.api
    @pytest.mark.xfail
    @pytest.mark.parametrize ("email", [valid_email, 'None', generate_string (255)],
                              ids=['valid_em', 'empty_em', 'generate_string(255)'])
    @pytest.mark.parametrize ("password", [valid_password, 'None', generate_string (255)],
                              ids=['valid_ps', 'empty_ps', 'generate_string(255)'])
    # проверка с разными паролями и почтой
    def test_1_get_api_key_check_api(self, email, password):
        print ('\n email=', email, '\n password=', password)
        self.status,_ = self.pf.get_api_key (email, password)
        assert self.status == 200


    def logging(self, request):
        ''' Функция логирования для задания 21.6.4,
         реализовано: создание файла, внесение кода ответа, тела ответа
         не реализовано: перечислены заголовки запроса, параметры пути, параметры строки и тело запроса
         '''
        yield

        with open ('log.txt', 'at', encoding='utf8') as log_file:
            log_file.write (f'\n============Test::{request.node.name}================\n')
            log_file.write (f'Test name: {request.function.__name__}\n')
            log_file.write (f'Status code: {str (self.status)}\n')
            log_file.write (f'Body: {self.result}\n')
            log_file.write (f'Exp: {request.response}\n')

    @pytest.mark.ui
    @pytest.mark.xfail
    @pytest.mark.parametrize ("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_2_get_all_pets_check_ui(self, filter):  # filter available values : my_pets
        # _, petfr.key = pf.get_api_key(valid_email, valid_password)
        self.status, self.result = self.pf.get_list_of_pets (self.key, filter)
        """ проверка на наличие своих питомцев
            если их нет, то выводим 'нет', если есть выводим результат
            для всех питомцев выводим статус """
        if len (self.result['pets']) > 0:
            assert len (self.result['pets']) > 0
        else:
            assert len (self.result['pets']) == 0
        assert self.status == 200
        print ('\n filter =', filter)
        print ('status', self.status)
        if filter == 'my_pets' and len (self.result['pets']) == 0:
            print ('\n У вас нет питомцев')
        elif filter == 'my_pets' and len (self.result['pets']) > 0:
            print ('result', self.result)

    # @pytest.mark.smoke
    # @pytest.mark.negative
    @pytest.mark.xfail
    @pytest.mark.parametrize ("filter",
                              [generate_string (255),
                               generate_string (256),
                               russian_chars (),
                               special_chars (),
                               123
                               ]
        , ids=['255 symbols'
            , 'more than 256 symbols'
            , 'russian'
            , 'specials'
            , 'digit'])
    def test_3_get_all_pets_with_another_filter(self, filter):
        # status, self.key = pf.get_api_key (valid_email, valid_password)
        self.status, self.result = self.pf.get_list_of_pets (self.key, filter)
        assert self.status == 500
        print ('\n status =', self.status, )

    """Проверяем что можно добавить питомца с корректными данными.   """

    @pytest.mark.parametrize ('name', ['danger'], ids=['valid name'])
    @pytest.mark.parametrize ('animal_type', ['virus'], ids=['animal_type'])
    @pytest.mark.parametrize ('age', ['3'], ids=['age'])
    # Интересно. что пайтон не пропускает большие файлы и с неверным расширением
    @pytest.mark.parametrize ('pet_photo',
                              ['pictures\mask.jpg',
                               'pictures\covirus.jpg'],
                              ids=['valid_photo_1', 'valid_photo_2'])

    def test_4_add_new_pet_with_valid_data(self, name, animal_type, age, pet_photo):
        pet_photo = os.path.join (os.path.dirname (__file__), pet_photo)
        self.status, self.result = self.pf.add_new_pet (self.key, name, animal_type, age, pet_photo)
        assert self.result['name'] == "danger"
        assert self.result['animal_type'] == 'virus'
        assert self.result['age'] == '3'
        # assert self.result['pet_photo'] == 'data:image/jpeg;base64,'
        assert self.status == 200
        print ('\n status =', self.status, )

    """ Тест на добавления питомца без фото, для уменьшения тестов разбиты на два этапа
        в первом меняются имя и тип питомца, во втором меняется возраст """

    @pytest.mark.parametrize ("name"
        , [generate_string (255), generate_string (256), russian_chars (),
           special_chars (), '123']
        , ids=['255 symbols', 'more than 255 symbols', 'russian', 'specials', 'digit'])
    @pytest.mark.parametrize ("animal_type"
        , ['', generate_string (255), generate_string (256), russian_chars (), special_chars (), '123']
        , ids=['empty', '255 symbols', 'more than 256 symbols', 'russian',
               'specials', 'digit'])
    @pytest.mark.parametrize ("age", ['1'], ids=['min'])
    # первый этап
    def test_5a_add_new_pet_simple_without_photo(self, name, animal_type, age):
        self.status, self.result = self.pf.add_new_pet_simple (self.key, name, animal_type, age)
        assert self.status == 200
        assert self.result['name'] == name
        assert self.result['age'] == age
        assert self.result['animal_type'] == animal_type

    @pytest.mark.parametrize ("name", ['Name'], ids=['Name'])
    @pytest.mark.parametrize ("animal_type", ['animal_type'], ids=['Animal type'])
    @pytest.mark.parametrize ("age"
        , ['', '0', '-1', '1', '1,5', '100', '2147483647', '2147483648', special_chars (),
           russian_chars ()]
        , ids=['empty', '0', 'negative', '1', '1.5', 'greater than max', 'int_max',
               'int_max + 1', 'specials', 'russian'])
    # второй этап
    def test_5b_add_new_pet_simple_without_photo(self, name, animal_type, age):
        self.status, result = pf.add_new_pet_simple (self.key, name, animal_type, age)
        # ожидается, что будут приняты только разумные значения по возрасту
        if self.status == 400:
            assert self.status == 400
            print ('Unsave')
        if self.status == 200:
            assert self.status == 200
            print ('Save')
        else:
            print ('another')

    @pytest.mark.ui
    def test_6_successful_delete_self_pet_ui(self):
        """Проверяем возможность удаления питомца"""
        # Получаем  список своих питомцев
        _, my_pets = self.pf.get_list_of_pets (self.key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len (my_pets['pets']) == 0:
            pf.add_new_pet (self.key, "Суперкот", "кот", "3", "pictures/mask.jpg")
            _, my_pets = pf.get_list_of_pets (self.key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        print ()
        print ('pet_id=', pet_id)
        status, _ = pf.delete_pet (self.key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets (self.key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values ()

    @pytest.mark.ui
    @pytest.mark.parametrize ('name', ['Мурзик'], ids=['valid name'])
    @pytest.mark.parametrize ('animal_type', ['кошка'], ids=['animal_type'])
    @pytest.mark.parametrize ('age', [5], ids=['age'])
    def test_7_successful_update_self_pet_info_ui(self, name, animal_type, age):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        _, my_pets = self.pf.get_list_of_pets (self.key, "my_pets")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len (my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info (self.key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == "Мурзик"
            print ('\n result [name]=', result['name'])
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception ("There is no my pets")

    @pytest.mark.parametrize ('pet_photo',
                              ['pictures\covirus.jpg'],
                              ids=['photo'])
    def test_8_add_photo_pet(self, pet_photo):
        pet_photo = os.path.join (os.path.dirname (__file__), pet_photo)
        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets (self.key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        print ('\n Обновление фото для pet_id=', pet_id)

        status, result = self.pf.add_photo_pet (self.key, pet_id, pet_photo)

        assert status == 200
        print ('status=', status)
