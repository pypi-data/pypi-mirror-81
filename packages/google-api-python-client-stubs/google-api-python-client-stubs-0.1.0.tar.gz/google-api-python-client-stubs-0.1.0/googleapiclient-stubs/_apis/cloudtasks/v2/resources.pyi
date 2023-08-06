import typing

import httplib2  # type: ignore
import typing_extensions

import googleapiclient.discovery
import googleapiclient.http  # type: ignore

from .schemas import *

class CloudTasksResource(googleapiclient.discovery.Resource):
    class ProjectsResource(googleapiclient.discovery.Resource):
        class LocationsResource(googleapiclient.discovery.Resource):
            class QueuesResource(googleapiclient.discovery.Resource):
                class TasksResource(googleapiclient.discovery.Resource):
                    def run(
                        self,
                        *,
                        name: str,
                        body: RunTaskRequest = ...,
                        **kwargs: typing.Any
                    ) -> TaskHttpRequest: ...
                    def list(
                        self,
                        *,
                        parent: str,
                        responseView: typing_extensions.Literal[
                            "VIEW_UNSPECIFIED", "BASIC", "FULL"
                        ] = ...,
                        pageSize: int = ...,
                        pageToken: str = ...,
                        **kwargs: typing.Any
                    ) -> ListTasksResponseHttpRequest: ...
                    def delete(
                        self, *, name: str, **kwargs: typing.Any
                    ) -> EmptyHttpRequest: ...
                    def get(
                        self,
                        *,
                        name: str,
                        responseView: typing_extensions.Literal[
                            "VIEW_UNSPECIFIED", "BASIC", "FULL"
                        ] = ...,
                        **kwargs: typing.Any
                    ) -> TaskHttpRequest: ...
                    def create(
                        self,
                        *,
                        parent: str,
                        body: CreateTaskRequest = ...,
                        **kwargs: typing.Any
                    ) -> TaskHttpRequest: ...
                def purge(
                    self,
                    *,
                    name: str,
                    body: PurgeQueueRequest = ...,
                    **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def create(
                    self, *, parent: str, body: Queue = ..., **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def setIamPolicy(
                    self,
                    *,
                    resource: str,
                    body: SetIamPolicyRequest = ...,
                    **kwargs: typing.Any
                ) -> PolicyHttpRequest: ...
                def list(
                    self,
                    *,
                    parent: str,
                    pageToken: str = ...,
                    filter: str = ...,
                    pageSize: int = ...,
                    **kwargs: typing.Any
                ) -> ListQueuesResponseHttpRequest: ...
                def get(
                    self, *, name: str, **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def patch(
                    self,
                    *,
                    name: str,
                    body: Queue = ...,
                    updateMask: str = ...,
                    **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def getIamPolicy(
                    self,
                    *,
                    resource: str,
                    body: GetIamPolicyRequest = ...,
                    **kwargs: typing.Any
                ) -> PolicyHttpRequest: ...
                def pause(
                    self,
                    *,
                    name: str,
                    body: PauseQueueRequest = ...,
                    **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def testIamPermissions(
                    self,
                    *,
                    resource: str,
                    body: TestIamPermissionsRequest = ...,
                    **kwargs: typing.Any
                ) -> TestIamPermissionsResponseHttpRequest: ...
                def delete(
                    self, *, name: str, **kwargs: typing.Any
                ) -> EmptyHttpRequest: ...
                def resume(
                    self,
                    *,
                    name: str,
                    body: ResumeQueueRequest = ...,
                    **kwargs: typing.Any
                ) -> QueueHttpRequest: ...
                def tasks(self) -> TasksResource: ...
            def list(
                self,
                *,
                name: str,
                pageSize: int = ...,
                filter: str = ...,
                pageToken: str = ...,
                **kwargs: typing.Any
            ) -> ListLocationsResponseHttpRequest: ...
            def get(
                self, *, name: str, **kwargs: typing.Any
            ) -> LocationHttpRequest: ...
            def queues(self) -> QueuesResource: ...
        def locations(self) -> LocationsResource: ...
    def projects(self) -> ProjectsResource: ...

class ListLocationsResponseHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> ListLocationsResponse: ...

class EmptyHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Empty: ...

class ListQueuesResponseHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> ListQueuesResponse: ...

class QueueHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Queue: ...

class LocationHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Location: ...

class TestIamPermissionsResponseHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> TestIamPermissionsResponse: ...

class TaskHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Task: ...

class PolicyHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Policy: ...

class ListTasksResponseHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> ListTasksResponse: ...
