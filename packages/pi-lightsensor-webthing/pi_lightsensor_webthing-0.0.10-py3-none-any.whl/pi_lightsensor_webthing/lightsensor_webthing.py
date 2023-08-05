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

        self.ioloop = tornado.ioloop.IOLoop.current()

        logging.info('bind to port ' + str(gpio_number))
        self.gpio_number = gpio_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)
        self.bright.notify_of_external_update(self.read_gpio())
        GPIO.add_event_detect(self.gpio_number, GPIO.BOTH, callback=self.update, bouncetime=5)


    def update(self, channel):
        if GPIO.input(self.gpio_number):
            logging.info("motion detected")
            self.ioloop.add_callback(self.update_bright_prop, True)
        else:
            self.ioloop.add_callback(self.update_bright_prop, False)

    def update_bright_prop(self, is_bright):
        if is_bright:
            self.bright.notify_of_external_update(True)
        else:
            self.bright.notify_of_external_update(False)

    def read_gpio(self):
        if GPIO.input(self.gpio_number):
            logging.info("state updated: False")
            return False
        else:
            logging.info("state updated: True")
            return True


def run_server(port, gpio_number, description):
    light_sensor = LightSensor(gpio_number, description)
    server = WebThingServer(SingleThing(light_sensor), port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
