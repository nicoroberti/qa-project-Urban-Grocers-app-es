import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(kit_body):
    user_body = get_user_body(kit_body)
    user_response = sender_stand_request.post_new_client_kits(kit_body)

    assert user_response.status_code == 201
    assert user_response.json()['name'] == kit_body['name']
    assert user_response.json()['name'] == 'El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud'
    print(user_response.json())

    #comprobar si hay un registro de creación de un nuevo usuario guardado en la tabla users
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

def test_create_user_1_character_in_first_name_get_success_response():
    positive_assert(data.kit_body1)

def test_create_user_511_characters_allowed_in_first_name_get_success_response():
    positive_assert(data.kit_body2)

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

def test_create_user_no_first_name_get_error_response():
    negative_assert_no_first_name(data.kit_body3)

def test_create_user_512_characters_in_first_name_get_error_response():
    negative_assert_symbol(data.kit_body4)

def test_create_user_has_special_symbol_in_first_name_get_success_response():
    positive_assert(data.kit_body5)

def test_create_user_has_space_in_first_name_get_success_response():
    positive_assert(data.kit_body6)

def test_create_user_has_number_in_first_name_get_success_response():
    positive_assert(data.kit_body7)

def test_create_user_empty_first_name_get_error_response():
    negative_assert_symbol(data.kit_body8)

def test_create_user_number_type_first_name_get_error_response():
    negative_assert_symbol(data.kit_body9)




