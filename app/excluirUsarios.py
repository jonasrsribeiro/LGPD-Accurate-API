from .crud import get_historic_exclusion_all, get_user_all, delete_user_with_historic

def delete_users_based_on_historic():
    historic_records = get_historic_exclusion_all()
    ids_to_exclude = [record['usuario_id'] for record in historic_records]

    users = get_user_all()

    if ids_to_exclude:
        for user in users:
            if user['id'] in ids_to_exclude and user['ativo'] and user['nome'] and user['email'] and user['senha']:
                print(user)
                delete_user_with_historic(user['id'])

    return ids_to_exclude
