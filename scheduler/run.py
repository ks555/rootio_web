import atexit
import logging
import argparse

from env import read_env
from broker import MessageBroker
from scheduler import MessageScheduler

from  multiprocessing import Process

def run():
    config = read_env('config.cfg')
    
    scheduler = MessageScheduler(config['jobstore'],config['url'])
    broker = MessageBroker(scheduler)
    
    # start scheduler in own thread
    scheduler.start()

    # shut scheduler threads cleanly at exit
    atexit.register(lambda: scheduler.shutdown())
    atexit.register(lambda: broker.shutdown())
    # start message broker ioloop
    try:
        print Process(target=broker.listener, args=('55666',)).start()
	print Process(target=broker.listener2, args=('55665',)).start()
    except KeyboardInterrupt:
        broker.shutdown()
    except Exception, e:
	logging.debug("exception in run():{}".format(e))
    try:
        while(1):
	       pass
    except:
        broker.shutdown()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RootIO Scheduled Message Broker')

    parser.add_argument('--log', action='store', help='log level', default='debug')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    
    logging.basicConfig(name='rootio_scheduler',level=numeric_level)

    try:
        run()
    finally:
        logging.shutdown()
