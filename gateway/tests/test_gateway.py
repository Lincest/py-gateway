import unittest
from gateway import main


class TestGateway(unittest.TestCase):
    def setUp(self) -> None:
        self.app = main.create_app()
        self.service_name = 'gateway-test-server'
        self.client = self.app.test_client()

    def check(self, res):
        print('res = ', res.json)
        self.assertEqual(res.json['code'], 1)
        self.assertEqual(res.json['msg'], 'success')
        self.assertEqual(res.json['json']['key1'], 'key1')
        self.assertEqual(res.json['json']['key2'], 'key2')

    def test_get(self):
        res = self.client.get('/{}/get-test'.format(self.service_name))
        self.assertEqual(res.json['code'], 1)
        self.assertEqual(res.json['msg'], 'success')

    def test_get_with_params(self):
        res = self.client.get('/{}/get-test-params?key1={}&key2={}'.format(self.service_name, 'key1', 'key2'))
        self.check(res)

    def test_post_with_json_body(self):
        res = self.client.post('/{}/post-test'.format(self.service_name), json={'key1': 'key1', 'key2': 'key2'})
        self.check(res)

    def test_post_with_form(self):
        res = self.client.post('/{}/post-test-form'.format(self.service_name), data={
            'key1': 'key1', 'key2': 'key2'
        })
        self.check(res)

    def test_put(self):
        self.check(
            self.client.put('/{}/other-methods'.format(self.service_name), json={'key1': 'key1', 'key2': 'key2'}))

    def test_delete(self):
        self.check(
            self.client.delete('/{}/other-methods'.format(self.service_name), json={'key1': 'key1', 'key2': 'key2'}))

    def test_patch(self):
        res = self.client.patch('/{}/patch/1'.format(self.service_name), json={'key1': 'key1', 'key2': 'key2'})
        print('res.json = ', res.json)
        self.assertEqual(res.json['patch'], '1')


if __name__ == '__main__':
    unittest.main()
