from logging import getLogger
from typing import List, Optional

from conda.api import SubdirData
from conda.misc import explicit
from conda import CondaError
from conda.models.match_spec import MatchSpec

from .env.env import Environment


log = getLogger(__name__)


def find_package_url(
        match_spec: MatchSpec,
        channels: Optional[List[str]]=None,
        subdirs: Optional[List[str]]=None,
    ):
    match = SubdirData.query_all(
        match_spec,
        channels=channels,
        subdirs=subdirs
    )
    if len(match) != 1:
        raise CondaError(f"Bad match for {match_spec}: found {len(match)} package(s) that match")
    return match[0].url


def no_solve_install(env: Environment, prefix: str):
    matchspecs = [MatchSpec(d) for d in env.dependencies['conda']]
    log.info("Finding packages that match environment specification...")
    urls = [find_package_url(ms) for ms in matchspecs]
    log.info("Packages found that match specs:")
    for url in urls:
        log.info(url)
    explicit(urls, prefix)
    return
