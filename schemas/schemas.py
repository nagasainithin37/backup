def individual_serial(data)->dict:
    return {
        **{i:str(data[i]) for i in data if i=="_id"},
        **{i:data[i] for i in data if i!="_id"}

    }    

def list_serial(dataList)->list:
    return [individual_serial(data) for data in dataList]