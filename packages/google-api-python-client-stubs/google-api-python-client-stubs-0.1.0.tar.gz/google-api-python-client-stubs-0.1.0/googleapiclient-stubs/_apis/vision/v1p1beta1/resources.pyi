import typing

import httplib2  # type: ignore
import typing_extensions

import googleapiclient.discovery
import googleapiclient.http  # type: ignore

from .schemas import *

class VisionResource(googleapiclient.discovery.Resource):
    class ProjectsResource(googleapiclient.discovery.Resource):
        class LocationsResource(googleapiclient.discovery.Resource):
            class FilesResource(googleapiclient.discovery.Resource):
                def annotate(
                    self,
                    *,
                    parent: str,
                    body: GoogleCloudVisionV1p1beta1BatchAnnotateFilesRequest = ...,
                    **kwargs: typing.Any
                ) -> GoogleCloudVisionV1p1beta1BatchAnnotateFilesResponseHttpRequest: ...
                def asyncBatchAnnotate(
                    self,
                    *,
                    parent: str,
                    body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateFilesRequest = ...,
                    **kwargs: typing.Any
                ) -> OperationHttpRequest: ...
            class ImagesResource(googleapiclient.discovery.Resource):
                def asyncBatchAnnotate(
                    self,
                    *,
                    parent: str,
                    body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateImagesRequest = ...,
                    **kwargs: typing.Any
                ) -> OperationHttpRequest: ...
                def annotate(
                    self,
                    *,
                    parent: str,
                    body: GoogleCloudVisionV1p1beta1BatchAnnotateImagesRequest = ...,
                    **kwargs: typing.Any
                ) -> GoogleCloudVisionV1p1beta1BatchAnnotateImagesResponseHttpRequest: ...
            def files(self) -> FilesResource: ...
            def images(self) -> ImagesResource: ...
        class FilesResource(googleapiclient.discovery.Resource):
            def asyncBatchAnnotate(
                self,
                *,
                parent: str,
                body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateFilesRequest = ...,
                **kwargs: typing.Any
            ) -> OperationHttpRequest: ...
            def annotate(
                self,
                *,
                parent: str,
                body: GoogleCloudVisionV1p1beta1BatchAnnotateFilesRequest = ...,
                **kwargs: typing.Any
            ) -> GoogleCloudVisionV1p1beta1BatchAnnotateFilesResponseHttpRequest: ...
        class ImagesResource(googleapiclient.discovery.Resource):
            def annotate(
                self,
                *,
                parent: str,
                body: GoogleCloudVisionV1p1beta1BatchAnnotateImagesRequest = ...,
                **kwargs: typing.Any
            ) -> GoogleCloudVisionV1p1beta1BatchAnnotateImagesResponseHttpRequest: ...
            def asyncBatchAnnotate(
                self,
                *,
                parent: str,
                body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateImagesRequest = ...,
                **kwargs: typing.Any
            ) -> OperationHttpRequest: ...
        def locations(self) -> LocationsResource: ...
        def files(self) -> FilesResource: ...
        def images(self) -> ImagesResource: ...
    class FilesResource(googleapiclient.discovery.Resource):
        def asyncBatchAnnotate(
            self,
            *,
            body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateFilesRequest = ...,
            **kwargs: typing.Any
        ) -> OperationHttpRequest: ...
        def annotate(
            self,
            *,
            body: GoogleCloudVisionV1p1beta1BatchAnnotateFilesRequest = ...,
            **kwargs: typing.Any
        ) -> GoogleCloudVisionV1p1beta1BatchAnnotateFilesResponseHttpRequest: ...
    class ImagesResource(googleapiclient.discovery.Resource):
        def asyncBatchAnnotate(
            self,
            *,
            body: GoogleCloudVisionV1p1beta1AsyncBatchAnnotateImagesRequest = ...,
            **kwargs: typing.Any
        ) -> OperationHttpRequest: ...
        def annotate(
            self,
            *,
            body: GoogleCloudVisionV1p1beta1BatchAnnotateImagesRequest = ...,
            **kwargs: typing.Any
        ) -> GoogleCloudVisionV1p1beta1BatchAnnotateImagesResponseHttpRequest: ...
    def projects(self) -> ProjectsResource: ...
    def files(self) -> FilesResource: ...
    def images(self) -> ImagesResource: ...

class GoogleCloudVisionV1p1beta1BatchAnnotateImagesResponseHttpRequest(
    googleapiclient.http.HttpRequest
):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> GoogleCloudVisionV1p1beta1BatchAnnotateImagesResponse: ...

class GoogleCloudVisionV1p1beta1BatchAnnotateFilesResponseHttpRequest(
    googleapiclient.http.HttpRequest
):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> GoogleCloudVisionV1p1beta1BatchAnnotateFilesResponse: ...

class OperationHttpRequest(googleapiclient.http.HttpRequest):
    def execute(
        self, http: typing.Optional[httplib2.Http] = ..., num_retries: int = ...
    ) -> Operation: ...
