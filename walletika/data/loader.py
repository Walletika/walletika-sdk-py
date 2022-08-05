import aesdatabase


def loader(file_name: str, backup: bool = False) -> aesdatabase.DatabaseEngine:
    """
    :exception aesdatabase.error.TableCreationError
    :exception aesdatabase.error.SignatureNotFoundError
    :exception aescrypto.error.SignatureNotFoundError
    :exception aescrypto.error.WrongKeyError
    """

    # Memory setup
    drive = aesdatabase.DriveSetup(add_backup=backup)
    drive.database_update(file=file_name)

    if backup:
        drive.backup_update(file='Walletika')

    drive.create()

    # Default configuration and load
    db = aesdatabase.DatabaseEngine(drive=drive)
    db.load()

    return db
