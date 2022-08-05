from . import loader


db = loader.loader(file_name='addressesbook')

if db.count_column() == 0:
    db.create_table(['username', 'interface'])

__all__ = ['db']
