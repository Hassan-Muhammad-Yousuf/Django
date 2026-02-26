from rest_framework import status
import pytest
from store.models import Product, Collection, OrderItem, Customer
from model_bakery import baker
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_return_401(self, create_product):
        response = create_product({'title': 'a', 'slug': 'a', 'unit_price': 1})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, create_product):
        authenticate(is_staff=False)
        response = create_product({'title': 'a', 'slug': 'a', 'unit_price': 1})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product({'title': '', 'slug': 'a', 'unit_price': 1}) # Invalid title
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = create_product({'title': 'a', 'slug': 'a', 'unit_price': 1, 'inventory': 10, 'collection': collection.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_return_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title

    def test_if_product_does_not_exist_return_404(self, api_client):
        response = api_client.get('/store/products/9999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_return_401(self, api_client):
        product = baker.make(Product)
        response = api_client.put(f'/store/products/{product.id}/', {'title': 'updated'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        product = baker.make(Product)
        response = api_client.put(f'/store/products/{product.id}/', {'title': 'updated'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)
        response = api_client.put(f'/store/products/{product.id}/', {'title': ''}) # Invalid title
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)
        # Provide all required fields for a PUT request
        response = api_client.put(f'/store/products/{product.id}/', {
            'title': 'updated title',
            'slug': 'updated-title',
            'unit_price': 10.00,
            'inventory': 5,
            'collection': product.collection.id # Use existing collection ID
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'updated title'


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_return_401(self, api_client):
        product = baker.make(Product)
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        product = baker.make(Product)
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_has_order_items_return_400(self, authenticate, api_client):
        authenticate(is_staff=True)

        product = baker.make(Product)
        user = baker.make('core.User')
        customer, _ = Customer.objects.get_or_create(user=user)
        order = baker.make('store.Order', customer=customer)
        baker.make(OrderItem, product=product, order=order)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

    def test_if_product_has_no_order_items_return_204(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.filter(id=product.id).exists() == False