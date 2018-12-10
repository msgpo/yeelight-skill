#!/usr/bin/env python
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util.log import LOG
from yeelight import Bulb
from yeelight.transitions import *
from time import sleep
from colour import Color
import math
import re
import random


__author__ = 'PCWii'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# List each of the bulbs here
seq_delay = 0.5
effect_delay = 3500

bulbRHS = Bulb("192.168.0.50")
bulbLHS = Bulb("192.168.0.51")
Valid_Color = ['red', 'read', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'purple', 'white']

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class YeeLightSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(YeeLightSkill, self).__init__(name="YeeLightSkill")
        self.error_code = 0

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        yee_light_on_intent = IntentBuilder("YeeLightOnIntent").\
            require("DeviceKeyword").require("OnKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(yee_light_on_intent, self.handle_yee_light_on_intent)

        yee_light_off_intent = IntentBuilder("YeeLightOffIntent").\
            require("DeviceKeyword").require("OffKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(yee_light_off_intent, self.handle_yee_light_off_intent)

        yee_light_dim_intent = IntentBuilder("YeeLightDimIntent").\
            require("DimKeyword").require("DeviceKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(yee_light_dim_intent, self.handle_yee_light_dim_intent)

        yee_light_set_intent = IntentBuilder("YeeLightSetIntent").\
            require("SetKeyword").require("DeviceKeyword").\
            optionally("LightKeyword"). \
            optionally("SilentKeyword").optionally("TransitionKeyword").build()
        self.register_intent(yee_light_set_intent, self.handle_yee_light_set_intent)

    def load_transition(self, transition):
        bulbLHS.t
        # LOG.info("transition: " & transition)
        if transition == "alarm":
            bulbLHS.start_flow(alarm(duration=250))
            bulbRHS.start_flow(alarm(duration=250))
        if transition == "christmas":
            bulbLHS.start_flow(christmas(duration=250, brightness=100, sleep=3000))
            bulbRHS.start_flow(christmas(duration=250, brightness=100, sleep=3000))
        if transition == "disco":
            bulbLHS.transitions.disco(bpm=120)
            bulbRHS.transitions.disco(bpm=120)
        if transition == "lsd":
            bulbLHS.transitions.lsd(duration=3000, brightness=100)
            bulbRHS.transitions.lsd(duration=3000, brightness=100)
        if transition == "police":
            bulbLHS.transitions.police(duration=300, brightness=100)
            bulbRHS.transitions.police(duration=300, brightness=100)
        if transition == "pulse":
            bulbLHS.transitions.pulse(0, 255, 0, duration=250, brightness=100)
            bulbRHS.transitions.pulse(0, 255, 0, duration=250, brightness=100)
        if transition == "random":
            bulbLHS.transitions.randomloop(duration=750, brightness=100, count=9)
            bulbRHS.transitions.randomloop(duration=750, brightness=100, count=9)
        if transition == "strobe":
            if random.random() < 0.7:
                bulbLHS.transitions.strobe_color(brightness=100)
                bulbRHS.transitions.strobe_color(brightness=100)
            else:
                bulbLHS.transitions.strobe()
                bulbRHS.transitions.strobe()

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_yee_light_on_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        self.error_code = 0
        try:
            bulbRHS.turn_on()
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "right hand side,"})
        sleep(seq_delay)
        try:
            bulbLHS.turn_on()
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "left hand side,"})
        if self.error_code == 0:
            if not silent_kw:
                self.speak_dialog("light.on")

    def handle_yee_light_off_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        self.error_code = 0
        try:
            bulbRHS.turn_off(duration=effect_delay)
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "right hand side,"})
        sleep(seq_delay)
        try:
            bulbLHS.turn_off(duration=effect_delay)
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "left hand side,"})
        if self.error_code == 0:
            if not silent_kw:
                self.speak_dialog("light.off")

    def handle_yee_light_dim_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        self.error_code = 0
        try:
            bulbRHS.set_brightness(5, duration=effect_delay)
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "right hand side,"})
        sleep(seq_delay)
        try:
            bulbLHS.set_brightness(5, duration=effect_delay)
        except Exception as e:
            self.error_code += 1
            LOG.error(e)
            if not silent_kw:
                self.speak_dialog("error", data={"result": "left hand side,"})
        if self.error_code == 0:
            if not silent_kw:
                self.speak_dialog("light.dim")

    def handle_yee_light_set_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        transition_kw = str(message.data.get("TransitionKeyword"))
        self.error_code = 0
        str_remainder = str(message.utterance_remainder())
        for findcolor in Valid_Color:
            mypos = str_remainder.find(findcolor)
            if mypos > 0:
                if findcolor == 'read':
                    findcolor = 'red'
                myRed = math.trunc(Color(findcolor).get_red() * 255)
                myGreen = math.trunc(Color(findcolor).get_green() * 255)
                myBlue = math.trunc(Color(findcolor).get_blue() * 255)
                try:
                    bulbLHS.set_rgb(myRed, myGreen, myBlue)
                except Exception as e:
                    self.error_code += 1
                    LOG.error(e)
                    if not silent_kw:
                        self.speak_dialog("error", data={"result": "left hand side,"})
                sleep(seq_delay)
                try:
                    bulbRHS.set_rgb(myRed, myGreen, myBlue)
                except Exception as e:
                    self.error_code += 1
                    LOG.error(e)
                    if not silent_kw:
                        self.speak_dialog("error", data={"result": "right hand side,"})
                if self.error_code == 0:
                    if not silent_kw:
                        self.speak_dialog("light.set", data ={"result": findcolor})
                break
        dim_level = re.findall('\d+', str_remainder)
        if dim_level:
            self.error_code = 0
            try:
                bulbLHS.set_brightness(int(dim_level[0]), duration=effect_delay)
            except Exception as e:
                self.error_code += 1
                LOG.error(e)
                if not silent_kw:
                    self.speak_dialog("error", data={"result": "left hand side,"})
            sleep(seq_delay)
            try:
                bulbRHS.set_brightness(int(dim_level[0]), duration=effect_delay)
            except Exception as e:
                self.error_code += 1
                LOG.error(e)
                if not silent_kw:
                    self.speak_dialog("error", data={"result": "right hand side,"})
            if self.error_code == 0:
                if not silent_kw:
                    self.speak_dialog("light.set", data={"result": str(dim_level[0]) + ", percent"})
        if transition_kw:
            LOG.info(transition_kw)
            bulb_transition = str(transition_kw.split(' ', 1)[0])
            LOG.info(bulb_transition)
            self.load_transition(bulb_transition)


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return YeeLightSkill()
