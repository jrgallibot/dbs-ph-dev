from datetime import datetime
from time import sleep
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_mobile_friendly, schedule_google_index, every_fourth_day_checking_index, schedule_mobile_friendly_rank_checker, schedule_sitemap_lastmod_update, \
	empty_url_delete, GenerateArticleSchedule, SchedGenerateFirstSectionAndOtherSections, schedule_check_siteurl_update_page, GenerateAssistedGCSchedule

def start():
	print('x')
	"""scheduler = BackgroundScheduler()
	# scheduler.add_job(SchedGenerateFirstSectionAndOtherSections, 'interval', seconds=60)
	# scheduler.add_job(GenerateAssistedGCSchedule, 'interval', seconds=60)
	# scheduler.add_job(GenerateArticleSchedule, 'interval', seconds=60)
	# scheduler.add_job(schedule_check_siteurl_update_page, 'interval', seconds=60)
	scheduler.add_job(schedule_mobile_friendly, 'interval', hours=24)
	scheduler.add_job(schedule_sitemap_lastmod_update, 'interval', hours=12)
	scheduler.add_job(empty_url_delete, 'interval', hours=1)
	# scheduler.add_job(schedule_mobile_friendly_rank_checker, 'interval', hours=24)
	# scheduler.add_job(schedule_mobile_friendly, 'interval', minutes=2)
	scheduler.add_job(schedule_google_index, 'interval', hours=8)
	# scheduler.add_job(every_fourth_day_checking_index, 'interval', hours=24)
	scheduler.start()"""