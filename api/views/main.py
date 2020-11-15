from datetime import datetime
from flask import Blueprint, request
from api.models import db, Sensor, Reading
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import os

main = Blueprint("main", __name__)  # initialize blueprint

@main.before_request
def check_key():
    if request.headers.get('ApiKey') is None:
        msg = "Bad auth."
        logger.info(msg)
        return create_response(status=401, message=msg)
    
    token = request.headers['ApiKey']
    if token != os.getenv("APIKEY"):
        msg = "Bad auth."
        logger.info(msg)
        return create_response(status=401, message=msg)


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    # access the logger with the logger from api.core and uses the standard logging module
    # try using ipdb here :) you can inject yourself
    logger.info("Hello World!")
    return "<h1>Hello World!</h1>"


# function that is called when you visit /sensors
@main.route("/sensors", methods=["GET"])
def get_sensors():
    sensors = Sensor.query.all()
    return create_response(data={"sensors": serialize_list(sensors)})


# POST request for /sensors
@main.route("/sensors", methods=["POST"])
def create_sensor():
    data = request.form
    logger.info(str(data.keys()))
    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "location" not in data:
        msg = "No location provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)

    # create SQLAlchemy Objects
    new_sensor = Sensor(name=data["name"], location=data["location"])

    # commit it to database
    db.session.add_all([new_sensor])
    db.session.commit()
    return create_response(
        message=f"Successfully created sensor {new_sensor.name} with id: {new_sensor.id}",
        data={"id":new_sensor._id, "name": new_sensor.name, "location": new_sensor.location}
    )

@main.route("/readings", methods=["GET"])
def get_readings():
    data = request.form

    from_time_str = data.get("from","2020-01-01 00:00:00")
    from_time = datetime.strptime(from_time_str, '%Y-%m-%d %H:%M:%S')

    if data.get("to") is None:
        to_time = datetime.now()
    else:
        to_time_str = data.get("to")
        to_time = datetime.strptime(to_time_str, '%Y-%m-%d %H:%M:%S')

    readings = Reading.query.filter(Reading.timestamp <= to_time).filter(Reading.timestamp >= from_time)
    return create_response(data={"readings": serialize_list(readings)})


@main.route("/readings", methods=["POST"])
def create_reading():
    data = request.form

    if "temperature" not in data:
        msg = "No temperature provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "pressure" not in data:
        msg = "No pressure provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "humidity" not in data:
        msg = "No pressure provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "sensor_id" not in data:
        msg = "No sensor_id provided for sensor."
        logger.info(msg)
        return create_response(status=422, message=msg)
    
    #check if sensor is in sensor table
    sensor = Sensor.query.filter(Sensor.id == data["sensor_id"])
    if len(sensor) == 0:
        msg = "Sensor with sensor_id: {sensor_id} not found.".format(**data)
        logger.info(msg)
        return create_response(status=422, message=msg)

    new_reading = Reading(sensor_id=data["sensor_id"], 
                        temperature=data["temperature"],
                        pressure=data["pressure"],
                        humidity=data["humidity"],
                        )

    db.session.add_all([new_reading])
    db.session.commit()
    return create_response(
        message=f"Successfully created reading",
        data={"sensor_id":new_reading.sensor_id, "temperature": new_reading.temperature, "pressure": new_reading.pressure, "humidity": new_reading.humidity}
    )