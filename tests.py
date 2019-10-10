from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_shopping_list_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_shopping_list = {
    'title': 'Birthday List',
    'description': 'Good gifts',
    'images': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w']    
}
sample_form_data = {
    'title': sample_shopping_list['title'],
    'description': sample_shopping_list['description'],
    'images': '\n'.join(sample_shopping_list['images'])
}


class Shopping_ListsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the shopping lists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Shopping List', result.data)

    def test_new(self):
        """Test the new shopping list creation page."""
        result = self.client.get('/shopping_lists/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Shopping List', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_shopping_list(self, mock_find):
        """Test editing a single shopping list."""
        mock_find.return_value = sample_shopping_list

        result = self.client.get(f'/shopping_lists/{sample_shopping_list}')
        self.assertIn(b'Birthday List', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_shopping_list(self, mock_find):
        """Test showing a single shopping list"""
        mock_find.return_value = sample_shopping_list

        result = self.client.get(f'/shopping_lists/{sample_shopping_list_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Birthday List', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_shopping_list(self, mock_insert):
        """Test submitting a new shopping_list."""
        result = self.client.post('/shopping_lists', data=sample_form_data)

        #After submitting, should redirect to the page of that shopping list
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_shopping_list)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_shopping_list(self, mock_update):
        result = self.client.post(f'/shopping_lists/{sample_shopping_list_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_shopping_list_id}, {'$set': sample_shopping_list})
    
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_playlist(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/shopping_lists/{sample_shopping_list_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_shopping_list_id})



if __name__ == '__main__':
    unittest_main()