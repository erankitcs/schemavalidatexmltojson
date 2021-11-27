# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions
)



class PipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        artifacts_bucket = s3.Bucket(self, "ArtifactsBucket")

        ## Importing exiting Code Commit.
        code_repo = codecommit.Repository.from_repository_name(self,'AppRepository',repository_name="schemavalidatexmltojson")
        ## Pipeline creation starts-
        pipeline = codepipeline.Pipeline(
            self,'XmltojsonPipeline',
            artifact_bucket=artifacts_bucket
        )
        ## Declare Source code as a Artifacts.
        source_output = codepipeline.Artifact()

        ## Add Source stage to pipeline.
        pipeline.add_stage(
            stage_name="Source",
            actions=[
                codepipeline_actions.CodeCommitSourceAction(
                    action_name="Source",
                    branch="main",
                    output=source_output,
                    repository=code_repo
                )
            ]
        )

        # Declare build output as artifacts
        build_output = codepipeline.Artifact()
        # New Code Build project to build artifacts.
        build_project = codebuild.PipelineProject(
            self,"Build",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            environment_variables={
                'PACKAGE_BUCKET': codebuild.BuildEnvironmentVariable(value=artifacts_bucket.bucket_name)
            },
        )
        ## Adding build stage to pipeline
        pipeline.add_stage(
            stage_name="Build",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="Build",
                    project=build_project,
                    input=source_output,
                    outputs=[build_output],
                )
            ]
        )
