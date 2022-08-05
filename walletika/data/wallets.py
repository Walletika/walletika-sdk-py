from . import loader


db = loader.loader(file_name='wallets', backup=True)

if db.count_column() == 0:
    db.create_table(['username', 'interface'])

__all__ = ['db']
