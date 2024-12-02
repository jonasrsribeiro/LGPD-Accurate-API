from app.models import Usuario, HistoricExclusion
from .database import get_db1, get_db2

def delete_users_based_on_historic():
    # Obtém os IDs dos usuários no histórico de exclusão
    with next(get_db2()) as db2:
        ids_to_exclude = db2.query(HistoricExclusion.usuario_id).all()

    # Converte para uma lista de IDs (removendo tuplas)
    ids_to_exclude = [user_id[0] for user_id in ids_to_exclude]

    # Exclui os usuários na tabela Usuario
    if ids_to_exclude:
        with next(get_db1()) as db1:
            db1.query(Usuario).filter(Usuario.id.in_(ids_to_exclude)).delete(synchronize_session=False)
            db1.commit()

    return ids_to_exclude
