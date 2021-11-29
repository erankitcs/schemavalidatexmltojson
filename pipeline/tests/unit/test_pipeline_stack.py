from aws_cdk import (
        core,
        assertions
    )

from pipeline.pipeline_stack import PipelineStack
import pytest

# example tests. To run these tests, uncomment this file along with the example
# resource in pipeline/pipeline_stack.py
def test_pipeline_created():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.find_resources)
    template.resource_count_is("AWS::CodePipeline::Pipeline",1)
def test_codebuild_created():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.find_resources)
    template.resource_count_is("AWS::CodeBuild::Project",1)

def test_source_stage_created():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.to_json)
    expected = {
    "Stages": assertions.Match.array_with([assertions.Match.object_like(
      {
        "Name":"Source"
      }
    )])
    }  
    template.has_resource_properties("AWS::CodePipeline::Pipeline",expected)

def test_build_stage_created():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.to_json)
    expected = {
    "Stages": assertions.Match.array_with([assertions.Match.object_like(
      {
        "Name":"Build"
      }
    )])
    }  
    template.has_resource_properties("AWS::CodePipeline::Pipeline",expected)

def test_dev_stage_created():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.to_json)
    expected = {
    "Stages": assertions.Match.array_with([assertions.Match.object_like(
      {
        "Name":"Dev"
      }
    )])
    }  
    template.has_resource_properties("AWS::CodePipeline::Pipeline",expected)

def test_source_branch_master():
    app = core.App()
    stack = PipelineStack(app, "pipeline")
    template = assertions.Template.from_stack(stack)
    print(template.to_json)
    expected = {
    "Stages": assertions.Match.array_with([assertions.Match.object_like(
      {
        "Name":"Source",
        "Actions": assertions.Match.array_with([assertions.Match.object_like(
          {
            "Configuration": {
              "BranchName": "master"
            }
          }
        )])
      }
    )])
    }  
    template.has_resource_properties("AWS::CodePipeline::Pipeline",expected)