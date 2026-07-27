import asyncio
from collections import defaultdict

from pier.job import Job
from pier.models.job.config import JobConfig, RetryConfig
from pier.models.job.lock import JobLock
from pier.models.metric.mean import Mean
from pier.models.trial.config import TaskConfig


def test_job_config_equality_ignores_resume_concurrency():
    saved_config = JobConfig(n_concurrent_trials=4)
    resumed_config = JobConfig(n_concurrent_trials=2)

    assert saved_config == resumed_config


def test_job_lock_equality_ignores_resume_concurrency():
    saved_lock = JobLock(n_concurrent_trials=4, retry=RetryConfig())
    resumed_lock = JobLock(n_concurrent_trials=2, retry=RetryConfig())

    assert saved_lock == resumed_lock


def test_resume_cleanup_preserves_critiques_metadata_dir(tmp_path):
    config = JobConfig(job_name="job", jobs_dir=tmp_path)
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    (job_dir / "config.json").write_text(config.model_dump_json(), encoding="utf-8")

    critiques_dir = job_dir / ".critiques" / "olympus-qa-v3"
    critiques_dir.mkdir(parents=True)
    (critiques_dir / "result.json").write_text("{}", encoding="utf-8")

    incomplete_trial_dir = job_dir / "task__abc123"
    incomplete_trial_dir.mkdir()
    (incomplete_trial_dir / "config.json").write_text("{}", encoding="utf-8")

    job = Job(config, _task_configs=[], _metrics=defaultdict(list))
    job._close_logger_handlers()

    assert (job_dir / ".critiques").is_dir()
    assert critiques_dir.is_dir()
    assert not incomplete_trial_dir.exists()


def test_explicit_dataset_task_source_gets_default_metric(tmp_path):
    task_config = TaskConfig(path=tmp_path, source="swe-bench-verified")

    metrics = asyncio.run(Job._resolve_metrics(JobConfig(), [task_config]))

    assert len(metrics["swe-bench-verified"]) == 1
    assert isinstance(metrics["swe-bench-verified"][0], Mean)

