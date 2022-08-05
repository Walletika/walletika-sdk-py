from . import loader


db = loader.loader(file_name='stakecontracts')

if db.count_column() == 0:
    db.create_table(['rpc', 'interface'])

__all__ = ['db']
