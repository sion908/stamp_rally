import { Template } from "aws-cdk-lib/assertions";
import * as cdk from "aws-cdk-lib";
import { RogainingSystemStack } from "../lib/rogaining-system-cdk-stack";

describe("rogainingSystemStack", () => {
  test("synthesizes the way we expect", () => {
    const app = new cdk.App();

    // Create the ProcessorStack.
    const rogainingSystemStack = new RogainingSystemStack(app, "rogainingSystemStack", {
      stageName: 'dev'
    });

    // Prepare the stack for assertions.
    const template = Template.fromStack(rogainingSystemStack);

    // Assert it creates the function with the correct properties...
    template.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "main.handler",
      Runtime: "python3.10",
      MemorySize: 256,
      Timeout: 180
    });
    template.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "index.handler",
      Runtime: "nodejs18.x"
    });


    // Creates lambda function main AND for LOG
    template.resourceCountIs("AWS::Lambda::Function", 2);
    template.resourceCountIs("AWS::ApiGateway::RestApi", 1);

  })},
)
