from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import RPi.GPIO as GPIO
import tornado.ioloop


class LightSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number, description):
        Thing.__init__(
            self,
            'urn:dev:ops:illuminanceSensor-1',
            'IlluminanceSensor',
            ['OnOffSwitch'],
            description
        )

        self.gpio_number = gpio_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)

        self.bright = Value(False)
        self.add_property(
            Property(self,
                     'bright',
                     self.bright,
                     metadata={
                         '@type': 'OnOffProperty',
                         'title': 'bright',
                         "type": "boolean",
                         'description': 'Whether the lamp is bright',
                         'readOnly': True,
                     }))

        self.timer = tornado.ioloop.PeriodicCallback(self.__measure, (60 * 1000))  # 1 min
        self.timer.start()

    def __measure(self):
        try:
            if GPIO.input(self.gpio_number):
                self.bright.notify_of_external_update(True)
                logging.info("bright=True")
            else:
                self.bright.notify_of_external_update(False)
                logging.info("bright=False")
        except Exception as e:
            logging.error(e)

    def cancel_measure_task(self):
        self.timer.stop()


def run_server(port, gpio_number, description):
    light_sensor = LightSensor(gpio_number, description)
    server = WebThingServer(SingleThing(light_sensor), port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        light_sensor.timer.stop()
        server.stop()
        logging.info('done')
