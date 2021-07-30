import sys
sys.path.append("..")
import pytest
import os
from api_pf import PetFriends

@pytest.fixture()
def some_data():
    return 42

def test_some_data(some_data):
    assert some_data == 42

test_some_data(42)

@pytest.fixture(autouse=True)
def get_key(self):
   self.pf = PetFriends()
   status, self.key = self.pf.get_api_key('al66@pf.com', '1qasw2')
   assert status == 200
   assert 'key' in self.key

   yield

   assert self.status == 200

def test_getAllPetsWithValidKey(self, filter=''):  # filter available values : my_pets
   self.status, result = self.pf.get_list_of_pets(self.key, filter)
   assert len(result['pets']) > 0
