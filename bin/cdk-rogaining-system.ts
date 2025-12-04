#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { RogainingSystemStack } from "../lib/rogaining-system-cdk-stack";
import { ENVS } from "../lib/env";

const app = new cdk.App();

// 環境の指定 -c environment=('dev'||'prod')
const argContext = 'environment';
const stageName = app.node.tryGetContext(argContext);

if(!Object.values(ENVS).includes(stageName)){
  throw new Error(
    `環境が指定されていないまたは、適当な環境が指定されていません -> env_name:${stageName}`
  );
}

const rogainingSystemStack = new RogainingSystemStack(app, `RogainingSystemStack-${stageName}`,{
  stageName: stageName,
});

cdk.Tags.of(rogainingSystemStack).add("Project", "rogaining-system")
cdk.Tags.of(rogainingSystemStack).add("Project_env", `rogaining-system-${stageName}`)
