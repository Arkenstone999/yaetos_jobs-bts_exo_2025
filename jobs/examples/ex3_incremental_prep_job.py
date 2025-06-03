from yaetos.etl_utils import ETL_Base, Commandliner
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.sql.functions import col


class Job(ETL_Base):
    def transform(self, some_events):

        udf_format_datetime = udf(self.format_datetime, StringType())

        events_cleaned = some_events \
            .withColumn('timestamp_obj', udf_format_datetime(some_events.timestamp).cast("timestamp")) \
            .where(col('timestamp').like("%2.016%") is False)
        return events_cleaned

    @staticmethod
    def format_datetime(wiki_dt):
        dt = {}
        dt['year'] = wiki_dt[:4]
        dt['month'] = wiki_dt[4:6]
        dt['day'] = wiki_dt[6:8]
        dt['hour'] = wiki_dt[8:10]
        dt['minute'] = wiki_dt[10:12]
        dt['sec'] = wiki_dt[12:14]
        return '{year}-{month}-{day} {hour}:{minute}:{sec}'.format(**dt)


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
