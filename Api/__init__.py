parameters:
  - name: serviceConnection
    type: string
  - name: environmentType
    type: string
  - name: functionAppName
    type: string

jobs:
  - deployment: Deploy
    environment: ${{parameters.environmentType}}
    displayName: Deploying FunctionApp.
    strategy:
      runOnce:
        deploy:
          steps:
            - checkout: self
            - task: DownloadBuildArtifacts@0
              displayName: "Download Artifact"
              inputs:
                artifactName: "drop"
                downloadPath: "$(Build.ArtifactStagingDirectory)"
            - task: AzureFunctionApp@2
              displayName: "Deploy functionApp"
              inputs:
                connectedServiceNameARM: "${{parameters.serviceConnection}}"
                appType: "functionAppLinux"
                appName: "${{parameters.functionAppName}}"
                package: "$(Build.ArtifactStagingDirectory)/drop/function-app-$(Build.BuildId).zip"
                runtimeStack: "PYTHON|3.13"
                deploymentMethod: "runFromPackage"
            - task: AzureAppServiceManage@0
              displayName: "Restart FunctionApp"
              inputs:
                azureSubscription: ${{parameters.serviceConnection}}
                Action: "Restart Azure App Service"
                WebAppName: ${{parameters.functionAppName}}
