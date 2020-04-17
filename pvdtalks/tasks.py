import logging
import time

from celery import Celery

from .models import Answer, db


logger = logging.getLogger(__name__)

celery = Celery(__name__)

@celery.task
def long_add(x: int, y: int) -> int:
  time.sleep(5)
  logger.info(f'Hello {x + y}')
  answer = x + y
  db.session.add(Answer(answer=answer))
  db.session.commit()
  return answer
