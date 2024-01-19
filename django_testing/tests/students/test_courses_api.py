from random import randint

import pytest
from django.urls import reverse

from students.models import Course
from tests.conftest import api_client, student_factory, course_factory
from students.filters import CourseFilter

@pytest.mark.django_db
def test_one_course(api_client, course_factory):
    course = course_factory(_quantity=1)
    url = reverse('courses-list')
    response = api_client.get(url)
    data = response.json()
    assert data[0]['name'] == course[0].name
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_list(api_client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = api_client.get(url)
    data = response.json()
    for id, content in enumerate(data):
        assert content['name'] == courses[id].name
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_creation(api_client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = api_client.post(url, data={'name': 'test course'})
    assert Course.objects.count() == count + 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_course_update(api_client, course_factory):
    course_amount = 20
    courses = course_factory(_quantity=course_amount)
    random_num = randint(1, course_amount)
    course_id = courses[random_num - 1].id
    url = reverse('courses-detail', kwargs={'pk': course_id})
    response = api_client.patch(url, data={'name': 'patched name'})
    data = response.json()
    filtered_course = Course.objects.filter(id=course_id)
    assert data['name'] == filtered_course.get().name
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_delete(api_client, course_factory):
    course_amount = 20
    courses = course_factory(_quantity=course_amount)
    random_num = randint(1, course_amount)
    course_id = courses[random_num - 1].id
    url = reverse('courses-detail', kwargs={'pk': course_id})
    response = api_client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_course_id_filtration(api_client, course_factory):
    course_amount = 100
    courses = course_factory(_quantity=course_amount)
    random_num = randint(1, course_amount)
    course_id = courses[random_num - 1].id
    qs = Course.objects.all()
    filter = CourseFilter()
    result_course = filter.custom_filter(qs, 'id', course_id)
    assert result_course.get().id == course_id


@pytest.mark.django_db
def test_course_name_filtration(api_client, course_factory):
    course_amount = 100
    courses = course_factory(_quantity=course_amount)
    random_num = randint(1, course_amount)
    course_name = courses[course_amount - 1].name
    qs = Course.objects.all()
    filter = CourseFilter()
    result_course = filter.custom_filter(qs, 'name', course_name)
    assert result_course.get().name == course_name

