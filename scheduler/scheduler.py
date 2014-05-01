from apscheduler.scheduler import Scheduler
import logging

class MessageScheduler(object):
    def __init__(self, jobstore, url):
        self._scheduler = Scheduler(daemonic=True)

        config = {'apscheduler.jobstores.file.class': 'apscheduler.jobstores%s' % jobstore,
                   'apscheduler.jobstores.file.url':  url}      
        self._scheduler.configure(config)

    def start(self):
        logging.info("scheduler start")
        self._scheduler.start()

    def shutdown(self):
        logging.info("scheduler shutdown")
        self._scheduler.shutdown()

    def schedule_message(self, topic, message, send_at):
        logging.info("schedule message %s:%s at %s" % (topic, message, send_at))

        #create lambda for scheduler to call at execution time

        #and add it
        try:
            job = self._scheduler.add_date_job(self._broker.forward, send_at, args=(topic, message))
            logging.debug("scheduled job_id", job.id)
        except ValueError,e:
            logging.error(e)

    def cancel_message(self, message_id):
        logging.info("cancel message_id %s" % message_id)
        # apscheduler.unschedule_job works by comparing apscheduler.job objects
        # we don't have a whole job, just the id, message_id == job.id
        # so do it manually

        self._scheduler._jobstores_lock.acquire()
        try:
            for alias, jobstore in self._scheduler._jobstores.iteritems():
                for job in list(jobstore.jobs):
                    if job.id == message_id:
                        self._remove_job(job, alias, jobstore)
                    return
        finally:
            self._scheduler._jobstores_lock.release()

        raise KeyError('Message id "%s" is not scheduled in any job store' % message_id)

    def reschedule_message(self, message_id, topic, message, send_at):
        logging.info("reschedule message_id %s" % message_id)
        self.cancel_message(message_id)
        self.schedule_message(topic, message, send_at)
