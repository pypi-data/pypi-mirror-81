import typing

import httplib2  # type: ignore
import typing_extensions

import googleapiclient.discovery
import googleapiclient.http  # type: ignore

from .schemas import *

class YouTubeAnalyticsResource(googleapiclient.discovery.Resource): ...
