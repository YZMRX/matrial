from math import e

from db import pysql

R = 8.31
B = 3
ACTIVATION_ENERGY = 8e-20
AVERAGE = 1e6
db = pysql()


def life_temperature_65mn(T):
    T += 273.15
    L = 10 * AVERAGE * e ** (-ACTIVATION_ENERGY * 1e23 / (R * T))
    return L


def life_humidity_65mn(H):
    L = AVERAGE * e ** (-H / 100 / 0.5)
    return L


def life_force_65mn(F, amp):
    if F == 0:
        F = 1
    N = (2 * F / (amp ** 2)) ** (-1 / B) * AVERAGE / 10
    return N


def rate(tn, hn, fn):
    """
    当前温度 当前湿度 当前应力 总体；
    rate 初值100%；
    损耗比:rate=rate-在当前条件下使用的次数/总的次数；
    将损耗比提前存入数据库在读取，无返回值
    """
    data = db.check()
    data_rate = db.look_rate()
    current_temperature = data['CurrentTemperature']
    current_humidity = data['CurrentHumidity']
    current_force = data['CurrentForce']
    id = data['id']
    t_rate, h_rate, f_rate = data_rate['t_rate'], data_rate['h_rate'], data_rate['f_rate']
    t_rate = t_rate - life_temperature_65mn(current_temperature) / tn
    h_rate = h_rate - life_humidity_65mn(current_humidity) / hn
    f_rate = f_rate - life_force_65mn(current_force) / fn
    params = (id, t_rate, h_rate, f_rate)
    db.update_rate(params)


def count_life_65Mn(id):
    sql = 'select * from data where id = %s'
    data = db.check(sql, id)
    data_rate = db.look_rate(id)
    print(data)
    print(data_rate)
    t_rate, h_rate, f_rate = data_rate['t_rate'], data_rate['h_rate'], data_rate['f_rate']
    current_temperature = data['CurrentTemperature']
    current_humidity = data['CurrentHumidity']
    current_force = data['CurrentForce']
    # 关于温度的计算

    mint = data['minTemperature']
    maxt = data['maxTemperature']
    dif_temperature = maxt - mint
    temperature, time_temperature = [], []
    temperature.append(current_temperature)
    time_temperature.append(round(life_temperature_65mn(current_temperature) * t_rate / 100))
    while maxt > mint:
        t = round(life_temperature_65mn(mint), 0)
        temperature.append(mint)
        time_temperature.append(t)
        mint += round(dif_temperature / 11)
    if mint > maxt:
        t = round(life_temperature_65mn(maxt), 0)
        temperature.append(maxt)
        time_temperature.append(t)
    # 关于湿度的计算

    minh = data['minHumidity']
    maxh = data['maxHumidity']
    humidity, time_humidity = [], []
    humidity.append(current_humidity)
    time_humidity.append(round(life_humidity_65mn(current_humidity) * h_rate / 100))
    dif_humidity = maxh - minh
    while maxh > minh:
        t = round(life_humidity_65mn(minh))
        humidity.append(minh)
        time_humidity.append(t)
        minh += round(dif_humidity / 11)
    if maxh < minh:
        t = round(life_humidity_65mn(maxh))
        humidity.append(maxh)
        time_humidity.append(t)

    # 关于应力的计算

    minf = data['minForce']
    maxf = data['maxForce']
    amplitude = data['amplitude']
    force, time_force = [], []
    force.append(current_force)
    time_force.append(round(life_force_65mn(current_force, amplitude) * f_rate / 100))
    dif_force = maxf - minf
    while maxf > minf:
        t = round(life_force_65mn(minf, amplitude))
        force.append(minf)
        time_force.append(t)
        minf += round(dif_force / 11)
    if maxf < minf:
        t = round(life_force_65mn(maxf, amplitude))
        force.append(maxf)
        time_force.append(t)
    # 求权重
    all_time = []
    for i in range(min(len(time_temperature),len(time_humidity),len(time_force))):
        all_time.append(round((time_temperature[i]*0.3+time_humidity[i]*0.3+time_force[i]*0.4)))
    # ---------------------------------------------

    return temperature, time_temperature, humidity, time_humidity, force, time_force, all_time, data


