from . import loader


db = loader.loader(file_name='tokens')

if db.count_column() == 0:
    db.create_table(['rpc', 'address', 'interface'])

__all__ = ['db']
