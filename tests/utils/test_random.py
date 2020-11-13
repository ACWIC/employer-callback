from app.utils.random import Random


def test_random():
    """
    call the random method some number of times
    and ensure no two results the same are ever returned
    hash each random string and ensure the hash is different from the string
    and that no two hashes are the same.
    """
    random_string1 = Random.get_uuid()
    random_string2 = Random.get_uuid()

    hash1 = Random.get_str_hash(random_string1)
    hash2 = Random.get_str_hash(random_string2)

    assert random_string1 != random_string2
    assert hash1 != random_string1
    assert hash2 != random_string2
    assert hash1 != hash2
