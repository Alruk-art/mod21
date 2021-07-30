@pytest.fixture(autouse=True)
def get_key(self):
   self.pf = PetFriends()
   status, self.key = self.pf.get_API_key(valid_email, valid_password)
   assert status == 200
   assert 'key' in self.key

   yield

   assert self.status == 200

def test_getAllPetsWithValidKey(self, filter=''):  # filter available values : my_pets
   self.status, result = self.pf.get_list_of_pets(self.key, filter)
   assert len(result['pets']) > 0
