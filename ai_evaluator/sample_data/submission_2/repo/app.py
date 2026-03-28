def predict(transaction):
    if transaction > 10000:
        return "fraud"
    return "not fraud"

print(predict(12000))