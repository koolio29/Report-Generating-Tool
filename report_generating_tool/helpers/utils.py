from chardet.universaldetector import UniversalDetector

def get_file_encoding(csv_file):
    """
    Gets the type of file encoding

    Parameters
    ----------
    csv_file : str
        Name of the csv file

    Returns
    --------
    str
        Type of the encoding
    """
    encoding_detector = UniversalDetector()

    try:
        with open(csv_file, "rb") as file:
            for line in file.readlines():
                encoding_detector.feed(line)
                if encoding_detector.done:
                    break
    except Exception as e:
        print("Exception occured when reading the csv file.")
        print("Error: ", e)
        exit(1)
    else:
        encoding_detector.close()
    
    return encoding_detector.result["encoding"]

def get_max_value_from_dict(mydict):
    """
    Gets the maximum key value from a dictionary

    Parameters
    ----------
    mydict : dict
        Dictionary to where the maximum key value is to be found

    Returns
    -------
    Dictionary key value
        The maximum dictionary key value
    """
    return mydict[max(mydict, key=mydict.get)]

def to_two_decimals(value):
    """
    Rounds of a floating number to 2 decimal points

    Parameters
    ----------
    value : float
        Floating number to be rounded off

    Returns
    -------
    float
        A floating number with 2 decimal points
    """
    # FIXME:
    # Not a very good idea to use floats here... since it does not all numbers 
    # are represented exactly... however leaving like this for now since a
    # changing it to decimal.Decimal breaks over half of the unit tests. Even 
    # left as it is, it does not cause a huge problem to the tool itself
    # https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
    return round(float(value), 2) 
