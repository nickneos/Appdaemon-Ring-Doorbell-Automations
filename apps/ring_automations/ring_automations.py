"""
Automations for Ring Doorbell 
Supported features:
    * Play alert sound on media device (eg. google home)
    * Courtesy light
    * Flash lights
    * Google Home voice prompt (TTS)
"""

import appdaemon.plugins.hass.hassapi as hass
import time

# default values
DEFAULT_MEDIA_CONTENT = "https://www.myinstants.com/media/sounds/dj-airhorn-sound-effect-kingbeatz_1.mp3"
DEFAULT_COURTESY_LIGHT_TIMER = 60
DEFUALT_DOORBELL_VOLUME = 10
DEFAULT_TTS = "There's someone at the door"

class Doorbell(hass.Hass):

    def initialize(self):
        """Initialize AppDaemon App."""
        self.button = self.args.get("button")
        self.motion = self.args.get("motion")
        self.media_player = self.args.get("media_player")
        self.media_content = self.args.get("media_content", DEFAULT_MEDIA_CONTENT)
        self.flash = self.args.get("flash")
        self.courtesy_light = self.args.get("courtesy_light")
        self.tts_device = self.args.get("tts_device")
        self.tts = self.args.get("tts", DEFAULT_TTS)

        # listener for when ring doorbell is pressed
        self.listen_state(self.cb_doorbell, self.button, new = "on")

         # listener for when ring doorbell detects motion
        self.listen_state(self.cb_motion, self.motion, new = "on")
                

    def cb_doorbell(self, entity, attribute, old, new, kwargs):
        """Callback function when doorbell button is pressed"""

        self.log(f"Ring Doorbell {self.button} pressed") 

        # Turn on courtesy light if enabled and after sunset
        if self.courtesy_light and self.sun_down():
            light = self.courtesy_light.get("entity_id")
            timer = self.courtesy_light.get("timer", DEFAULT_COURTESY_LIGHT_TIMER)

            self.turn_on(light)
            self.run_in(
                self.cb_delayed_service, 
                timer, 
                entity_id = light,
                service = "light.turn_off"    
            )

        # Play alert if someone is home
        if self.anyone_home(person=True) and self.media_player:
            if self.volume_slider:
                vol = float(self.get_state(self.volume_slider))
            else:
                vol = self.volume

            if vol > 0:
                self.call_service("xiaomi_aqara/play_ringtone", 
                                media_player = self.media_player,
                                media_content = self.media_content,
                                ringtone_vol = vol)
        
        # Flash lights if enabled
        if self.flash:
            if type(self.flash) is list:
                lights = self.flash
            else:
                lights = [self.flash]

            self.flash_lights(lights)
               

        # Google Home voice prompt if enabled
        if self.tts_device and self.anyone_home(person=True):
            if type(self.tts_device) is list:
                ggl_homes = self.tts_device
            else:
                ggl_homes = [self.tts_device]

            for gh in ggl_homes:
                if self.get_state(gh) == "off": 
                    self.call_service("tts/google_say", entity_id = gh,
                                      message = self.tts)
                                      

    def cb_motion(self, entity, attribute, old, new, kwargs):
        """ Callback function when doorbell motion is detected"""
        return
        # placeholder


    def cb_delayed_service(self, kwargs):
        """Callback function to use with self.run_in() to call a service on a device"""
        entity = kwargs.get("entity_id")
        service = kwargs.get("service")
        
        if service:
            service = service.replace(".", "/")
        
        try:
            self.call_service(service, entity_id = entity)
        except AttributeError:
            pass

    def flash_lights(self, lights):
        """Flash the light specified"""
        
        rng = range(6) # number of times to loop later

        for light in lights:
            state = self.get_state(light)
            
            for x in rng:
                self.log(x)
                self.run_in(self.cb_delayed_service, x, entity_id = light, service = "light.toggle")

            if state == "on":
                self.run_in(self.cb_delayed_service, len(rng), entity_id = light, service = "light.turn_on")
            elif state == "off":
                self.run_in(self.cb_delayed_service, len(rng), entity_id = light, service = "light.turn_off")
            