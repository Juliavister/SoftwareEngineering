from sklearn.linear_model import LinearRegression
import numpy as np
import data


def send_currency_predict(cr):
    currency = cr
    dates = []
    rates = []
    for i in range(len(data.data[currency]['dates'])):
        date = data.data[currency]['dates'][i]
        date_numeric = date.toordinal()
        dates.append([date_numeric])
        rates.append(data.data[currency]['rates'][i])
    model = LinearRegression()
    model.fit(dates, rates)

    predictions = model.predict(dates)

    return np.mean(predictions)
