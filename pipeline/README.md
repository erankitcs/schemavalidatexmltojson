
# Welcome to your CDK Python project!

### PreRequisites
1. Create Repository named - schemavalidatexmltojson using below AWS CLI Command.
```
aws codecommit create-repository --repository-name schemavalidatexmltojson
```

This is a CI/CD project based Python development with CDK for SAM Application (schemavalidatexmltojson)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

## commands to test, build and deploy

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Start the Pipeline
* Get Code Commit credentials from IAM.
* From root folder of the project, Setup code commit by running git add remote command.
```bash
git remote add cmrepo <REPO URL>
```
* Push changes to AWS Code Commit using below commands.
```bash
git add .
git commit -m "Some comment here"
git push cmrepo master
```
