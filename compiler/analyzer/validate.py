errors = {
    "quantity_primitive": "CANNOT ADD A QUANTITY OF A PRIMITIVE",
    "": ""
}

def validate_add(params):
    #Adding a primitive
    if len(params) == 3:
        pass
    else:
        primitive = params[1]

    # return error
    return None

def validate_remove():
    pass


validate_map = {
    "ADD" : validate_add
}
