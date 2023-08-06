import argparse
import threading
import time
import queue
from pyfiglet import Figlet
from beacontools import BeaconScanner
from .models import TiltStatus
from .providers import *
from .configuration import PitchConfig
from .rate_limiter import RateLimitedException

#############################################
# Statics
#############################################
uuid_to_colors = {
        "a495bb20-c5b1-4b44-b512-1370f02d74de": "green",
        "a495bb30-c5b1-4b44-b512-1370f02d74de": "black",
        "a495bb10-c5b1-4b44-b512-1370f02d74de": "red",
        "a495bb60-c5b1-4b44-b512-1370f02d74de": "blue",
        "a495bb50-c5b1-4b44-b512-1370f02d74de": "orange",
        "a495bb70-c5b1-4b44-b512-1370f02d74de": "pink",
        "a495bb40-c5b1-4b44-b512-1370f02d74de": "purple",
        "a495bb40-c5b1-4b44-b512-1370f02d74df": "simulated"  # reserved for fake beacons during simulation mode
    }

colors_to_uuid = dict((v, k) for k, v in uuid_to_colors.items())

# Load config
parser = argparse.ArgumentParser(description='')
parser.add_argument('--simulate-beacons', dest='simulate_beacons', action='store_true',
                    help='Creates simulated beacon signals for testing')

args = parser.parse_args()
# Load config from file, with defaults, and args
config = PitchConfig.load(vars(args))

all_providers = [
        PrometheusCloudProvider(config),
        FileCloudProvider(config),
        InfluxDbCloudProvider(config),
        BrewfatherCustomStreamCloudProvider(config),
        BrewersFriendCustomStreamCloudProvider(config)
    ]

enabled_providers = list()

# Queue for holding incoming scans
pitch_q = queue.Queue(maxsize=config.queue_size)

#############################################
#############################################


def pitch_main():
    start_message()
    # add any webhooks defined in config
    add_webhook_providers(config)
    # Start cloud providers
    print("Starting...")
    for provider in all_providers:
        if provider.enabled():
            enabled_providers.append(provider)
            provider_start_message = provider.start()
            if not provider_start_message:
                provider_start_message = ''
            print("...started: {} {}".format(provider, provider_start_message))

    if config.simulate_beacons:
        threading.Thread(name='background', target=simulate_beacons).start()
    else:
        scanner = BeaconScanner(beacon_callback)
        scanner.start()
        print("...started: Tilt scanner")

    print("Ready!  Listening for beacons")
    while True:
        handle_pitch_queue()


def simulate_beacons():
    """Simulates Beacon scanning with fake events. Useful when testing or developing
    without a beacon, or on a platform with no Bluetooth support"""
    print("...started: Tilt Beacon Simulator")
    # Using Namespace to trick a dict into a 'class'
    fake_packet = argparse.Namespace(**{
        'uuid': colors_to_uuid['simulated'],
        'major': 70,
        'minor': 1035
    })
    while True:
        beacon_callback(None, None, fake_packet, dict())
        time.sleep(0.25)


def beacon_callback(bt_addr, rssi, packet, additional_info):
    uuid = packet.uuid
    color = uuid_to_colors.get(uuid)
    if color:
        # iBeacon packets have major/minor attributes with data
        # major = degrees in F (int)
        # minor = gravity (int) - needs to be converted to float (e.g. 1035 -> 1.035)
        tilt_status = TiltStatus(color, packet.major, get_decimal_gravity(packet.minor), config)
        pitch_q.put(tilt_status)


def handle_pitch_queue():
    if pitch_q.empty():
        return

    if pitch_q.full():
        length = pitch_q.qsize()
        print("Queue is full ({} events), scans will be ignored until the queue is reduced".format(length))

    tilt_status = pitch_q.get()
    for provider in enabled_providers:
        try:
            start = time.time()
            provider.update(tilt_status)
            time_spent = time.time() - start
            print("Updated provider {} for color {} took {:.3f} seconds".format(provider, tilt_status.color, time_spent))
        except RateLimitedException:
            # nothing to worry about, just called this too many times (locally)
            print("Skipping update due to rate limiting for provider {} for color {}".format(provider, tilt_status.color))
        except Exception as e:
            # todo: better logging of errors
            print(e)
    # Log it to console/stdout
    print(tilt_status.json())


def get_decimal_gravity(gravity):
    # gravity will be an int like 1035
    # turn into decimal, like 1.035
    return gravity * .001


def add_webhook_providers(config: PitchConfig):
    # Multiple webhooks can be fired, so create them dynamically and add to
    # all providers static list
    for url in config.webhook_urls:
        all_providers.append(WebhookCloudProvider(url, config))


def start_message():
    f = Figlet(font='slant')
    print(f.renderText('Pitch'))
